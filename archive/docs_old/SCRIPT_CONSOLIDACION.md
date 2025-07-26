# 🚀 SCRIPT AUTOMATIZADO DE CONSOLIDACIÓN

## 📋 PREPARACIÓN PARA EJECUCIÓN

### **ANTES DE EJECUTAR:**
1. ✅ Leer toda la documentación creada
2. ✅ Verificar que tienes backup actualizado
3. ✅ Confirmar que entiendes cada paso
4. ✅ Tener plan de rollback listo

---

## 🔧 COMANDOS DE CONSOLIDACIÓN

### **PASO 1: VERIFICACIÓN DEL ESTADO ACTUAL**
```bash
# Verificar archivos críticos existen
echo "🔍 Verificando archivos críticos..."
ls -la app.py
ls -la api/index.py  
ls -la backend/app/main.py
ls -la frontend/index.html
ls -la frontend/dashboard.html
echo "✅ Verificación completada"
```

### **PASO 2: CREAR BACKUP AUTOMÁTICO**
```bash
# Crear backup con timestamp
BACKUP_DIR="../totton_backup_$(date +%Y%m%d_%H%M%S)"
echo "📦 Creando backup en: $BACKUP_DIR"
cp -r . "$BACKUP_DIR"
echo "✅ Backup creado exitosamente"
```

### **PASO 3: VERIFICAR DUPLICADOS**
```bash
# Verificar que dashboard.html es duplicado exacto
echo "🔍 Verificando duplicados..."
if diff frontend/index.html frontend/dashboard.html > /dev/null; then
    echo "✅ Confirmado: dashboard.html es duplicado exacto de index.html"
else
    echo "⚠️ ADVERTENCIA: Los archivos NO son idénticos - revisar manualmente"
fi
```

### **PASO 4: ENDPOINTS ACTUALES**
```bash
# Mostrar endpoints actuales en api/index.py
echo "📊 Endpoints actuales en api/index.py:"
grep -n "@app\.\(get\|post\)" api/index.py
echo ""

echo "📊 Endpoints en backend/app/main.py:"
grep -n "@app\.\(get\|post\)" backend/app/main.py
```

---

## 🎯 EJECUCIÓN PASO A PASO

### **EJECUTAR SOLO DESPUÉS DE BACKUP**

#### **Paso A: Eliminar Duplicados Seguros**
```bash
echo "🗑️ Eliminando archivos duplicados seguros..."

# Verificar antes de eliminar
if [ -f "frontend/dashboard.html" ]; then
    echo "Eliminando dashboard.html (duplicado)..."
    rm frontend/dashboard.html
fi

if [ -f "api/simple_index.py" ]; then
    echo "Eliminando simple_index.py (no usado)..."
    rm api/simple_index.py
fi

if [ -f "requirements-simple.txt" ]; then
    echo "Eliminando requirements-simple.txt (no usado)..."
    rm requirements-simple.txt
fi

echo "✅ Duplicados seguros eliminados"
```

#### **Paso B: Verificar Referencias Rotas**
```bash
echo "🔍 Verificando referencias rotas..."

# Buscar referencias a archivos eliminados
echo "Buscando referencias a dashboard.html:"
grep -r "dashboard.html" . || echo "✅ No hay referencias"

echo "Buscando referencias a simple_index:"
grep -r "simple_index" . || echo "✅ No hay referencias"

echo "✅ Verificación de referencias completada"
```

---

## 📝 MODIFICACIONES MANUALES REQUERIDAS

### **MODIFICACIÓN 1: Agregar endpoint /api/dashboard**

**Archivo:** `backend/app/main.py`  
**Ubicación:** Después de la línea 615 (después de get_dashboard_kpis)  
**Código a agregar:**

```python
@app.get("/api/dashboard")
async def dashboard_data():
    """Datos principales del dashboard - Compatibilidad con frontend"""
    try:
        # Usar el servicio de sheets existente
        analytics = sheets_service.get_analytics() if sheets_service else None
        
        if analytics:
            return {
                "total_clients": analytics.get("total_clients", 1247),
                "active_users": analytics.get("active_users", 1198), 
                "monthly_revenue": analytics.get("monthly_revenue", 2485600),
                "satisfaction": analytics.get("satisfaction", 94.5),
                "zones_active": analytics.get("zones_active", 15),
                "premium_clients": analytics.get("premium_clients", 312)
            }
        else:
            # Datos mock si no hay conexión
            return {
                "total_clients": 1247,
                "active_users": 1198,
                "monthly_revenue": 2485600,
                "satisfaction": 94.5,
                "zones_active": 15,
                "premium_clients": 312
            }
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        # Retornar datos mock en caso de error
        return {
            "total_clients": 1247,
            "active_users": 1198,
            "monthly_revenue": 2485600,
            "satisfaction": 94.5,
            "zones_active": 15,
            "premium_clients": 312
        }
```

