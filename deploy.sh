#!/bin/bash

# Red Soluciones ISP - Script de Deploy Automático
# Configura y despliega el sistema con credenciales

echo "🚀 RED SOLUCIONES ISP - DEPLOY AUTOMÁTICO"
echo "=========================================="

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar Python
if ! command_exists python3; then
    echo "❌ Error: Python3 no está instalado"
    exit 1
fi

# Verificar si estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encontró app.py. Ejecuta desde el directorio del proyecto."
    exit 1
fi

echo "✅ Directorio del proyecto verificado"

# Verificar/crear entorno virtual
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv .venv
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual encontrado"
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source .venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Dependencias instaladas"

# Verificar/configurar credenciales
echo "🔑 Verificando credenciales..."
if [ ! -f ".env" ]; then
    echo "⚠️  No se encontró archivo .env"
    echo "🔧 Iniciando configuración automática..."
    python3 configurar_credenciales.py
else
    echo "✅ Archivo .env encontrado"
    python3 verificar_credenciales.py
fi

# Verificar importaciones
echo "🔍 Verificando sistema..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from backend.app.main import app
    print('✅ Sistema verificado correctamente')
except Exception as e:
    print(f'❌ Error en verificación: {e}')
    sys.exit(1)
" || exit 1

# Opciones de deploy
echo ""
echo "🎯 OPCIONES DE DEPLOY:"
echo "1) Desarrollo local (uvicorn)"
echo "2) Producción Vercel"
echo "3) Solo verificar sistema"
echo ""

read -p "Selecciona una opción (1-3): " option

case $option in
    1)
        echo "🖥️  Iniciando servidor de desarrollo..."
        echo "🌐 URL: http://localhost:8004"
        echo "⏹️  Presiona Ctrl+C para detener"
        echo ""
        python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8004 --reload
        ;;
    2)
        if command_exists vercel; then
            echo "☁️  Desplegando en Vercel..."
            
            # Configurar variables de entorno en Vercel
            if [ -f ".env" ]; then
                echo "⚡ Configurando variables de entorno en Vercel..."
                
                # Leer variables del .env y configurarlas en Vercel
                while IFS= read -r line; do
                    if [[ $line =~ ^[A-Z_]+=.* ]] && [[ ! $line =~ ^# ]]; then
                        var_name=$(echo "$line" | cut -d'=' -f1)
                        var_value=$(echo "$line" | cut -d'=' -f2-)
                        echo "Setting $var_name..."
                        echo "$var_value" | vercel env add "$var_name" production
                    fi
                done < .env
            fi
            
            # Deploy
            vercel --prod
            echo "🎉 Deploy completado!"
        else
            echo "❌ Vercel CLI no está instalado"
            echo "📥 Instalar con: npm i -g vercel"
        fi
        ;;
    3)
        echo "✅ Sistema verificado y listo"
        echo "📖 Para iniciar: python3 app.py"
        ;;
    *)
        echo "❌ Opción no válida"
        exit 1
        ;;
esac

echo ""
echo "🎉 Proceso completado!"
echo "📖 Consulta CONFIGURACION_CREDENCIALES.md para más información"
