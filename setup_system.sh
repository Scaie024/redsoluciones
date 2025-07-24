#!/bin/bash

# 🚀 CONFIGURADOR AUTOMÁTICO - RED SOLUCIONES ISP 2025
# ====================================================
# 
# Este script configura automáticamente todo el sistema para que funcione perfectamente

set -e  # Salir si hay algún error

# Colores para output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
PURPLE='\\033[0;35m'
CYAN='\\033[0;36m'
NC='\\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "${CYAN}================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}================================${NC}"
    echo
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "messaging/modern_launcher.py" ]; then
    print_error "Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

print_header "🚀 CONFIGURADOR RED SOLUCIONES ISP 2025"

echo -e "${PURPLE}Este script configurará automáticamente:${NC}"
echo "🤖 Agente conversacional moderno"
echo "📱 Bot de Telegram optimizado"
echo "🧠 Integración con IA (Gemini)"
echo "📊 Conexión a Google Sheets"
echo

# 1. Verificar Python
print_info "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_success "Python $PYTHON_VERSION detectado"

# 2. Crear directorio de logs si no existe
print_info "Configurando directorios..."
mkdir -p logs
mkdir -p config
print_success "Directorios creados"

# 3. Instalar dependencias
print_info "Instalando dependencias de Python..."
pip3 install -q python-telegram-bot[all] google-generativeai gspread oauth2client python-dotenv
print_success "Dependencias instaladas"

# 4. Configurar variables de entorno
print_header "🔧 CONFIGURACIÓN DE VARIABLES"

# Verificar si ya existe .env
if [ -f ".env" ]; then
    print_warning "Archivo .env ya existe"
    read -p "¿Quieres sobrescribirlo? (y/N): " overwrite
    if [[ ! $overwrite =~ ^[Yy]$ ]]; then
        print_info "Manteniendo configuración actual"
    else
        rm .env
    fi
fi

# Crear .env si no existe
if [ ! -f ".env" ]; then
    print_info "Creando archivo .env..."
    
    # Token de Telegram
    echo
    echo -e "${YELLOW}📱 CONFIGURACIÓN DE TELEGRAM BOT${NC}"
    echo "1. Ve a https://t.me/BotFather"
    echo "2. Envía /newbot"
    echo "3. Sigue las instrucciones"
    echo "4. Copia el token que te da"
    echo
    read -p "🔑 Pega tu TELEGRAM_BOT_TOKEN: " TELEGRAM_TOKEN
    
    # API Key de Gemini (opcional)
    echo
    echo -e "${YELLOW}🧠 CONFIGURACIÓN DE IA (OPCIONAL)${NC}"
    echo "1. Ve a https://makersuite.google.com/app/apikey"
    echo "2. Crea una nueva API key"
    echo "3. Cópiala aquí (o presiona Enter para omitir)"
    echo
    read -p "🔑 Pega tu GEMINI_API_KEY (opcional): " GEMINI_KEY
    
    # Crear archivo .env
    cat > .env << EOF
# 🚀 RED SOLUCIONES ISP - CONFIGURACIÓN 2025
# ==========================================

# 📱 Telegram Bot
TELEGRAM_BOT_TOKEN="$TELEGRAM_TOKEN"

# 🧠 IA (Google Gemini) - Opcional pero recomendado
GEMINI_API_KEY="$GEMINI_KEY"

# 📊 Google Sheets - Ya configurado
GOOGLE_SHEETS_ENABLED=true

# 🎯 Configuración del agente
AGENT_NAME="Carlos"
AGENT_PERSONALITY="profesional_mexicano"
AGENT_MAX_RESPONSE_LENGTH=400

# 🔧 Sistema
DEBUG=false
LOG_LEVEL=INFO
EOF

    print_success "Archivo .env creado"
fi

# 5. Configurar Google Sheets
print_header "📊 VERIFICANDO GOOGLE SHEETS"

