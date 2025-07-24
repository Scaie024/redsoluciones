# 🤖 CARLOS CON GEMINI - Variables de Entorno
# ============================================
# Agregar estas líneas a tu ~/.bashrc o ~/.zshrc para configuración permanente

# API de Gemini para respuestas inteligentes de Carlos
export GEMINI_API_KEY="AIzaSyD5_316B_bOhy-lVJAdCliYH6ZBhFALBWo"

# Token del Bot de Telegram
export TELEGRAM_BOT_TOKEN="7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk"

# INSTRUCCIONES:
# ==============
# 1. Ejecuta: source carlos_env.sh
# 2. O agrega el contenido a tu ~/.zshrc:
#    echo 'export GEMINI_API_KEY="AIzaSyD5_316B_bOhy-lVJAdCliYH6ZBhFALBWo"' >> ~/.zshrc
#    echo 'export TELEGRAM_BOT_TOKEN="7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk"' >> ~/.zshrc
# 3. Reinicia terminal o ejecuta: source ~/.zshrc
# 4. Inicia Carlos: python3 carlos_telegram_bot.py

echo "✅ Variables de entorno para Carlos configuradas"
echo "🤖 Carlos listo para usar Gemini AI"
echo "📱 Bot de Telegram activo"
