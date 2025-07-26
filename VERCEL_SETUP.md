# CONFIGURACIÓN PARA VERCEL - Red Soluciones ISP

## Variables de Entorno Requeridas:

### 🔑 API Keys (Reemplaza con tus valores reales):

GEMINI_API_KEY=AIzaSyDummy_Key_Replace_With_Real_One
TELEGRAM_BOT_TOKEN=1234567890:AAEDummy_Token_Replace_With_Real_One

### 📄 Google Credentials (Opcional - para Google Sheets):
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"your-project","private_key_id":"123","private_key":"-----BEGIN PRIVATE KEY-----\nDUMMY\n-----END PRIVATE KEY-----\n","client_email":"dummy@your-project.iam.gserviceaccount.com","client_id":"123","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/dummy%40your-project.iam.gserviceaccount.com"}

## 🚀 Instrucciones de Despliegue:

1. Ve a https://vercel.com
2. Conecta tu repositorio: Scaie024/redsoluciones  
3. En Environment Variables, agrega las variables de arriba con TUS valores reales
4. ¡Deploy automático!

## 📱 URLs después del despliegue:
- API Principal: https://tu-proyecto.vercel.app/
- Estado: https://tu-proyecto.vercel.app/api/status
- Salud: https://tu-proyecto.vercel.app/health

## 🔧 Funcionalidades Activas:
✅ FastAPI con fallback automático
✅ Manejo de errores robusto  
✅ Google Credentials automático
✅ Variables de entorno flexibles
✅ Endpoints de diagnóstico

## ⚠️ IMPORTANTE:
- Reemplaza las claves DUMMY con tus valores reales
- El sistema funcionará incluso si faltan algunas variables
- Los logs te dirán qué servicios están activos
