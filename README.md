# Red Soluciones ISP v2.0 🚀

Sistema completo de gestión para proveedores de servicios de internet (ISP) con inteligencia artificial integrada.

## 📁 Estructura del Proyecto (Organizada)

```
redsoluciones/
├── 📁 backend/                    # Backend principal
│   └── app/
│       ├── main.py                # ✅ Aplicación FastAPI principal
│       ├── core/                  # Configuración del sistema
│       │   ├── config_unified.py  # Configuración unificada
│       │   ├── config.py          # Wrapper de configuración
│       │   ├── user_auth.py       # Sistema de autenticación
│       │   ├── security.py        # Configuración de seguridad
│       │   ├── error_handlers.py  # Manejo centralizado de errores
│       │   └── versions/          # Versiones anteriores de configuración
│       ├── services/              # Servicios de negocio
│       │   ├── consolidated_agent.py    # Agente IA unificado
│       │   ├── context_engine.py        # Motor de contexto
│       │   └── sheets/
│       │       └── service.py           # Servicio Google Sheets
│       ├── utils/                 # Utilidades del sistema
│       │   ├── logger.py          # Sistema de logging unificado
│       │   └── versions/          # Versiones anteriores
│       └── versions/              # Versiones anteriores del main
│
├── 📁 frontend/                   # Interfaz de usuario
│   ├── index.html                 # ✅ Dashboard principal
│   ├── assets/                    # Recursos estáticos
│   │   ├── css/                   # Estilos
│   │   ├── js/                    # JavaScript
│   │   └── logo-red-soluciones.png
│   └── versions/                  # Versiones anteriores del frontend
│
├── 📁 api/                       # Gateway para Vercel
│   ├── index.py                  # ✅ Entry point para Vercel
│   └── telegram_webhook.py       # Webhook de Telegram
│
├── 📁 scripts/                   # Scripts de utilidad
│   ├── analyze_clients.py        # Análisis de clientes
│   ├── verificar_google_sheets.py # Verificación de Google Sheets
│   └── ...                       # Otros scripts de utilidad
│
├── 📁 docs/                      # Documentación
│   └── archived/                 # Documentación archivada
│
├── 📁 logs/                      # Archivos de log
├── 📁 archive/                   # Código archivado
├── 📁 improvements/              # Mejoras y características adicionales
│
├── app.py                        # ✅ Entry point unificado
├── vercel.json                   # Configuración de Vercel
├── requirements.txt              # Dependencias Python
├── .env                          # Variables de entorno
└── README.md                     # Este archivo
```

## ✨ Características Principales

- 🤖 **Agente IA Consolidado**: Un solo agente inteligente que maneja todas las consultas
- 📊 **Google Sheets Integration**: Conexión directa con hojas de cálculo
- 🔐 **Autenticación Simple**: Sin contraseñas, solo para propietarios autorizados
- 📱 **API RESTful**: 41+ endpoints para todas las operaciones
- 🎨 **Dashboard Moderno**: Interfaz web responsive
- 🚀 **Deploy Ready**: Configurado para Vercel y otros servicios

## 🛠️ Instalación

### Prerrequisitos
- Python 3.9+
- Cuenta de Google Cloud con Sheets API habilitada
- Service Account JSON key

### Configuración Rápida

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Scaie024/redsoluciones.git
cd redsoluciones
```

2. **Crear entorno virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar credenciales:**
```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar .env con tus valores
GOOGLE_SHEET_ID=tu_sheet_id_aqui
GEMINI_API_KEY=tu_api_key_aqui  # Opcional
```

5. **Agregar service account:**
- Descargar `service_account.json` desde Google Cloud Console
- Colocarlo en la raíz del proyecto
- Compartir tu Google Sheet con el email del service account

6. **Iniciar servidor:**
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8004 --reload
```

## 🎯 Uso

### Dashboard Web
Visita: `http://localhost:8004/dashboard.html`

### API Endpoints
- **Health Check**: `GET /health`
- **Chat IA**: `POST /api/chat`
- **Clientes**: `GET /api/clients`
- **Dashboard**: `GET /api/dashboard`
- **Documentación**: `http://localhost:8004/docs`

### Ejemplo de Chat
```bash
curl -X POST "http://localhost:8004/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cuántos clientes tenemos?",
    "user_id": "admin",
    "session_id": "session123"
  }'
```

## 📁 Estructura del Proyecto

```
redsoluciones/
├── backend/
│   └── app/
│       ├── main.py                 # FastAPI application
│       ├── core/
│       │   ├── config_unified.py   # Configuración principal
│       │   └── user_auth.py        # Autenticación
│       └── services/
│           ├── consolidated_agent.py  # Agente IA principal
│           └── sheets/
│               └── service.py      # Google Sheets service
├── frontend/
│   ├── dashboard.html             # Dashboard principal
│   └── assets/                    # CSS, JS, imágenes
├── api/
│   └── index.py                   # Vercel entry point
├── .env                           # Configuración
├── service_account.json           # Credenciales Google
└── requirements.txt               # Dependencias Python
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# OBLIGATORIAS
GOOGLE_SHEET_ID=1ABC123...         # ID de tu Google Sheet

# OPCIONALES
GEMINI_API_KEY=AIza...             # Para funciones IA avanzadas
TELEGRAM_BOT_TOKEN=123:ABC...      # Para bot de Telegram
HOST=0.0.0.0                       # Host del servidor
PORT=8004                          # Puerto del servidor
DEBUG=false                        # Modo debug
```

### Google Sheets Setup
1. Crear proyecto en Google Cloud Console
2. Habilitar Google Sheets API
3. Crear Service Account
4. Descargar JSON key
5. Compartir Sheet con service account email
6. Estructura requerida:
   - Hoja `01_Clientes`
   - Hoja `02_Prospectos`
   - Hoja `03_Incidentes`

## 🚀 Deploy

### Vercel (Recomendado)
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker
```bash
# Construir imagen
docker build -t red-soluciones .

# Ejecutar
docker run -p 8004:8004 red-soluciones
```

### Tradicional
```bash
# Usar gunicorn para producción
pip install gunicorn
gunicorn backend.app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🔍 Verificación

Ejecutar script de verificación:
```bash
python verification_v2.py
```

## 📊 Métricas del Sistema

- **534+ Clientes** gestionados
- **41+ API Endpoints** disponibles
- **7 Agentes → 1** (85% reducción complejidad)
- **100% Funcionalidad** preservada
- **Sub-2s** tiempo respuesta promedio

## 🤝 Contribuir

1. Fork el proyecto
2. Crear branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/Scaie024/redsoluciones/issues)
- **Email**: [Contacto directo]
- **Documentación**: [Wiki del proyecto]

## 🎖️ Agradecimientos

- Equipo Red Soluciones ISP
- Comunidad Python/FastAPI
- Google Cloud Platform

---

**Red Soluciones ISP v2.0** - Construido con ❤️ para la gestión empresarial moderna.
