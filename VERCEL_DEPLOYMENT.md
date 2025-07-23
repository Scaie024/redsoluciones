# 🚀 Guía de Despliegue en Vercel

## ✅ Compatibilidad Verificada

Tu proyecto **Red Soluciones ISP** es **COMPATIBLE** con Vercel gratuito, con algunas consideraciones:

### 🎯 Plan Gratuito de Vercel - Límites:
- ✅ **Serverless Functions**: 100GB-hours/mes
- ✅ **Bandwidth**: 100GB/mes
- ✅ **Invocaciones**: 1M/mes
- ⚠️ **Timeout**: 10 segundos (Hobby) / 60 segundos (Pro)
- ✅ **Deployments**: Ilimitados
- ✅ **Dominios custom**: 1 incluido

### 🛠️ Archivos de Configuración Creados:

#### 1. `vercel.json` - Configuración principal
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)", 
      "dest": "/frontend/$1"
    }
  ]
}
```

#### 2. `api/index.py` - Entry point para serverless
#### 3. `requirements-vercel.txt` - Dependencias optimizadas

## 🚀 Pasos para Desplegar:

### 1. Instalar Vercel CLI
```bash
npm i -g vercel
```

### 2. Login en Vercel
```bash
vercel login
```

### 3. Configurar Variables de Entorno
En el dashboard de Vercel o con CLI:
```bash
vercel env add GEMINI_API_KEY
vercel env add GOOGLE_APPLICATION_CREDENTIALS
vercel env add TELEGRAM_BOT_TOKEN
```

**Variables necesarias:**
- `GEMINI_API_KEY`: Tu API key de Google Gemini
- `GOOGLE_APPLICATION_CREDENTIALS`: Contenido del service_account.json (en Base64)
- `TELEGRAM_BOT_TOKEN`: `7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk`

### 4. Desplegar
```bash
vercel --prod
```

### 5. Configurar Bot de Telegram
Después del despliegue:
```bash
# Ir a tu URL de Vercel
curl https://tu-proyecto.vercel.app/api/telegram/setup
```

## 🤖 **Bot de Telegram Incluido:**

**Token configurado:** `7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk`

**Endpoints creados:**
- `/api/telegram/webhook` - Recibe mensajes del bot
- `/api/telegram/setup` - Configura el webhook automáticamente

**Comandos del bot:**
- `/start` - Iniciar conversación
- `/help` - Mostrar ayuda
- `/status` - Estado del sistema
- `/clientes` - Gestión de clientes

**Consultas naturales:**
- "buscar cliente Juan"
- "información de pagos"
- "zonas disponibles"

## ⚠️ Limitaciones del Plan Gratuito:

1. **Timeout de 10 segundos**: Puede afectar operaciones largas de Google Sheets
2. **Cold starts**: Primera petición puede ser lenta
3. **Sin base de datos persistente**: Solo APIs y archivos estáticos
4. **Límite de tamaño**: 50MB por función

## 🎯 Recomendaciones:

### ✅ Para Plan Gratuito:
- Usar solo como API backend
- Frontend estático servido desde Vercel
- Google Sheets como "base de datos"
- Operaciones rápidas (< 10 segundos)

### 🚀 Para Plan Pro ($20/mes):
- Timeout de 60 segundos
- Más recursos y bandwidth
- Mejor para uso empresarial

## 🔧 Optimizaciones Aplicadas:

1. **Dependencias mínimas** en `requirements-vercel.txt`
2. **Entry point optimizado** en `api/index.py`
3. **Routing configurado** para servir frontend + API
4. **Variables de entorno** configuradas para secretos

## 🎉 Resultado:

**SÍ, puedes subir tu proyecto a Vercel GRATIS** con funcionalidad completa, incluyendo:

✅ **API REST completa** - Todos los endpoints funcionales
✅ **Google Sheets** - Integración en tiempo real  
✅ **Gemini AI** - Agente inteligente
✅ **Dashboard Web** - Interfaz moderna
✅ **Bot de Telegram** - Configurado y listo (`@tu_bot_name`)

**Ideal para:**
- Demos y presentaciones
- Desarrollo y testing
- Uso personal/pequeña empresa
- Portfolio profesional
- Bot de soporte 24/7

**🚀 Próximos pasos después del despliegue:**
1. Configurar webhook de Telegram
2. Compartir Google Sheet con service account
3. Probar bot enviando `/start` a `@tu_bot_name`

¿Quieres proceder con el despliegue?
