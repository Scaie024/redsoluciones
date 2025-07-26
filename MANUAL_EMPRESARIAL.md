# 🏢 RED SOLUCIONES ISP - SISTEMA EMPRESARIAL
## Manual para Propietarios y Personal Autorizado

### ⚠️ **IMPORTANTE: SISTEMA SIN MODO DEMO**

Este sistema ha sido configurado **exclusivamente para uso empresarial real**. 
**NO EXISTE MODO DEMO** - todas las funcionalidades requieren credenciales válidas.

---

## 🔐 **CREDENCIALES OBLIGATORIAS**

### ✅ **Para que el sistema funcione, DEBE tener configurado:**

1. **🔑 GOOGLE_SHEET_ID**: ID de su hoja de Google Sheets
2. **🤖 GEMINI_API_KEY**: Clave de Google Gemini AI para el chat inteligente
3. **📄 service_account.json**: Archivo de credenciales de Google Cloud

### ❌ **Sin estas credenciales, el sistema NO INICIARÁ**

---

## 🚀 **CONFIGURACIÓN INICIAL**

### **Opción 1: Configuración Automática (RECOMENDADA)**
```bash
# Ejecutar script de configuración empresarial
python3 configurar_empresa.py
```

### **Opción 2: Configuración Manual**
1. Copiar `.env.example` a `.env`
2. Editar `.env` con sus credenciales reales
3. Colocar `service_account.json` en la raíz
4. Ejecutar: `python3 verificar_credenciales.py`

---

## 📋 **CÓMO OBTENER LAS CREDENCIALES**

### **🔑 Google Sheets ID:**
1. Abrir su hoja de Google Sheets de Red Soluciones
2. Copiar el ID de la URL: `docs.google.com/spreadsheets/d/[ESTE_ID]/edit`
3. Ejemplo: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

### **🤖 Gemini AI API Key:**
1. Ir a: https://makersuite.google.com/app/apikey
2. Crear proyecto o usar existente
3. Generar API Key
4. Formato: `AIzaSyC...`

### **📄 Service Account JSON:**
1. Ir a: https://console.cloud.google.com/
2. IAM & Admin > Service Accounts
3. Crear cuenta de servicio
4. Descargar archivo JSON
5. Guardar como `service_account.json` en la raíz

---

## 🏃‍♂️ **INICIO RÁPIDO**

### **Para Personal Técnico:**
```bash
# 1. Verificar sistema
python3 verificar_credenciales.py

# 2. Si todo está OK, iniciar
python3 app.py

# 3. Acceder al sistema
# http://localhost:8004
```

### **Para Administradores:**
```bash
# Configuración completa automática
./deploy.sh
```

---

## 🎯 **FUNCIONALIDADES EMPRESARIALES**

### ✅ **Gestión Completa:**
- **👥 Clientes**: CRUD completo con datos reales
- **🎯 Prospectos**: Sistema de seguimiento
- **🔧 Incidencias**: Gestión de tickets técnicos
- **💬 Chat IA**: Asistente Carlos con Gemini AI
- **📊 Analytics**: Métricas del negocio en tiempo real
- **🔍 Búsquedas**: Filtros avanzados

### ✅ **Integración Total:**
- **📊 Google Sheets**: Base de datos sincronizada
- **🤖 IA Avanzada**: Chat inteligente empresarial
- **📱 Responsive**: Funciona en móviles y tablets
- **🔒 Seguro**: Credenciales encriptadas

---

## 🔧 **VERIFICACIÓN DEL SISTEMA**

### **Script de Verificación:**
```bash
python3 verificar_credenciales.py
```

### **Estados Posibles:**
- ✅ **LISTO PARA PRODUCCIÓN**: Todas las credenciales configuradas
- ❌ **CONFIGURACIÓN INCOMPLETA**: Faltan credenciales obligatorias

---

## 🚨 **SEGURIDAD Y MANTENIMIENTO**

### **🔒 Archivo .env (CRÍTICO):**
- ⛔ **NO compartir con personal no autorizado**
- ⛔ **NO subir a repositorios públicos**
- ✅ **Hacer backup periódico**
- ✅ **Renovar API keys cada 6 meses**

### **📄 service_account.json:**
- ⛔ **Mantener privado y seguro**
- ✅ **Solo acceso para administradores**
- ✅ **Backup en ubicación segura**

---

## 📞 **SOPORTE TÉCNICO**

### **Problemas Comunes:**

**❌ "GOOGLE_SHEET_ID es obligatorio"**
- Verificar que la variable está en `.env`
- Confirmar que el ID es correcto

**❌ "GEMINI_API_KEY es obligatorio"**
- Verificar API key en `.env`
- Confirmar que la key es válida

**❌ "service_account.json no encontrado"**
- Verificar que el archivo está en la raíz
- Confirmar permisos de lectura

**❌ "Address already in use"**
- Cambiar puerto: `PORT=8005`
- O terminar procesos: `lsof -ti:8004 | xargs kill`

### **Contacto de Emergencia:**
- **Administrador del Sistema**: [configurar contacto]
- **Soporte Técnico**: [configurar contacto]

---

## 🎉 **SISTEMA LISTO**

Una vez configurado correctamente:

- **🌐 URL**: `http://localhost:8004`
- **📚 API**: `http://localhost:8004/docs`
- **🔧 Admin**: Panel de administración integrado
- **📱 Mobile**: Interface responsive

**🏆 Su Red Soluciones ISP está completamente operativa para uso empresarial.**

---

## ⚖️ **POLÍTICA DE USO**

Este sistema es **propiedad exclusiva de Red Soluciones ISP** y está configurado únicamente para uso interno de la empresa. El acceso no autorizado está prohibido.

**Última actualización**: Julio 2025  
**Versión del Sistema**: 2.0.0 Empresarial