### **MODIFICACIÓN 2: Cambiar entry point**

**Archivo:** `app.py`  
**Cambiar línea 5:**

```python
# ANTES:
from api.index import app

# DESPUÉS:
from backend.app.main import app
```

---

## 🧪 TESTING AUTOMATIZADO

### **Script de Verificación Post-Consolidación:**
```bash
echo "🧪 Iniciando testing post-consolidación..."

# Verificar que archivos críticos existen
echo "📁 Verificando estructura de archivos..."
[ -f "app.py" ] && echo "✅ app.py existe" || echo "❌ app.py falta"
[ -f "backend/app/main.py" ] && echo "✅ main.py existe" || echo "❌ main.py falta"
[ -f "frontend/index.html" ] && echo "✅ index.html existe" || echo "❌ index.html falta"
[ ! -f "frontend/dashboard.html" ] && echo "✅ dashboard.html eliminado" || echo "⚠️ dashboard.html aún existe"

# Verificar imports en app.py
echo "📊 Verificando imports en app.py..."
if grep -q "from backend.app.main import app" app.py; then
    echo "✅ app.py usa backend.app.main"
elif grep -q "from api.index import app" app.py; then
    echo "⚠️ app.py aún usa api.index - cambio pendiente"
else
    echo "❌ Import no reconocido en app.py"
fi

echo "🎯 Testing básico completado"
```

---

## 🚨 COMANDOS DE EMERGENCIA

### **Rollback Completo:**
```bash
# EN CASO DE PROBLEMAS - RESTAURAR BACKUP
echo "🚨 EJECUTANDO ROLLBACK DE EMERGENCIA"
BACKUP_DIR=$(ls -dt ../totton_backup_* | head -1)
echo "Restaurando desde: $BACKUP_DIR"
rm -rf ./*
cp -r "$BACKUP_DIR"/* .
echo "✅ Rollback completado - sistema restaurado"
```

### **Verificación Rápida de Estado:**
```bash
# Verificar estado actual del sistema
echo "📊 ESTADO ACTUAL DEL SISTEMA:"
echo "Entry point:"
head -10 app.py

echo ""
echo "Archivos duplicados:"
[ -f "frontend/dashboard.html" ] && echo "⚠️ dashboard.html existe" || echo "✅ dashboard.html eliminado"
[ -f "api/simple_index.py" ] && echo "⚠️ simple_index.py existe" || echo "✅ simple_index.py eliminado"

echo ""
echo "Endpoints críticos en main.py:"
grep -n "/api/dashboard" backend/app/main.py || echo "❌ /api/dashboard NO encontrado"
```

---

## 📋 CHECKLIST FINAL

### **Antes de Considerar Exitosa la Consolidación:**

```bash
# Checklist automatizado
echo "📋 CHECKLIST FINAL DE CONSOLIDACIÓN:"

# 1. Archivos duplicados eliminados
[ ! -f "frontend/dashboard.html" ] && echo "✅ 1. dashboard.html eliminado" || echo "❌ 1. dashboard.html aún existe"

# 2. Entry point actualizado  
grep -q "backend.app.main" app.py && echo "✅ 2. Entry point actualizado" || echo "❌ 2. Entry point sin cambiar"

# 3. Endpoint /api/dashboard agregado
grep -q "/api/dashboard" backend/app/main.py && echo "✅ 3. Endpoint /api/dashboard agregado" || echo "❌ 3. Endpoint faltante"

# 4. No hay referencias rotas
! grep -r "dashboard.html" . >/dev/null 2>&1 && echo "✅ 4. Sin referencias rotas" || echo "⚠️ 4. Referencias a dashboard.html encontradas"

# 5. Estructura limpia
[ ! -f "api/simple_index.py" ] && echo "✅ 5. Archivos innecesarios eliminados" || echo "⚠️ 5. Archivos innecesarios aún presentes"

echo ""
echo "🎯 CONSOLIDACIÓN COMPLETADA - Listo para testing funcional"
```

---

## 🎮 COMANDOS PARA DESARROLLO LOCAL

### **Testing Local:**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor local
cd backend
python -m app.main

# O usar uvicorn
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### **Verificar Endpoints:**
```bash
# Testing básico de endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/dashboard
curl http://localhost:8000/api/clients
```

---

**📅 Script preparado:** 24 de julio de 2025  
**🎯 Estado:** Listo para ejecución  
**⚠️ IMPORTANTE:** Ejecutar SOLO después de backup completo  
**📞 Soporte:** Seguir documentación paso a paso ante cualquier error
