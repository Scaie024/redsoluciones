#!/bin/bash

echo "🚀 Iniciando Red Soluciones ISP..."
echo "=================================="

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

# Crear directorio de logs si no existe
mkdir -p backend/app/utils/logs

# Verificar archivo de entorno
if [ ! -f ".env" ]; then
    echo "⚠️ Archivo .env no encontrado, usando .env.example como base"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "📝 Archivo .env creado desde .env.example"
        echo "⚠️ IMPORTANTE: Configura tus API keys en el archivo .env"
    fi
fi

# Instalar dependencias si es necesario
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv .venv
fi

echo "🔧 Activando entorno virtual..."
source .venv/bin/activate

echo "📋 Instalando/actualizando dependencias..."
pip install -q -r requirements.txt

echo "🔍 Verificando configuración..."
python3 -c "
import os
print('✅ Python configurado')
try:
    import fastapi
    print('✅ FastAPI disponible')
except ImportError:
    print('❌ FastAPI no disponible')

try:
    import google.generativeai
    print('✅ Gemini AI disponible')
except ImportError:
    print('⚠️ Gemini AI no disponible - modo fallback')

if os.path.exists('service_account.json'):
    print('✅ Google Sheets credenciales encontradas')
else:
    print('⚠️ Google Sheets credenciales no encontradas')
"

echo ""
echo "🌐 Iniciando servidor optimizado..."
echo "=================================="
echo "✅ Sistema listo!"
echo "📱 Dashboard: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo "❤️  Health: http://localhost:8000/health"
echo "📊 Status: http://localhost:8000/api/status"
echo "=================================="

# Usar api/index.py que está más estable para Vercel pero con puerto diferente para desarrollo
export PYTHONPATH="${PWD}:${PYTHONPATH}"
uvicorn api.index:app --host 0.0.0.0 --port 8000 --reload
