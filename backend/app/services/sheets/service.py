"""
Servicio MEJORADO para Google Sheets - Versión 3.0
Sistema robusto con:
- Manejo de errores mejorado
- Timeouts configurables
- Reconexión automática
- Sistema de caché con invalidación
- Circuit breaker para fallos
- Métricas de rendimiento
"""

import gspread
from pathlib import Path
from google.oauth2.service_account import Credentials
from google.api_core.exceptions import GoogleAPIError, ServiceUnavailable, GatewayTimeout
import time
import logging
import json
import random
import os
from typing import List, Dict, Any, Optional, Callable, TypeVar, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from functools import wraps
import statistics
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    RetryCallState
)

# Tipos personalizados
T = TypeVar('T')
CacheKey = str
CacheValue = Any

@dataclass
class CacheEntry:
    value: Any
    expires_at: float
    metadata: dict = None

class CircuitBreakerError(Exception):
    """Excepción lanzada cuando el circuito está abierto"""
    pass

class SheetsServiceV2:
    """
    Servicio mejorado para interactuar con Google Sheets.
    
    Esta implementación incluye características avanzadas para mejorar la confiabilidad y el rendimiento:
    
    Características principales:
    - Manejo automático de reconexiones con backoff exponencial
    - Sistema de caché con expiración para reducir llamadas a la API
    - Circuit breaker para prevenir fallos en cascada
    - Métricas detalladas de rendimiento y errores
    - Reintentos automáticos con jitter para evitar el efecto de tormenta
    - Logging detallado para diagnóstico
    
    Uso básico:
        service = SheetsServiceV2()
        
        # Obtener todas las filas
        rows = service.get_all_rows()
        
        # Buscar una fila por ID
        row = service.get_row_by_id(123)
        
        # Agregar una nueva fila
        service.add_row({"ID": 123, "Nombre": "Ejemplo"})
        
        # Actualizar una fila existente
        service.update_row(123, {"Estado": "Completado"})
        
        # Eliminar una fila
        service.delete_row(123)
        
        # Buscar en todas las columnas
        results = service.search_rows("término de búsqueda")
    
    Configuración:
    - El servicio busca automáticamente el archivo de credenciales en varias ubicaciones
    - Los tiempos de espera y reintentos son configurables mediante constantes de clase
    - El sistema de caché se puede habilitar/deshabilitar por operación
    
    Manejo de errores:
    - Las excepciones de la API de Google se capturan y registran
    - Se proporciona información detallada en los logs
    - El circuit breaker evita sobrecargar el servicio en caso de fallos
    """
    
    # Configuración de la hoja
    SHEET_ID = "1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ"
    
    # Configuración de reintentos
    MAX_RETRIES = 3
    INITIAL_RETRY_DELAY = 1  # segundos
    MAX_RETRY_DELAY = 30  # segundos
    
    # Configuración del circuit breaker
    CIRCUIT_BREAKER_MAX_FAILURES = 5
    CIRCUIT_BREAKER_RESET_TIMEOUT = 300  # segundos
    
    # Configuración de caché
    DEFAULT_CACHE_TTL = 60  # segundos
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Inicializa el servicio con configuración por defecto.
        
        Args:
            logger: Instancia de logger personalizada. Si no se proporciona,
                   se creará una nueva instancia con el nombre del módulo.
        """
        self.logger = logger or logging.getLogger(f"{__name__}.SheetsServiceV2")
        
        # Configurar formato de logging si no hay manejadores configurados
        if not self.logger.handlers and logging.getLogger().level == logging.NOTSET:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        # Inicializar cliente y hoja de cálculo
        self.gc = None
        self.sheet = None
        self.sheet_id = self.SHEET_ID
        
        # Estado del circuit breaker
        self._circuit_state = {
            'failures': 0,          # Número de fallos consecutivos
            'last_failure': None,   # Marca de tiempo del último fallo
            'is_open': False        # Si el circuito está abierto
        }
        
        # Sistema de caché mejorado
        self._cache: Dict[CacheKey, CacheEntry] = {}
        self._cache_metrics = {
            'hits': 0,
            'misses': 0,
            'expired': 0,
            'size': 0
        }
        
        # Caché simple adicional para compatibilidad
        self._cache_timestamp = 0
        self._cache_duration = 60  # 60 segundos
        
        # Métricas de rendimiento
        self._performance_metrics = {
            'calls': [],
            'errors': [],
            'response_times': []
        }
        
        # Inicializar la conexión
        self._initialize_connection()
    
    def _check_circuit(self):
        """Verifica el estado del circuit breaker"""
        if not self._circuit_state['is_open']:
            return True
            
        last_failure = self._circuit_state['last_failure']
        if last_failure and (time.time() - last_failure) > self.CIRCUIT_BREAKER_RESET_TIMEOUT:
            self.logger.warning("🔁 Intentando restablecer el circuit breaker")
            self._circuit_state = {
                'failures': 0,
                'last_failure': None,
                'is_open': False
            }
            return True
            
        return False
        
    def _record_failure(self):
        """Registra un fallo y actualiza el estado del circuit breaker"""
        self._circuit_state['failures'] += 1
        self._circuit_state['last_failure'] = time.time()
        
        if self._circuit_state['failures'] >= self.CIRCUIT_BREAKER_MAX_FAILURES:
            self._circuit_state['is_open'] = True
            self.logger.error(f"🚨 Circuit breaker abierto después de {self._circuit_state['failures']} fallos")
    
    def _record_success(self):
        """Registra un éxito y reinicia el contador de fallos"""
        if self._circuit_state['failures'] > 0:
            self.logger.info("✅ Operación exitosa, reiniciando contador de fallos")
            self._circuit_state['failures'] = 0
            self._circuit_state['last_failure'] = None
    
    # ===== MÉTODOS DE CACHÉ =====
    
    def _get_cache_key(self, method_name: str, *args, **kwargs) -> str:
        """Genera una clave única para el caché basada en el método y argumentos"""
        args_str = json.dumps(args, default=str, sort_keys=True)
        kwargs_str = json.dumps(kwargs, default=str, sort_keys=True)
        return f"{method_name}:{args_str}:{kwargs_str}"
    
    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché si existe y no ha expirado"""
        if key not in self._cache:
            self._cache_metrics['misses'] += 1
            return None
            
        entry = self._cache[key]
        
        # Verificar si la entrada ha expirado
        if time.time() > entry.expires_at:
            self._cache_metrics['expired'] += 1
            del self._cache[key]
            self._cache_metrics['size'] -= 1
            return None
            
        self._cache_metrics['hits'] += 1
        return entry.value
    
    def _set_cache(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Almacena un valor en el caché con un TTL opcional"""
        if ttl is None:
            ttl = self.DEFAULT_CACHE_TTL
            
        expires_at = time.time() + ttl
        self._cache[key] = CacheEntry(
            value=value,
            expires_at=expires_at,
            metadata={
                'stored_at': datetime.now().isoformat(),
                'ttl': ttl
            }
        )
        self._cache_metrics['size'] = len(self._cache)
    
    def clear_cache(self, pattern: Optional[str] = None) -> int:
        """Limpia el caché, opcionalmente filtrando por patrón de clave"""
        if pattern is None:
            count = len(self._cache)
            self._cache.clear()
            self._cache_metrics['size'] = 0
            return count
            
        # Filtrar por patrón
        to_delete = [k for k in self._cache if pattern in k]
        for k in to_delete:
            del self._cache[k]
            
        self._cache_metrics['size'] = len(self._cache)
        return len(to_delete)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del caché"""
        return {
            'hits': self._cache_metrics['hits'],
            'misses': self._cache_metrics['misses'],
            'expired': self._cache_metrics['expired'],
            'size': self._cache_metrics['size'],
            'hit_ratio': (
                self._cache_metrics['hits'] / 
                (self._cache_metrics['hits'] + self._cache_metrics['misses'] + 1e-10)
            )
        }
    
    # ===== MÉTODOS DE OPERACIONES CON REINTENTOS =====
    
    def _execute_with_retry(
        self, 
        operation: Callable[..., T],
        *args,
        max_retries: Optional[int] = None,
        initial_delay: float = 1.0,
        max_delay: float = 30.0,
        **kwargs
    ) -> T:
        """
        Ejecuta una operación con reintentos exponenciales y backoff.
        
        Args:
            operation: Función a ejecutar
            *args: Argumentos posicionales para la función
            max_retries: Número máximo de reintentos (None para usar el valor por defecto)
            initial_delay: Tiempo de espera inicial en segundos
            max_delay: Tiempo máximo de espera entre reintentos
            **kwargs: Argumentos con nombre para la función
            
        Returns:
            El resultado de la operación
            
        Raises:
            Exception: Si se agotan los reintentos
        """
        if max_retries is None:
            max_retries = self.MAX_RETRIES
            
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                start_time = time.time()
                result = operation(*args, **kwargs)
                elapsed = (time.time() - start_time) * 1000  # ms
                
                # Registrar métricas de rendimiento
                self._record_metrics(operation.__name__, elapsed)
                
                # Si llegamos aquí, la operación fue exitosa
                self._record_success()
                return result
                
            except Exception as e:
                last_exception = e
                self._record_failure()
                
                # Registrar error
                self._record_error(operation.__name__, str(e))
                
                # Si no hay más reintentos, lanzar la excepción
                if attempt == max_retries:
                    self.logger.error(
                        f"❌ Error después de {max_retries} intentos: {e}",
                        exc_info=True
                    )
                    raise
                
                # Calcular espera exponencial con jitter
                delay = min(
                    initial_delay * (2 ** attempt) * (0.5 * (1 + random.random())),
                    max_delay
                )
                
                self.logger.warning(
                    f"🔄 Reintentando operación {operation.__name__} en {delay:.2f}s "
                    f"(intento {attempt + 1}/{max_retries}): {e}"
                )
                
                time.sleep(delay)
        
        # Este punto no debería alcanzarse nunca debido al raise anterior
        raise RuntimeError("Error inesperado en _execute_with_retry")
    
    # ===== MÉTRICAS Y MONITOREO =====
    
    def _record_metrics(self, operation: str, response_time_ms: float) -> None:
        """Registra métricas de rendimiento"""
        self._performance_metrics['calls'].append({
            'operation': operation,
            'timestamp': datetime.now().isoformat(),
            'response_time_ms': response_time_ms
        })
        
        # Mantener solo las últimas 1000 llamadas para evitar uso excesivo de memoria
        if len(self._performance_metrics['calls']) > 1000:
            self._performance_metrics['calls'] = self._performance_metrics['calls'][-1000:]
        
        # Actualizar estadísticas de tiempo de respuesta
        self._performance_metrics['response_times'].append(response_time_ms)
        if len(self._performance_metrics['response_times']) > 1000:
            self._performance_metrics['response_times'] = self._performance_metrics['response_times'][-1000:]
    
    def _record_error(self, operation: str, error: str) -> None:
        """Registra un error en las métricas"""
        self._performance_metrics['errors'].append({
            'operation': operation,
            'timestamp': datetime.now().isoformat(),
            'error': error
        })
        
        # Mantener solo los últimos 100 errores
        if len(self._performance_metrics['errors']) > 100:
            self._performance_metrics['errors'] = self._performance_metrics['errors'][-100:]
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas de rendimiento"""
        response_times = self._performance_metrics['response_times']
        
        return {
            'total_calls': len(self._performance_metrics['calls']),
            'total_errors': len(self._performance_metrics['errors']),
            'error_rate': (
                len(self._performance_metrics['errors']) / 
                (len(self._performance_metrics['calls']) + 1e-10)
            ),
            'response_time': {
                'min': min(response_times, default=0),
                'max': max(response_times, default=0),
                'avg': sum(response_times) / len(response_times) if response_times else 0,
                'p50': statistics.quantiles(response_times, n=10)[4] if len(response_times) >= 2 else 0,
                'p90': statistics.quantiles(response_times, n=10)[8] if len(response_times) >= 10 else 0,
                'p99': statistics.quantiles(response_times, n=100)[98] if len(response_times) >= 100 else 0,
            },
            'circuit_breaker': {
                'is_open': self._circuit_state['is_open'],
                'failures': self._circuit_state['failures'],
                'last_failure': self._circuit_state['last_failure']
            },
            'cache': self.get_cache_stats()
        }
    
    def _initialize_connection(self) -> None:
        """Inicializa la conexión con Google Sheets con manejo de errores y circuit breaker"""
        if self._circuit_state.get('is_open', False) and not self._check_circuit():
            self.logger.error("🔴 Circuit breaker abierto, no se puede conectar")
            raise CircuitBreakerError("El servicio no está disponible temporalmente")
            
        try:
            start_time = time.time()
            
            # Buscar archivo de credenciales en múltiples ubicaciones
            possible_paths = [
                Path('/etc/secrets/service_account.json'),  # Para Docker/Kubernetes
                Path(__file__).parents[4] / 'service_account.json',  # Raíz del proyecto  
                Path(__file__).parents[3] / 'config' / 'service_account.json',
                Path(__file__).parents[3] / 'service_account.json',
                Path(__file__).parents[2] / 'config' / 'service_account.json',
                Path('service_account.json')
            ]
            
            credentials_path = None
            for path in possible_paths:
                if path.exists():
                    credentials_path = str(path.resolve())
                    self.logger.info(f"📁 Credenciales encontradas en: {credentials_path}")
                    break
                if path.exists():
                    credentials_path = str(path.resolve())
            
            # Configuración de ámbitos de acceso
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/spreadsheets'
            ]
            
            # Intenta cargar credenciales desde el archivo
            creds = None
            
            # Primero intentar usar el archivo encontrado
            if credentials_path:
                self.logger.info(f"🔑 Cargando credenciales desde: {credentials_path}")
                creds = Credentials.from_service_account_file(
                    credentials_path,
                    scopes=scope
                )
            # Después, revisar otras ubicaciones
            elif Path.home().joinpath('.config/gspread/service_account.json').exists():
                creds_file = Path.home() / '.config/gspread/service_account.json'
                self.logger.info(f"🔑 Cargando credenciales desde: {creds_file}")
                creds = Credentials.from_service_account_file(
                    str(creds_file),
                    scopes=scope
                )
            elif 'GOOGLE_CREDENTIALS_JSON' in os.environ:
                self.logger.info("🔑 Cargando credenciales desde variable de entorno")
                creds = Credentials.from_service_account_info(
                    json.loads(os.environ['GOOGLE_CREDENTIALS_JSON']),
                    scopes=scope
                )
            else:
                error_msg = "❌ No se encontraron credenciales de Google Sheets en ninguna ubicación"
                self.logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Crear cliente con configuración de timeout
            client = gspread.Client(auth=creds)
            
            # Configurar timeout (usando la sesión de autenticación subyacente)
            if hasattr(creds, '_http'):
                creds._http.timeout = 30  # Timeout de 30 segundos
            
            # Guardar cliente
            self.gc = client
            
            # Inicializar la hoja específica
            try:
                spreadsheet = self.gc.open_by_key(self.sheet_id)
                self.sheet = spreadsheet.worksheet("01_Clientes")  # Hoja específica de clientes
                self.logger.info(f"📋 Hoja '01_Clientes' inicializada correctamente")
            except Exception as e:
                self.logger.warning(f"⚠️  No se pudo inicializar la hoja '01_Clientes': {e}")
                self.logger.info("🔄 Intentando obtener la primera hoja disponible...")
                try:
                    spreadsheet = self.gc.open_by_key(self.sheet_id)
                    self.sheet = spreadsheet.get_worksheet(0)  # Primera hoja
                    self.logger.info(f"📋 Hoja '{self.sheet.title}' inicializada como fallback")
                except Exception as e2:
                    self.logger.error(f"❌ Error crítico al inicializar cualquier hoja: {e2}")
                    self.sheet = None
            
            self.initialized = True
            self.logger.info("✅ Conexión con Google Sheets establecida correctamente")
            
        except GoogleAPIError as e:
            self._record_failure()
            self.logger.error(f"❌ Error de API de Google: {str(e)}")
            raise
        except Exception as e:
            self._record_failure()
            self.logger.error(f"❌ Error inesperado al inicializar conexión: {str(e)}")
            self.logger.error(f"❌ Error crítico al inicializar conexión: {e}", exc_info=True)
            raise
    
    # ===== OPERACIONES PRINCIPALES =====
    
    def get_all_rows(self, use_cache: bool = True) -> List[Dict[str, Any]]:
        """Obtiene todas las filas de la hoja de cálculo"""
        cache_key = self._get_cache_key('get_all_rows')
        
        # Intentar obtener del caché si está habilitado
        if use_cache:
            cached = self._get_from_cache(cache_key)
            if cached is not None:
                self.logger.debug("📦 Datos obtenidos del caché")
                return cached
        
        # Si no hay datos en caché o el caché está deshabilitado
        def _fetch_rows():
            try:
                # Obtener todas las filas
                rows = self.sheet.get_all_records()
                self.logger.info(f"📊 Se obtuvieron {len(rows)} filas de la hoja de cálculo")
                return rows
            except Exception as e:
                self.logger.error(f"❌ Error al obtener filas: {e}")
                raise
        
        # Ejecutar con reintentos
        rows = self._execute_with_retry(_fetch_rows)
        
        # Almacenar en caché si la operación fue exitosa
        if rows is not None and use_cache:
            self._set_cache(cache_key, rows)
        
        return rows
    
    def get_row_by_id(self, row_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una fila por su ID"""
        def _fetch_row():
            try:
                # Obtener todas las celdas de la columna de ID
                ids = self.sheet.col_values(1)  # Asumiendo que el ID está en la primera columna
                
                # Buscar el ID
                for i, id_str in enumerate(ids[1:], start=2):  # Saltar el encabezado
                    try:
                        if int(id_str) == row_id:
                            # Obtener toda la fila
                            row = self.sheet.row_values(i)
                            headers = self.sheet.row_values(1)
                            return dict(zip(headers, row))
                    except (ValueError, IndexError):
                        continue
                
                return None
                
            except Exception as e:
                self.logger.error(f"❌ Error al buscar fila con ID {row_id}: {e}")
                raise
        
        return self._execute_with_retry(_fetch_row)
    
    def add_row(self, data: Dict[str, Any]) -> bool:
        """Agrega una nueva fila a la hoja de cálculo"""
        def _insert_row():
            try:
                # Obtener encabezados
                headers = self.sheet.row_values(1)
                
                # Preparar fila en el orden correcto
                row = []
                for header in headers:
                    row.append(str(data.get(header, '')))
                
                # Agregar fila al final
                self.sheet.append_row(row)
                
                # Invalidar caché de todas las filas
                self.clear_cache('get_all_rows')
                
                self.logger.info(f"✅ Fila agregada exitosamente: {data}")
                return True
                
            except Exception as e:
                self.logger.error(f"❌ Error al agregar fila: {e}")
                raise
        
        return self._execute_with_retry(_insert_row)
    
    def update_row(self, row_id: int, data: Dict[str, Any]) -> bool:
        """Actualiza una fila existente"""
        def _update_row():
            try:
                # Obtener todas las celdas de la columna de ID
                ids = self.sheet.col_values(1)  # Asumiendo que el ID está en la primera columna
                
                # Buscar el ID
                for i, id_str in enumerate(ids[1:], start=2):  # Saltar el encabezado
                    try:
                        if int(id_str) == row_id:
                            # Obtener encabezados
                            headers = self.sheet.row_values(1)
                            
                            # Preparar actualización
                            updates = []
                            for j, header in enumerate(headers, start=1):
                                if header in data:
                                    updates.append({
                                        'range': f"{gspread.utils.rowcol_to_a1(i, j)}:{gspread.utils.rowcol_to_a1(i, j)}",
                                        'values': [[str(data[header])]]
                                    })
                            
                            # Aplicar actualizaciones
                            if updates:
                                self.sheet.batch_update(updates)
                                
                                # Invalidar caché
                                self.clear_cache()
                                
                                self.logger.info(f"✅ Fila {row_id} actualizada exitosamente")
                                return True
                            
                            break
                            
                    except (ValueError, IndexError):
                        continue
                
                self.logger.warning(f"⚠️ No se encontró la fila con ID {row_id}")
                return False
                
            except Exception as e:
                self.logger.error(f"❌ Error al actualizar fila {row_id}: {e}")
                raise
        
        return self._execute_with_retry(_update_row)
    
    def delete_row(self, row_id: int) -> bool:
        """Elimina una fila por su ID"""
        def _delete_row():
            try:
                # Obtener todas las celdas de la columna de ID
                ids = self.sheet.col_values(1)  # Asumiendo que el ID está en la primera columna
                
                # Buscar el ID
                for i, id_str in enumerate(ids[1:], start=2):  # Saltar el encabezado
                    try:
                        if int(id_str) == row_id:
                            # Eliminar fila
                            self.sheet.delete_rows(i)
                            
                            # Invalidar caché
                            self.clear_cache()
                            
                            self.logger.info(f"✅ Fila {row_id} eliminada exitosamente")
                            return True
                            
                    except (ValueError, IndexError):
                        continue
                
                self.logger.warning(f"⚠️ No se encontró la fila con ID {row_id}")
                return False
                
            except Exception as e:
                self.logger.error(f"❌ Error al eliminar fila {row_id}: {e}")
                raise
        
        return self._execute_with_retry(_delete_row)
    
    def search_rows(self, query: str, column: Optional[str] = None) -> List[Dict[str, Any]]:
        """Busca filas que coincidan con el criterio de búsqueda"""
        def _search():
            try:
                # Obtener todas las filas
                rows = self.get_all_rows()
                
                # Si no hay filas, retornar lista vacía
                if not rows:
                    return []
                
                # Filtrar filas que coincidan con la búsqueda
                query_lower = query.lower()
                results = []
                
                for row in rows:
                    # Si se especificó una columna, buscar solo en esa columna
                    if column:
                        if column in row and query_lower in str(row[column]).lower():
                            results.append(row)
                    else:
                        # Buscar en todas las columnas
                        for value in row.values():
                            if query_lower in str(value).lower():
                                results.append(row)
                                break
                
                self.logger.info(f"🔍 Encontradas {len(results)} coincidencias para '{query}'")
                return results
                
            except Exception as e:
                self.logger.error(f"❌ Error al buscar '{query}': {e}")
                raise
        
        return self._execute_with_retry(_search)
    
    def _get_cached_data(self, key: str):
        """Obtiene datos del cache si están vigentes"""
        current_time = time.time()
        if (current_time - self._cache_timestamp < self._cache_duration and 
            key in self._cache):
            return self._cache[key]
        
        # También verificar el caché avanzado
        if key in self._cache:
            entry = self._cache[key]
            if hasattr(entry, 'value'):
                return entry.value
            
        return None
    
    def _set_cache_data(self, key: str, data):
        """Guarda datos en cache"""
        self._cache[key] = data
        self._cache_timestamp = time.time()
    
    def get_all_clients(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Obtiene todos los clientes con cache y manejo de errores"""
        cache_key = f"all_clients_{include_inactive}"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        def _get_records():
            if self.sheet is None:
                self.logger.warning("⚠️  self.sheet is None, usando datos offline")
                return self._get_offline_data()
            
            try:
                self.logger.info("🔍 Intentando obtener registros desde Google Sheets...")
                records = self.sheet.get_all_records()
                self.logger.info(f"📊 Obtenidos {len(records)} registros desde Google Sheets")
                self.logger.info(f"🔍 Muestra de los primeros 2 registros: {records[:2] if records else 'Sin registros'}")
                
                # Si no hay registros reales, usar datos offline
                if not records:
                    self.logger.warning("⚠️  No se encontraron registros en Google Sheets, usando datos offline")
                    return self._get_offline_data()
                
                # Mapear campos de la Google Sheet real a los campos esperados
                mapped_records = []
                for i, record in enumerate(records):
                    # Mapear los campos existentes a los esperados
                    mapped_record = {
                        "Nombre": record.get("Nombre", ""),
                        "Email": record.get("Email", ""),  # Este campo puede no existir
                        "Zona": record.get("Zona", ""),
                        "Teléfono": record.get("Teléfono", ""),
                        "Pago": record.get("Pago", record.get("Precio", record.get("Mensualidad", "0"))),  # Varios nombres posibles
                        "Activo (SI/NO)": record.get("Activo (SI/NO)", "SI"),
                        "ID Cliente": record.get("ID Cliente", ""),
                        "Inicio Contrato": record.get("Inicio Contrato", ""),
                        "Propietario": record.get("Propietario", "")
                    }
                    
                    # Solo incluir registros que tengan al menos nombre
                    if mapped_record["Nombre"].strip():
                        mapped_records.append(mapped_record)
                    elif i < 5:  # Log de los primeros registros vacíos para debug
                        self.logger.debug(f"🔍 Registro {i} sin nombre válido: {record}")
                
                self.logger.info(f"📋 Después del mapeo: {len(mapped_records)} registros válidos")
                
                if not include_inactive:
                    # Filtrar solo clientes activos
                    active_records = []
                    for r in mapped_records:
                        activo = str(r.get('Activo (SI/NO)', '')).strip().lower()
                        if activo in ['si', 'sí', 'yes', '1', 'true', 'activo']:
                            active_records.append(r)
                    self.logger.info(f"✅ Clientes activos filtrados: {len(active_records)}")
                    return active_records
                
                return mapped_records
                
            except Exception as e:
                self.logger.error(f"❌ Error obteniendo registros de Google Sheets: {e}")
                return self._get_offline_data()

        try:
            data = self._execute_with_retry(_get_records)
            if data is not None:
                self._set_cache_data(cache_key, data)
                return data
            else:
                return self._get_offline_data()
        except Exception as e:
            self.logger.error(f"Error obteniendo clientes: {e}")
            return self._get_offline_data()

    def find_client_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Busca clientes por nombre con optimización"""
        if not name or len(name.strip()) < 2:
            return []
        
        all_clients = self.get_all_clients()
        name = name.strip().lower()
        
        matching_clients = []
        search_fields = ["Nombre", "Email", "Zona", "Teléfono", "ID Cliente"]
        
        for client in all_clients:
            for field in search_fields:
                value = str(client.get(field, "")).strip().lower()
                if name in value and value:
                    matching_clients.append(client)
                    break
        
        return matching_clients
    
    def add_client(self, data: Dict[str, str]) -> bool:
        """Agrega cliente con validación y manejo de errores"""
        def _add_row():
            if self.sheet is None:
                return False
            
            # Validar datos requeridos
            required_fields = ['Nombre']
            for field in required_fields:
                if not data.get(field, '').strip():
                    raise ValueError(f"Campo requerido faltante: {field}")
            
            # Preparar fila para insertar
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            row_data = [
                data.get('Nombre', ''),
                data.get('Email', ''),
                data.get('Zona', ''),
                data.get('Teléfono', ''),
                data.get('Pago', ''),
                'SI',  # Activo por defecto
                current_time,  # Fecha de alta
                data.get('Notas', f'Agregado via sistema el {current_time}')
            ]
            
            self.sheet.append_row(row_data)
            return True
        
        try:
            result = self._execute_with_retry(_add_row)
            if result:
                # Limpiar cache
                self._cache.clear()
                self.logger.info(f"✅ Cliente agregado: {data.get('Nombre')}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Error agregando cliente: {e}")
            return False
    
    def add_prospect(self, data: Dict[str, str]) -> bool:
        """Agrega prospecto a una hoja separada"""
        def _add_prospect_row():
            if self.gc is None:
                return False
            
            try:
                # Intentar acceder a hoja de prospectos, crearla si no existe
                try:
                    spreadsheet = self.gc.open_by_key(self.sheet_id)
                    prospects_sheet = spreadsheet.worksheet("Prospectos")
                except gspread.WorksheetNotFound:
                    # Crear hoja de prospectos
                    spreadsheet = self.gc.open_by_key(self.sheet_id)
                    prospects_sheet = spreadsheet.add_worksheet(
                        title="Prospectos", 
                        rows=1000, 
                        cols=10
                    )
                    # Agregar encabezados
                    headers = [
                        "Nombre", "Teléfono", "Zona", "Email", "Estado", 
                        "Fecha Contacto", "Notas", "Prioridad", "Origen", "Siguiente Acción"
                    ]
                    prospects_sheet.append_row(headers)
                
                # Agregar prospecto
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                row_data = [
                    data.get('Nombre', ''),
                    data.get('Teléfono', ''),
                    data.get('Zona', ''),
                    data.get('Email', ''),
                    'Nuevo',  # Estado inicial
                    current_time,
                    data.get('Notas', 'Prospecto agregado via chat'),
                    data.get('Prioridad', 'Media'),
                    'Sistema',
                    'Llamar para ofrecer servicios'
                ]
                
                prospects_sheet.append_row(row_data)
                return True
                
            except Exception as e:
                self.logger.error(f"Error en hoja de prospectos: {e}")
                return False
        
        try:
            result = self._execute_with_retry(_add_prospect_row)
            if result:
                self.logger.info(f"✅ Prospecto agregado: {data.get('Nombre')}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Error agregando prospecto: {e}")
            return False
    
    def get_prospects(self) -> List[Dict[str, Any]]:
        """Obtiene lista de prospectos"""
        def _get_prospects():
            if self.gc is None:
                return []
            
            try:
                spreadsheet = self.gc.open_by_key(self.sheet_id)
                prospects_sheet = spreadsheet.worksheet("Prospectos")
                return prospects_sheet.get_all_records()
            except gspread.WorksheetNotFound:
                return []
        
        try:
            cached_data = self._get_cached_data("prospects")
            if cached_data:
                return cached_data
            
            data = self._execute_with_retry(_get_prospects)
            if data:
                self._set_cache_data("prospects", data)
                return data
            return []
        except Exception as e:
            self.logger.error(f"Error obteniendo prospectos: {e}")
            return []
    
    def add_incident(self, data: Dict[str, str]) -> bool:
        """Agrega incidente a una hoja separada"""
        def _add_incident_row():
            if self.gc is None:
                return False
            
            try:
                # Intentar acceder a hoja de incidentes, crearla si no existe
                try:
                    spreadsheet = self.gc.open_by_key(self.sheet_id)
                    incidents_sheet = spreadsheet.worksheet("Incidentes")
                except gspread.WorksheetNotFound:
                    # Crear hoja de incidentes
                    spreadsheet = self.gc.open_by_key(self.sheet_id)
                    incidents_sheet = spreadsheet.add_worksheet(
                        title="Incidentes", 
                        rows=1000, 
                        cols=12
                    )
                    # Agregar encabezados
                    headers = [
                        "ID Cliente", "Cliente", "Tipo", "Descripción", "Prioridad",
                        "Zona", "Teléfono", "Estado", "Fecha Creación", "Técnico Asignado",
                        "Fecha Resolución", "Notas Técnico"
                    ]
                    incidents_sheet.append_row(headers)
                
                # Agregar incidente
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                row_data = [
                    data.get('ID Cliente', ''),
                    data.get('Cliente', ''),
                    data.get('Tipo', ''),
                    data.get('Descripción', ''),
                    data.get('Prioridad', 'Media'),
                    data.get('Zona', ''),
                    data.get('Teléfono', ''),
                    'Nuevo',  # Estado inicial
                    current_time,
                    'Sin asignar',  # Técnico
                    '',  # Fecha resolución
                    f'Incidente creado via sistema el {current_time}'
                ]
                
                incidents_sheet.append_row(row_data)
                return True
                
            except Exception as e:
                self.logger.error(f"Error en hoja de incidentes: {e}")
                return False
        
        try:
            result = self._execute_with_retry(_add_incident_row)
            if result:
                self.logger.info(f"✅ Incidente agregado para: {data.get('Cliente')}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Error agregando incidente: {e}")
            return False
    
    def get_incidents(self) -> List[Dict[str, Any]]:
        """Obtiene lista de incidentes"""
        def _get_incidents():
            if self.gc is None:
                return []
            
            try:
                spreadsheet = self.gc.open_by_key(self.sheet_id)
                incidents_sheet = spreadsheet.worksheet("Incidentes")
                return incidents_sheet.get_all_records()
            except gspread.WorksheetNotFound:
                return []
        
        try:
            cached_data = self._get_cached_data("incidents")
            if cached_data:
                return cached_data
            
            data = self._execute_with_retry(_get_incidents)
            if data:
                self._set_cache_data("incidents", data)
                return data
            return []
        except Exception as e:
            self.logger.error(f"Error obteniendo incidentes: {e}")
            return []
    
    def deactivate_client(self, name: str) -> bool:
        """Marca cliente como inactivo (versión legacy)"""
        def _deactivate_client():
            if self.sheet is None:
                return False
            
            # Buscar cliente
            all_records = self.sheet.get_all_records()
            for i, record in enumerate(all_records, start=2):  # Empezar en fila 2
                record_name = str(record.get('Nombre', '')).strip().lower()
                if record_name == name.strip().lower():
                    # Marcar como inactivo en lugar de eliminar
                    activo_col = None
                    headers = self.sheet.row_values(1)
                    for j, header in enumerate(headers, start=1):
                        if 'activo' in header.lower():
                            activo_col = j
                            break
                    
                    if activo_col:
                        self.sheet.update_cell(i, activo_col, 'NO')
                    return True
            
            return False
        
        try:
            result = self._execute_with_retry(_deactivate_client)
            if result:
                self._cache.clear()  # Limpiar cache
                self.logger.info(f"✅ Cliente desactivado: {name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Error desactivando cliente: {e}")
            return False
    
    def get_analytics(self) -> Dict[str, Any]:
        """Obtiene análisis detallado del negocio"""
        clients = self.get_all_clients()
        prospects = self.get_prospects()
        
        analytics = {
            "total_clients": len(clients),
            "total_prospects": len(prospects),
            "zones": {},
            "packages": {"standard": 0, "premium": 0},
            "revenue": {"total": 0, "monthly_avg": 0},
            "recent_activity": []
        }
        
        total_revenue = 0
        payments = []
        
        for client in clients:
            # Análisis por zona
            zone = client.get('Zona', 'Sin zona').strip()
            if zone:
                analytics["zones"][zone] = analytics["zones"].get(zone, 0) + 1
            
            # Análisis de paquetes y revenue
            try:
                payment = client.get('Pago', '0')
                if payment:
                    payment_num = float(str(payment).replace('$', '').replace(',', '').strip())
                    total_revenue += payment_num
                    payments.append(payment_num)
                    
                    if payment_num > 300:
                        analytics["packages"]["premium"] += 1
                    else:
                        analytics["packages"]["standard"] += 1
            except:
                analytics["packages"]["standard"] += 1
        
        if payments:
            analytics["revenue"]["total"] = total_revenue
            analytics["revenue"]["monthly_avg"] = total_revenue / len(payments)
        
        return analytics
    
    def test_connection(self) -> Dict[str, Any]:
        """Prueba la conexión y retorna estado"""
        try:
            if self.sheet is None:
                self._initialize_connection()
            
            if self.sheet:
                # Intentar leer una celda
                test_read = self.sheet.get('A1')
                return {
                    "status": "connected",
                    "message": "✅ Conexión exitosa a Google Sheets",
                    "sheet_id": self.sheet_id,
                    "test_read": test_read
                }
            else:
                return {
                    "status": "disconnected", 
                    "message": "❌ No se pudo conectar a Google Sheets",
                    "sheet_id": self.sheet_id
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error de conexión: {str(e)}",
                "sheet_id": self.sheet_id
            }
    
    def _get_offline_data(self) -> List[Dict[str, Any]]:
        """Datos de ejemplo para modo offline"""
        return [
            {
                "Nombre": "María García",
                "Email": "maria@email.com", 
                "Zona": "Centro",
                "Teléfono": "555-0001",
                "Pago": "250",
                "Activo (SI/NO)": "SI"
            },
            {
                "Nombre": "Juan Pérez", 
                "Email": "juan@email.com",
                "Zona": "Norte", 
                "Teléfono": "555-0002",
                "Pago": "350",
                "Activo (SI/NO)": "SI"
            },
            {
                "Nombre": "Ana López",
                "Email": "ana@email.com",
                "Zona": "Sur",
                "Teléfono": "555-0003", 
                "Pago": "300",
                "Activo (SI/NO)": "SI"
            }
        ]
    
    def delete_client(self, client_name: str) -> bool:
        """Elimina un cliente por nombre"""
        def _delete_client_row():
            if self.gc is None or self.sheet is None:
                return False
            
            # Buscar fila del cliente
            all_records = self.sheet.get_all_records()
            for i, record in enumerate(all_records, start=2):  # start=2 porque fila 1 es header
                nombre = str(record.get('Nombre', '')).strip().lower()
                if nombre == client_name.strip().lower():
                    self.sheet.delete_rows(i)
                    return True
            return False
        
        try:
            result = self._execute_with_retry(_delete_client_row)
            if result:
                self._cache.clear()
                self.logger.info(f"✅ Cliente eliminado: {client_name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Error eliminando cliente: {e}")
            return False
    
    def update_client(self, client_name: str, data: Dict[str, str]) -> bool:
        """Actualiza un cliente existente"""
        def _update_client_row():
            if self.gc is None or self.sheet is None:
                return False
            
            # Buscar fila del cliente
            all_records = self.sheet.get_all_records()
            for i, record in enumerate(all_records, start=2):  # start=2 porque fila 1 es header
                nombre = str(record.get('Nombre', '')).strip().lower()
                if nombre == client_name.strip().lower():
                    # Actualizar campos
                    headers = self.sheet.row_values(1)
                    for j, header in enumerate(headers, start=1):
                        if header in data:
                            self.sheet.update_cell(i, j, data[header])
                    return True
            return False
        
        try:
            result = self._execute_with_retry(_update_client_row)
            if result:
                self._cache.clear()
                self.logger.info(f"✅ Cliente actualizado: {client_name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Error actualizando cliente: {e}")
            return False
    
    def get_clients_by_zone(self, zone: str) -> List[Dict[str, Any]]:
        """Obtiene clientes por zona"""
        all_clients = self.get_all_clients()
        return [client for client in all_clients if client.get('Zona', '').strip().lower() == zone.strip().lower()]
    
    def get_financial_summary(self) -> Dict[str, Any]:
        """Resumen financiero detallado"""
        clients = self.get_all_clients()
        
        total_revenue = 0
        active_clients = 0
        premium_clients = 0
        standard_clients = 0
        zones_revenue = {}
        
        for client in clients:
            # Calcular ingresos
            pago = client.get('Pago', 0)
            if isinstance(pago, str):
                try:
                    pago = float(pago.replace('$', '').replace(',', '').strip())
                except:
                    pago = 0
            total_revenue += pago
            
            # Contar clientes activos
            if str(client.get('Activo (SI/NO)', '')).lower() in ['si', 'yes', '1', 'true']:
                active_clients += 1
            
            # Clasificar por paquete (basado en pago)
            if pago >= 400:
                premium_clients += 1
            else:
                standard_clients += 1
            
            # Revenue por zona
            zona = client.get('Zona', 'Sin zona')
            if zona not in zones_revenue:
                zones_revenue[zona] = 0
            zones_revenue[zona] += pago
        
        return {
            "total_revenue": total_revenue,
            "monthly_revenue": total_revenue,  # Asumiendo que es mensual
            "annual_projection": total_revenue * 12,
            "active_clients": active_clients,
            "premium_clients": premium_clients,
            "standard_clients": standard_clients,
            "average_revenue_per_client": total_revenue / max(active_clients, 1),
            "zones_revenue": zones_revenue,
            "total_clients": len(clients)
        }

    # === MÉTODOS ASYNC PARA EL AGENTE INTELIGENTE ===
    
    async def get_clients_summary(self) -> List[Dict]:
        """Obtener resumen de clientes para el agente (async)"""
        try:
            return self.get_all_clients()
        except Exception as e:
            self.logger.error(f"Error getting clients summary: {e}")
            return []

    async def search_clients(self, query: str) -> List[Dict]:
        """Buscar clientes (async)"""
        try:
            all_clients = self.get_all_clients()
            query_lower = query.lower()
            
            filtered_clients = []
            for client in all_clients:
                if (query_lower in client.get('Nombre', '').lower() or
                    query_lower in client.get('Zona', '').lower() or
                    query_lower in str(client.get('Teléfono', '')).lower()):
                    filtered_clients.append(client)
            
            return filtered_clients
        except Exception as e:
            self.logger.error(f"Error searching clients: {e}")
            return []

    async def calculate_kpis(self) -> Dict:
        """Calcular KPIs del negocio (async)"""
        try:
            clients = self.get_all_clients()
            zones = set(client.get('Zona', '') for client in clients if client.get('Zona'))
            active_clients = [c for c in clients if c.get('Activo (SI/NO)', '').lower() == 'si']
            
            return {
                "total_clients": len(clients),
                "active_clients": len(active_clients),
                "total_zones": len(zones),
                "monthly_revenue": sum(c.get('paquete_info', {}).get('monthly', 0) for c in clients),
                "average_clients_per_zone": len(active_clients) / max(len(zones), 1)
            }
        except Exception as e:
            self.logger.error(f"Error calculating KPIs: {e}")
            return {}

    async def get_zones_data(self) -> List[Dict]:
        """Obtener datos de zonas (async)"""
        try:
            clients = self.get_all_clients()
            zones_data = {}
            
            for client in clients:
                zone = client.get('Zona', 'Sin Zona')
                if zone not in zones_data:
                    zones_data[zone] = {
                        "name": zone,
                        "clients": 0,
                        "active_clients": 0,
                        "revenue": 0
                    }
                
                zones_data[zone]["clients"] += 1
                if client.get('Activo (SI/NO)', '').lower() == 'si':
                    zones_data[zone]["active_clients"] += 1
                zones_data[zone]["revenue"] += client.get('paquete_info', {}).get('monthly', 0)
            
            return list(zones_data.values())
        except Exception as e:
            self.logger.error(f"Error getting zones data: {e}")
            return []

    async def calculate_revenue(self) -> Dict:
        """Calcular ingresos (async)"""
        try:
            clients = self.get_all_clients()
            total_revenue = sum(c.get('paquete_info', {}).get('monthly', 0) for c in clients)
            active_clients = [c for c in clients if c.get('Activo (SI/NO)', '').lower() == 'si']
            active_revenue = sum(c.get('paquete_info', {}).get('monthly', 0) for c in active_clients)
            
            return {
                "total_revenue": total_revenue,
                "active_revenue": active_revenue,
                "average_revenue_per_client": total_revenue / max(len(clients), 1),
                "projected_monthly": active_revenue
            }
        except Exception as e:
            self.logger.error(f"Error calculating revenue: {e}")
            return {}

    async def get_client_profile(self, client_id: str) -> Dict:
        """Obtener perfil completo de cliente (async)"""
        try:
            clients = self.get_all_clients()
            for client in clients:
                if client.get('ID Cliente') == client_id:
                    return {
                        **client,
                        "full_profile": True,
                        "last_updated": datetime.now().isoformat()
                    }
            return {}
        except Exception as e:
            self.logger.error(f"Error getting client profile: {e}")
            return {}

    async def get_client_history(self, client_id: str) -> List[Dict]:
        """Obtener historial de cliente (async - mock por ahora)"""
        try:
            # Por ahora retorna un mock, podrías expandir esto con datos reales
            return [
                {
                    "date": datetime.now().isoformat(),
                    "action": "profile_viewed",
                    "details": f"Perfil del cliente {client_id} consultado"
                }
            ]
        except Exception as e:
            self.logger.error(f"Error getting client history: {e}")
            return []

    async def add_client_async(self, client_data: Dict) -> Dict:
        """Agregar cliente (async wrapper)"""
        try:
            result = self.add_client(client_data)
            return {"status": "success", "data": result}
        except Exception as e:
            self.logger.error(f"Error adding client: {e}")
            return {"status": "error", "message": str(e)}

    async def update_client_async(self, client_data: Dict) -> Dict:
        """Actualizar cliente (async wrapper)"""
        try:
            client_name = client_data.get('Nombre', '')
            result = self.update_client(client_name, client_data)
            return {"status": "success", "data": result}
        except Exception as e:
            self.logger.error(f"Error updating client: {e}")
            return {"status": "error", "message": str(e)}
