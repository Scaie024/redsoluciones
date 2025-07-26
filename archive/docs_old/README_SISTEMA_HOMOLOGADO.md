# 🚀 Red Soluciones ISP v4.0 Homologado

## Sistema Empresarial Completo con IA Integrada

Red Soluciones ISP v4.0 es un sistema empresarial completamente homologado que integra Google Sheets como backend, IA empresarial con Gemini, y un dashboard reactivo en tiempo real.

---

## 🎯 **Características Principales**

### ✅ **Backend Google Sheets Unificado**
- **Context Engine**: Motor de contexto que mapea TODAS las hojas del Google Sheets
- **Sincronización inteligente**: Actualización automática y cache con invalidación selectiva
- **Relaciones automáticas**: Mapeo de relaciones entre clientes, incidentes, zonas, etc.
- **Filtrado por propietario**: Datos automáticamente filtrados para Eduardo y Omar

### 🤖 **IA Empresarial Avanzada**
- **Enhanced AI Agent**: Agente IA que comprende completamente el contexto del negocio
- **Respuestas contextuales**: Utiliza datos reales del Google Sheets para respuestas precisas
- **Acciones ejecutables**: Puede realizar operaciones directamente en el sistema
- **Insights automáticos**: Genera análisis y recomendaciones de negocio

### 📊 **Dashboard Reactivo**
- **Métricas en tiempo real**: KPIs actualizados automáticamente
- **Personalización por usuario**: Dashboard específico para Eduardo y Omar
- **Widgets inteligentes**: Componentes que se actualizan según el contexto
- **Insights visuales**: Gráficos y análisis automáticos

### 🔐 **Sistema de Autenticación**
- **Reconocimiento automático**: Identificación entre Eduardo y Omar
- **Contexto personalizado**: Datos filtrados según el propietario
- **Permisos granulares**: Control de acceso por usuario y módulo
- **Sesiones persistentes**: Mantiene la sesión entre recargas

---

## 🏗️ **Arquitectura del Sistema**

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND REACTIVO                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │    Dashboard    │  │   Chat con IA   │  │  Gestión    │  │
│  │   Inteligente   │  │   Empresarial   │  │  Usuarios   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND HOMOLOGADO                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │ Enhanced Agent  │  │ Context Engine  │  │  FastAPI    │  │
│  │  (IA Gemini)    │  │ (Contexto Real) │  │  Server     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  GOOGLE SHEETS BACKEND                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Clientes   │  │ Prospectos  │  │    Incidentes       │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Estadísticas│  │    Zonas    │  │   Propietarios      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 **Instalación y Configuración**

### **1. Requisitos del Sistema**
```bash
Python 3.8+
Google Sheets API habilitada
Cuenta de servicio de Google configurada
```

### **2. Variables de Entorno**
Crear archivo `.env` en la raíz del proyecto:

```env
# CONFIGURACIÓN PRINCIPAL
GOOGLE_SHEET_ID=tu_id_de_google_sheets
GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json

# IA (OPCIONAL)
GEMINI_API_KEY=tu_api_key_de_gemini

# SERVIDOR
PORT=8004
DEBUG=false
ENVIRONMENT=production

# TELEGRAM (OPCIONAL)
TELEGRAM_BOT_TOKEN=tu_token_de_telegram
```

### **3. Instalación de Dependencias**
```bash
pip install -r requirements.txt
```

### **4. Configuración de Google Sheets**
1. Crear proyecto en Google Cloud Console
2. Habilitar Google Sheets API
3. Crear cuenta de servicio
4. Descargar archivo `service_account.json`
5. Compartir Google Sheets con email de la cuenta de servicio

---

## 💻 **Uso del Sistema**

### **Ejecución Básica**
```bash
# Ejecutar sistema completo
python run_homologated_system.py

# Modo desarrollo (hot reload)
python run_homologated_system.py --dev

# Puerto personalizado
python run_homologated_system.py --port 8005

# Solo verificar configuración
python run_homologated_system.py --check
```

