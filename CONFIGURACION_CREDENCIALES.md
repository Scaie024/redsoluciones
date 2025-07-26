# 🔐 GUÍA COMPLETA DE CONFIGURACIÓN DE CREDENCIALES
## Red Soluciones ISP - Configuración para Producción

### 📋 **PASO 1: Variables de Entorno Esenciales**

Para que el sistema funcione completamente necesitas configurar estas credenciales:

#### **🔑 Variables Obligatorias:**

```bash
# 1. Google Sheets ID (tu hoja de datos)
GOOGLE_SHEET_ID=1ABC123_tu_sheet_id_real_aqui

# 2. Gemini AI API Key (para chat inteligente)
GEMINI_API_KEY=AIzaSyC-tu_api_key_gemini_aqui

# 3. Configuración de entorno
ENVIRONMENT=production
DEBUG=false
```

---

### 🛠️ **PASO 2: Cómo Obtener las Credenciales**

#### **📊 Google Sheets ID:**
1. Abre tu Google Sheet
2. Copia el ID de la URL: `https://docs.google.com/spreadsheets/d/[ESTE_ES_EL_ID]/edit`
3. Ejemplo: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

#### **🤖 Gemini AI API Key:**
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea un nuevo proyecto o usa uno existente
3. Genera una API Key
4. Copia la clave (formato: `AIzaSyC...`)

#### **📋 Service Account JSON:**
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un Service Account
3. Descarga el archivo JSON
4. Guárdalo como `service_account.json` en la raíz del proyecto

---

### 🚀 **PASO 3: Configuración por Plataforma**

#### **💻 Desarrollo Local:**
```bash
# Crear archivo .env en la raíz
cp .env.example .env

# Editar .env con tus valores reales
GOOGLE_SHEET_ID=tu_sheet_id_real
GEMINI_API_KEY=tu_api_key_real
ENVIRONMENT=development
DEBUG=true
```

#### **🌐 Vercel (Producción):**
```bash
# Configurar variables en Vercel Dashboard
vercel env add GOOGLE_SHEET_ID
vercel env add GEMINI_API_KEY  
vercel env add ENVIRONMENT production
vercel env add DEBUG false

# O usar CLI
vercel env add GOOGLE_SHEET_ID production
# Pegar tu Sheet ID cuando pregunte
```

#### **🏗️ Heroku:**
```bash
# Configurar variables en Heroku
heroku config:set GOOGLE_SHEET_ID=tu_sheet_id
heroku config:set GEMINI_API_KEY=tu_api_key
heroku config:set ENVIRONMENT=production
heroku config:set DEBUG=false
```

---

### 📁 **PASO 4: Estructura de Archivos de Credenciales**

```
proyecto/
├── .env                    # Variables locales (NO subir a git)
├── .env.example           # Plantilla (SÍ subir a git)
├── service_account.json   # Credenciales Google (NO subir a git)
└── .gitignore            # Debe incluir .env y *.json
```

---

### 🔐 **PASO 5: Seguridad - .gitignore**

Asegúrate de que estos archivos NO se suban a git:

```gitignore
# Variables de entorno
.env
.env.local
.env.production

# Credenciales
service_account.json
*.json

# Logs
*.log
server*.log
```

---

### ✅ **PASO 6: Verificación**

Para verificar que todo está configurado:

```bash
# Ejecutar verificación
python -c "
from backend.app.core.config import settings
print('✅ Configuración:')
print(f'  Sheet ID: {settings.GOOGLE_SHEET_ID[:10]}...')
print(f'  Gemini: {'✅' if settings.GEMINI_API_KEY else '❌'}')
print(f'  Environment: {settings.ENVIRONMENT}')
"
```

---

### 🆘 **SOLUCIÓN DE PROBLEMAS**

**❌ "GEMINI_API_KEY no configurada"**
- Configura la variable de entorno GEMINI_API_KEY
- Verifica que la API key sea válida

**❌ "No se pudo inicializar la hoja"**
- Verifica que GOOGLE_SHEET_ID sea correcto
- Asegúrate de que service_account.json existe
- Comparte la hoja con el email del service account

**❌ "Address already in use"**
- Cambia el puerto: `PORT=8005`
- O mata procesos: `lsof -ti:8004 | xargs kill`

---

### 🎯 **CONFIGURACIÓN MÍNIMA PARA PRODUCCIÓN**

```bash
# .env (archivo real - NO subir a git)
GOOGLE_SHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
GEMINI_API_KEY=AIzaSyC-tu_api_key_real_aqui
ENVIRONMENT=production
DEBUG=false
PORT=8004
SECRET_KEY=tu-secret-key-super-segura-para-production
```

Con esta configuración, tu sistema funcionará al 100% en cualquier entorno.