if [ -f "service_account.json" ] || [ -f "config/service_account.json" ]; then
    print_success "Credenciales de Google Sheets encontradas"
else
    print_warning "service_account.json no encontrado"
    echo "💡 Para conectar Google Sheets:"
    echo "1. Ve a https://console.cloud.google.com/"
    echo "2. Crea un proyecto o selecciona uno existente"
    echo "3. Habilita Google Sheets API"
    echo "4. Crea credenciales de cuenta de servicio"
    echo "5. Descarga el JSON y guárdalo como 'service_account.json'"
fi

# 6. Verificar configuración
print_header "🔍 VERIFICANDO CONFIGURACIÓN"

# Cargar variables de entorno
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Verificar token de Telegram
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    print_success "Token de Telegram configurado"
else
    print_error "Token de Telegram no configurado"
fi

# Verificar Gemini
if [ -n "$GEMINI_API_KEY" ]; then
    print_success "API Key de Gemini configurada"
else
    print_warning "API Key de Gemini no configurada (el agente funcionará sin IA)"
fi

# 7. Crear script de inicio rápido
print_info "Creando script de inicio rápido..."

cat > start_system.sh << 'EOF'
#!/bin/bash

# 🚀 INICIO RÁPIDO - RED SOLUCIONES ISP
# ====================================

# Cargar variables de entorno
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Colores
GREEN='\\033[0;32m'
CYAN='\\033[0;36m'
NC='\\033[0m'

echo -e "${CYAN}🚀 Iniciando Red Soluciones ISP - Sistema Moderno${NC}"
echo

# Verificar configuración
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN no configurado"
    echo "💡 Ejecuta ./setup_system.sh para configurar"
    exit 1
fi

echo -e "${GREEN}✅ Configuración verificada${NC}"
echo -e "${GREEN}🤖 Iniciando agente inteligente...${NC}"
echo

# Ejecutar sistema
python3 messaging/modern_launcher.py
EOF

chmod +x start_system.sh

print_success "Script de inicio creado: ./start_system.sh"

# 8. Crear script de verificación de salud
cat > check_health.sh << 'EOF'
#!/bin/bash

# 🏥 VERIFICACIÓN DE SALUD DEL SISTEMA
# ===================================

# Cargar variables de entorno
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "🏥 Verificando salud del sistema..."
python3 messaging/modern_launcher.py --health
EOF

chmod +x check_health.sh

print_success "Script de verificación creado: ./check_health.sh"

# 9. Resumen final
print_header "🎉 CONFIGURACIÓN COMPLETADA"

echo -e "${GREEN}✅ Sistema configurado correctamente${NC}"
echo
echo -e "${PURPLE}📋 PRÓXIMOS PASOS:${NC}"
echo
echo -e "${CYAN}1. Verificar el sistema:${NC}"
echo "   ./check_health.sh"
echo
echo -e "${CYAN}2. Iniciar el sistema:${NC}"
echo "   ./start_system.sh"
echo
echo -e "${CYAN}3. Probar tu bot:${NC}"
echo "   - Abre Telegram"
echo "   - Busca tu bot"
echo "   - Envía /start"
echo
echo -e "${PURPLE}💡 TIPS:${NC}"
echo "• El agente funciona sin IA, pero es mucho mejor con Gemini"
echo "• Puedes cambiar la personalidad en backend/app/core/config.py"
echo "• Los logs se guardan en logs/system.log"
echo "• Usa Ctrl+C para detener el sistema"
echo

if [ -n "$GEMINI_API_KEY" ]; then
    echo -e "${GREEN}🧠 IA configurada: Tu agente será súper inteligente${NC}"
else
    echo -e "${YELLOW}⚠️  Sin IA: El agente usará respuestas predefinidas${NC}"
fi

echo
echo -e "${CYAN}🎯 Tu sistema está listo para revolucionar la atención al cliente${NC}"
echo