### **Inicialización Completa**
```bash
# Inicializar sistema completo
python init_homologated_system.py

# Solo verificar configuración
python init_homologated_system.py --check-only

# Limpiar cache y reinicializar
python init_homologated_system.py --reset-cache
```

### **Acceso al Sistema**
- **Dashboard Principal**: `http://localhost:8004`
- **API v2**: `http://localhost:8004/api/v2/`
- **Estado del Sistema**: `http://localhost:8004/api/v2/system/status`

---

## 🎯 **Funcionalidades Empresariales**

### **1. Gestión de Clientes**
- ✅ Vista completa de cartera de clientes
- ✅ Filtrado automático por propietario (Eduardo/Omar)
- ✅ Búsqueda inteligente con IA
- ✅ Relaciones con incidentes y zonas

### **2. Pipeline de Prospectos**
- ✅ Gestión completa de leads
- ✅ Seguimiento de conversión
- ✅ Probabilidades automáticas
- ✅ Asignación por zona

### **3. Gestión de Incidentes**
- ✅ Sistema de tickets completo
- ✅ Priorización automática
- ✅ Asignación de técnicos
- ✅ Escalamiento por tiempo

### **4. Analytics Empresarial**
- ✅ KPIs en tiempo real
- ✅ Métricas por propietario
- ✅ Análisis de churn y crecimiento
- ✅ Predicciones con IA

### **5. Chat IA Empresarial**
- ✅ Comprende todo el contexto del negocio
- ✅ Respuestas con datos reales
- ✅ Acciones ejecutables
- ✅ Sugerencias inteligentes

---

## 🧠 **Capacidades de IA**

### **Consultas Inteligentes**
```
❓ "¿Cuántos clientes tiene Eduardo?"
✅ "Eduardo tiene 45 clientes activos, generando $12,350/mes"

❓ "Incidentes de alta prioridad"  
✅ "3 incidentes críticos: Conexión cliente García (Zona Norte), 
    Servicio intermitente López (Zona Sur)..."

❓ "Estado del negocio este mes"
✅ "Crecimiento +8%, ARPU $32.50, Churn 3.2% - 
    Excelente rendimiento vs objetivo"
```

### **Insights Automáticos**
- 🔍 **Análisis de patrones**: Detecta tendencias en datos
- ⚠️ **Alertas proactivas**: Identifica problemas antes que escaliden
- 💡 **Oportunidades de negocio**: Sugiere acciones para crecimiento
- 📈 **Predicciones**: Estima crecimiento y métricas futuras

---

## 📊 **Estructura de Google Sheets**

### **Hoja "Clientes"**
| ID | Nombre | Plan | Estado | Zona | Propietario | Pago_Mensual |
|----|--------|------|--------|------|-------------|--------------|
| 1  | García | Premium | Activo | Norte | Eduardo | 45.00 |

### **Hoja "Prospectos"** 
| ID | Nombre | Telefono | Estado | Propietario | Probabilidad |
|----|--------|----------|--------|-------------|--------------|
| 1  | López | 555-0123 | Interesado | Omar | 70% |

### **Hoja "Incidentes"**
| ID | Cliente_ID | Tipo | Estado | Prioridad | Propietario |
|----|------------|------|--------|-----------|-------------|
| 1  | 1 | Técnico | Abierto | Alta | Eduardo |

### **Hojas Adicionales**
- 📈 **Estadísticas**: KPIs históricos y métricas
- 🏠 **Zonas**: Sectores geográficos de cobertura  
- 👥 **Propietarios**: Configuración de Eduardo y Omar

---

## 🔧 **API Endpoints v2**

### **Sistema**
```
GET  /api/v2/system/status              # Estado del sistema
POST /api/v2/system/refresh             # Refrescar datos
```

