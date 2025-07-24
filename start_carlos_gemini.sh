#!/bin/bash
# 🚀 ACTIVAR CARLOS CON GEMINI - Red Soluciones ISP
# ================================================

echo "🔧 Configurando variables de entorno para Carlos..."

# Exportar API Keys
export GEMINI_API_KEY="AIzaSyD5_316B_bOhy-lVJAdCliYH6ZBhFALBWo"
export TELEGRAM_BOT_TOKEN="7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk"

echo "✅ GEMINI_API_KEY configurada"
echo "✅ TELEGRAM_BOT_TOKEN configurada"

# Verificar que Gemini funciona
echo "🧪 Probando conexión con Gemini..."
python3 -c "
import google.generativeai as genai
import os
try:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content('Di: Gemini conectado correctamente')
    print(f'✅ Gemini: {response.text}')
except Exception as e:
    print(f'❌ Error Gemini: {e}')
"

echo ""
echo "🤖 Iniciando Carlos con inteligencia natural..."
echo "📱 Carlos estará disponible en Telegram con respuestas inteligentes"
echo ""

# Iniciar Carlos
python3 carlos_telegram_bot.py
