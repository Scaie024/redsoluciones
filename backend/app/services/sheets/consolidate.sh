#!/bin/bash

echo "🚀 Ejecutando script de consolidación para Red Soluciones ISP..."
echo "=============================================================="

# --- PASO 1: RESPALDAR PROYECTO (RECOMENDACIÓN) ---
echo "⚠️  IMPORTANTE: Asegúrate de tener un backup antes de continuar."
read -p "Presiona [Enter] para continuar o Ctrl+C para cancelar..."

# --- PASO 2: UNIFICAR CONFIGURACIÓN ---
echo "🔧 Unificando archivos de configuración..."
if [ -f "backend/app/core/config_unified.py" ]; then
    # Eliminar el config viejo si existe para evitar conflictos
    rm -f backend/app/core/config.py
    # Renombrar el unificado para que sea el principal
    mv backend/app/core/config_unified.py backend/app/core/config.py
    echo "✅ Configuración unificada en 'backend/app/core/config.py'"
else
    echo "⚠️  No se encontró 'config_unified.py'. Omitiendo unificación de config."
fi

# --- PASO 3: ELIMINAR DOCUMENTACIÓN ENGAÑOSA Y ARCHIVOS OBSOLETOS ---
echo "🗑️  Eliminando archivos obsoletos, duplicados y peligrosos..."

# Documentación engañosa con credenciales hardcodeadas
rm -f DEPLOY_READY.md
rm -f READY_TO_DEPLOY.md

# API Antigua y agentes/vistas duplicadas según PLAN_CONSOLIDACION.md
rm -f api/index.py
rm -f backend/app/services/modern_agent_v2.py
rm -f frontend/dashboard.html

# Otros archivos de configuración obsoletos
rm -f backend/app/core/vercel_config.py

echo "✅ Limpieza de archivos principales completada."

echo "🎉 Consolidación finalizada."
echo "👉 Revisa los cambios con 'git status' y actualiza el README.md."
echo "=============================================================="