### **Contexto**
```
GET  /api/v2/context/{propietario}      # Contexto completo del usuario
GET  /api/v2/dashboard/{propietario}    # Dashboard personalizado
```

### **IA y Chat**
```
POST /api/v2/chat/enhanced              # Chat con IA empresarial
GET  /api/v2/insights/{propietario}     # Insights automáticos
```

### **Búsqueda**
```
GET  /api/v2/entities/search?q=...      # Búsqueda avanzada
```

---

## 🐛 **Debugging y Logs**

### **Logs del Sistema**
```bash
# Ver logs en tiempo real
tail -f logs/redsoluciones_homologado.log

# Logs por fecha
ls logs/redsol_*.log
```

### **Debug del Context Engine**
```python
# Verificar estado del cache
GET /api/v2/system/status

# Limpiar cache manualmente
POST /api/v2/system/refresh
```

### **Debug del Enhanced Agent**
```python
# Probar agente IA directamente
POST /api/v2/chat/enhanced
{
  "message": "debug: estado del sistema",
  "user_name": "Eduardo"
}
```

---

## 🚨 **Troubleshooting**

### **Problema: "Context Engine no disponible"**
```bash
# Verificar configuración
python run_homologated_system.py --check

# Reinicializar sistema
python init_homologated_system.py --reset-cache
```

### **Problema: "Google Sheets no accesible"**
1. Verificar `GOOGLE_SHEET_ID` en `.env`
2. Confirmar permisos de `service_account.json`
3. Compartir hoja con email de cuenta de servicio

### **Problema: "IA no disponible"**
1. Configurar `GEMINI_API_KEY` en `.env`
2. Verificar cuota de API de Gemini
3. Sistema funciona sin IA (funcionalidad limitada)

---

## 📈 **Roadmap y Mejoras**

### **v4.1 - Próximas Funcionalidades**
- [ ] Dashboard móvil responsivo
- [ ] Notificaciones push en tiempo real
- [ ] Integración con WhatsApp Business
- [ ] Reportes automatizados por email

### **v4.2 - IA Avanzada**
- [ ] Predicciones de churn por cliente
- [ ] Recomendaciones de precios dinámicas
- [ ] Chatbot para clientes
- [ ] Análisis de sentimientos

### **v5.0 - Expansión**
- [ ] Multi-tenant para otras ISPs
- [ ] Integración con sistemas de facturación
- [ ] App móvil nativa
- [ ] API pública para integraciones

---

## 🤝 **Contribución y Soporte**

### **Estructura del Proyecto**
```
red-soluciones-isp/
├── backend/
│   ├── app/
│   │   ├── core/                 # Configuración central
│   │   ├── services/             # Servicios principales
│   │   │   ├── context_engine.py # Motor de contexto
│   │   │   ├── enhanced_agent.py # IA empresarial
│   │   │   └── sheets/           # Google Sheets
│   │   └── utils/                # Utilidades
├── frontend/
│   ├── assets/
│   │   ├── js/
│   │   │   ├── enhanced-system.js # Sistema homologado
│   │   │   └── new-script.js      # Legacy
│   │   └── css/
│   └── index.html                # Dashboard principal
├── logs/                         # Logs del sistema
├── init_homologated_system.py    # Inicializador
├── run_homologated_system.py     # Ejecutor principal
└── requirements.txt              # Dependencias
```

### **Contacto**
- 📧 **Email**: soporte@redsoluciones.com
- 💬 **Chat**: Sistema integrado en dashboard
- 📱 **Telegram**: Bot empresarial (si configurado)

---

## 📄 **Licencia**

Copyright © 2025 Red Soluciones ISP. Todos los derechos reservados.

Sistema empresarial desarrollado específicamente para Red Soluciones ISP con tecnología homologada y IA integrada.

---

**🎉 ¡Disfruta de tu sistema empresarial completamente homologado!**
