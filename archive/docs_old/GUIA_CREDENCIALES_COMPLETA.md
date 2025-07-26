# 🔐 CONFIGURACIÓN AUTOMÁTICA DE CREDENCIALES
## Red Soluciones ISP - Sistema Completo

### 🎯 **LO QUE NECESITAS PARA DEPLOY COMPLETO**

Para que tu sistema **siempre funcione al 100%** en cualquier entorno, necesitas configurar estas credenciales:

## 📋 **CREDENCIALES ESENCIALES**

### 🔑 **1. Google Sheets ID**
- **Qué es**: ID de tu hoja de Google Sheets donde se guardan los datos
- **Cómo obtenerlo**: De la URL de tu hoja: `docs.google.com/spreadsheets/d/[ESTE_ID]/edit`
- **Ejemplo**: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

### 🤖 **2. Gemini AI API Key**  
- **Qué es**: Clave para el chat inteligente con IA
- **Cómo obtenerla**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Ejemplo**: `AIzaSyC-tu_api_key_aqui`

### 📄 **3. Service Account JSON**
- **Qué es**: Credenciales de Google para acceder a Sheets
- **Cómo obtenerlo**: [Google Cloud Console](https://console.cloud.google.com/) > Service Accounts
- **Archivo**: `service_account.json` en la raíz del proyecto

---

## ⚡ **CONFIGURACIÓN AUTOMÁTICA**

### 🚀 **Opción 1: Script Automático (RECOMENDADO)**

```bash
# Configuración y deploy en un solo comando
./deploy.sh
```

### 🔧 **Opción 2: Configuración Manual**

```bash
# 1. Configurar credenciales interactivamente
python3 configurar_credenciales.py

# 2. Verificar configuración
python3 verificar_credenciales.py

# 3. Iniciar servidor
python3 app.py
```

### 📝 **Opción 3: Editar .env directamente**

```bash
# Copiar plantilla
cp .env.example .env

# Editar con tus valores reales
nano .env
```

---

## 🌐 **CONFIGURACIÓN POR PLATAFORMA**

### 💻 **Desarrollo Local**
```bash
# Archivo .env (crear en la raíz)
GOOGLE_SHEET_ID=tu_sheet_id_real
GEMINI_API_KEY=tu_gemini_api_key
ENVIRONMENT=development
DEBUG=true
PORT=8004
```

### ☁️ **Vercel (Producción)**
```bash
# Método 1: Automático con deploy.sh
./deploy.sh  # Seleccionar opción 2

# Método 2: Manual
vercel env add GOOGLE_SHEET_ID production
vercel env add GEMINI_API_KEY production
vercel env add ENVIRONMENT production
vercel deploy --prod
```

### 🏗️ **Heroku**
```bash
# Configurar variables
heroku config:set GOOGLE_SHEET_ID=tu_sheet_id
heroku config:set GEMINI_API_KEY=tu_api_key
heroku config:set ENVIRONMENT=production
heroku config:set DEBUG=false

# Deploy
git push heroku main
```

### 🐳 **Docker**
```bash
# Variables en docker-compose.yml
environment:
  - GOOGLE_SHEET_ID=tu_sheet_id
  - GEMINI_API_KEY=tu_api_key
  - ENVIRONMENT=production
```

---

## 🛠️ **HERRAMIENTAS INCLUIDAS**

### 📊 **Scripts Disponibles**

| Script | Descripción | Uso |
|--------|-------------|-----|
| `deploy.sh` | Deploy automático completo | `./deploy.sh` |
| `configurar_credenciales.py` | Configuración interactiva | `python3 configurar_credenciales.py` |
| `verificar_credenciales.py` | Verificar configuración | `python3 verificar_credenciales.py` |
| `app.py` | Iniciar servidor | `python3 app.py` |

### 🔍 **Verificación Rápida**

```bash
# Verificar que todo está OK
python3 -c "
from backend.app.core.config import settings
print(f'✅ {settings.PROJECT_NAME} v{settings.VERSION}')
print(f'📊 Sheet: {settings.GOOGLE_SHEET_ID[:10] if settings.GOOGLE_SHEET_ID else \"❌\"}...')
print(f'🤖 Gemini: {\"✅\" if settings.GEMINI_API_KEY else \"❌\"}')
print(f'🌍 Env: {settings.ENVIRONMENT}')
"
```

---

## 🔐 **SEGURIDAD**

### ❌ **NO subir a Git:**
```gitignore
.env
.env.local
.env.production
service_account.json
*.log
```

### ✅ **SÍ subir a Git:**
```
.env.example
.gitignore
deploy.sh
configurar_credenciales.py
verificar_credenciales.py
```

---

## 🆘 **SOLUCIÓN DE PROBLEMAS**

### **❌ "Address already in use"**
```bash
# Cambiar puerto
PORT=8005 python3 app.py

# O matar procesos
lsof -ti:8004 | xargs kill
```

### **❌ "GEMINI_API_KEY no configurada"**
```bash
# Configurar en .env
echo "GEMINI_API_KEY=tu_api_key_aqui" >> .env
```

### **❌ "No se pudo inicializar la hoja"**
```bash
# Verificar Sheet ID y permisos
python3 verificar_credenciales.py
```

---

## ✅ **CONFIGURACIÓN MÍNIMA PARA FUNCIONAR AL 100%**

```bash
# .env (archivo real)
GOOGLE_SHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
GEMINI_API_KEY=AIzaSyC-tu_api_key_real_aqui
ENVIRONMENT=production
DEBUG=false
PORT=8004
SECRET_KEY=tu-secret-key-super-segura
```

**Con esta configuración, tu sistema Red Soluciones ISP funcionará al 100% en cualquier entorno.** 🚀

---

## 🎯 **INICIO RÁPIDO - 3 PASOS**

```bash
# 1. Clone y entra al directorio
git clone tu-repo
cd redsoluciones

# 2. Configuración automática
./deploy.sh

# 3. ¡Listo! Tu sistema está funcionando
```

**🏆 ¡Tu Red Soluciones ISP está lista para producción!**
