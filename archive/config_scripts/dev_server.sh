#!/bin/bash
# Script para ejecutar Red Soluciones ISP localmente
# Simula el entorno de producción de Vercel

echo "🚀 Iniciando Red Soluciones ISP - Modo Desarrollo"
echo "================================================"

# Verificar que Python esté disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

# Instalar dependencias si es necesario
echo "📦 Verificando dependencias..."
python3 -m pip install -r requirements.txt --quiet

# Mostrar información del sistema
echo ""
echo "✨ Configuración:"
echo "   - Puerto: 8001"
echo "   - Host: localhost"
echo "   - Modo: Desarrollo (simula Vercel)"
echo ""

# Configurar variables de entorno
export ENVIRONMENT="development"
export DEBUG="true"

# Ejecutar servidor
echo "🔥 Iniciando servidor..."
echo "📱 Abrir en navegador: http://localhost:8001"
echo ""
echo "🔗 Endpoints disponibles:"
echo "   • GET  /           → Información de la API"
echo "   • GET  /health     → Estado del sistema"
echo "   • GET  /api/status → Estado de servicios"
echo "   • POST /api/contact → Formulario de contacto"
echo ""

# Ejecutar con el entry point de Vercel
python3 -c "
import uvicorn
from app import app

print('🚀 Red Soluciones ISP ejecutándose...')
print('⚡ Simulando entorno de Vercel localmente')
print('📖 Documentación: http://localhost:8001/docs')
print('')
print('Para detener: Ctrl+C')
print('=' * 50)

uvicorn.run(
    app, 
    host='0.0.0.0', 
    port=8001, 
    reload=True,
    log_level='info'
)
"
