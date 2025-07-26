# Red Soluciones ISP - Sistema Consolidado

## 🎯 Resumen de Consolidación

El proyecto ha sido **simplificado y unificado** para eliminar redundancias y crear una estructura coherente.

## 📁 Estructura Principal Consolidada

```
/
├── backend/app/main.py          # ⭐ APLICACIÓN PRINCIPAL (única fuente de verdad)
├── api/index.py                 # Gateway para Vercel (importa desde backend)
├── app.py                       # Entry point unificado (importa desde backend)
├── run_dev.py                   # 🚀 Script de desarrollo (RECOMENDADO)
├── start_server.py              # Script alternativo de producción
└── frontend/                    # Frontend estático
```

## 🚀 Cómo Ejecutar el Sistema

### Desarrollo Local (RECOMENDADO)
```bash
python run_dev.py
```

### Alternativas
```bash
# Usando app.py
python app.py

# Usando start_server.py
python start_server.py

# Con uvicorn directamente
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🏗️ Arquitectura Unificada

### Punto de Entrada Único
- **`backend/app/main.py`** es la única definición de la aplicación FastAPI
- Todos los demás archivos simplemente **importan** la app desde ahí
- No hay duplicación de rutas, middlewares o configuración

### Configuración Centralizada
- **`backend/app/core/config_unified.py`** contiene toda la configuración
- **`backend/app/core/config.py`** re-exporta la configuración unificada
- Variables de entorno manejadas en un solo lugar

### Servicios
- **Google Sheets**: `backend/app/services/sheets/service.py`
- **Agente Carlos**: `backend/app/services/smart_agent.py`
- **Logging**: `backend/app/utils/logger.py`

## 🌐 URLs del Sistema

Cuando ejecutes el servidor, estará disponible en:

- **Dashboard**: http://localhost:8000/
- **API Health**: http://localhost:8000/health
- **API Chat**: http://localhost:8000/api/chat
- **API Clients**: http://localhost:8000/api/clients
- **API Stats**: http://localhost:8000/api/dashboard

## ⚙️ Configuración de Variables de Entorno

```bash
# Opcional - si no se configuran, usa valores por defecto
export GOOGLE_SHEET_ID="1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ"
export GEMINI_API_KEY="tu_clave_de_gemini"
export TELEGRAM_BOT_TOKEN="tu_token_de_telegram"
export DEBUG="True"
```

## 🚀 Despliegue

### Vercel (RECOMENDADO)
- **Entry Point**: `api/index.py`
- **Configuración**: `vercel.json`
- La aplicación en Vercel ejecuta la misma app de `backend/app/main.py`

### Heroku (Alternativo)
- **Entry Point**: `run_server.py`
- **Configuración**: `Procfile`

## ✅ Beneficios de la Consolidación

1. **Sin Duplicación**: Una sola definición de la aplicación FastAPI
2. **Mantenimiento Simple**: Cambios en un solo lugar
3. **Coherencia**: Mismo comportamiento en desarrollo y producción
4. **Claridad**: Fácil entender qué archivo hace qué
5. **Menos Errores**: No hay conflictos entre versiones duplicadas

## 🛠️ Desarrollo

Para modificar la aplicación:

1. **Rutas API**: Edita `backend/app/main.py`
2. **Configuración**: Edita `backend/app/core/config_unified.py`
3. **Agente Carlos**: Edita `backend/app/services/smart_agent.py`
4. **Frontend**: Edita archivos en `frontend/`

## 🔍 Verificación

Puedes verificar que todo funciona:

```bash
# Probar la API
curl http://localhost:8000/health

# Probar el chat con Carlos
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hola carlos"}'
```

## ⚠️ Notas Importantes

- **GEMINI_API_KEY**: Necesaria para funcionalidad completa del agente Carlos
- **Google Sheets**: El archivo `service_account.json` debe estar en la raíz del proyecto
- **Puerto 8000**: Es el puerto por defecto, asegúrate de que esté libre

---
**Sistema consolidado el 25 de julio de 2025** ✅
