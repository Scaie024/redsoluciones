#!/bin/bash
# 🚀 RED SOLUCIONES ISP - COMANDOS RÁPIDOS
# ======================================

echo "🏢 RED SOLUCIONES ISP v1.0.0 - COMANDOS RÁPIDOS"
echo "=================================================="

# Función para mostrar menú
show_menu() {
    echo ""
    echo "📋 OPCIONES DISPONIBLES:"
    echo "  1) 🚀 Iniciar servidor"
    echo "  2) 🔍 Verificar sistema"
    echo "  3) 🛑 Detener servidor"
    echo "  4) 📊 Ver logs en tiempo real"
    echo "  5) 🌐 Abrir dashboard en navegador"
    echo "  6) 📚 Abrir documentación API"
    echo "  7) ❓ Mostrar ayuda"
    echo "  8) 🚪 Salir"
    echo ""
}

# Función para iniciar servidor
start_server() {
    echo "🚀 Iniciando Red Soluciones ISP..."
    python3 start_server.py &
    echo "✅ Servidor iniciado en http://localhost:8004"
}

# Función para verificar sistema
verify_system() {
    echo "🔍 Verificando sistema completo..."
    python3 final_verification.py
}

# Función para detener servidor
stop_server() {
    echo "🛑 Deteniendo servidor..."
    pkill -f "uvicorn.*8004"
    echo "✅ Servidor detenido"
}

# Función para ver logs
view_logs() {
    echo "📊 Logs en tiempo real (Ctrl+C para salir):"
    tail -f backend/app/utils/logs/redsol_$(date +%Y%m%d).log 2>/dev/null || echo "📝 No hay logs del día actual"
}

# Función para abrir dashboard
open_dashboard() {
    echo "🌐 Abriendo dashboard..."
    open http://localhost:8004/dashboard.html 2>/dev/null || echo "🔗 Abrir manualmente: http://localhost:8004/dashboard.html"
}

# Función para abrir docs
open_docs() {
    echo "📚 Abriendo documentación..."
    open http://localhost:8004/docs 2>/dev/null || echo "🔗 Abrir manualmente: http://localhost:8004/docs"
}

# Función de ayuda
show_help() {
    echo "❓ AYUDA - RED SOLUCIONES ISP"
    echo "============================="
    echo ""
    echo "🎯 ACCESOS RÁPIDOS:"
    echo "   • Dashboard: http://localhost:8004/dashboard.html"
    echo "   • Admin: http://localhost:8004/admin.html"
    echo "   • API Docs: http://localhost:8004/docs"
    echo "   • Health: http://localhost:8004/health"
    echo ""
    echo "🤖 COMANDOS DEL AGENTE:"
    echo "   • 'estadísticas' - Resumen del negocio"
    echo "   • 'buscar [nombre]' - Encontrar cliente"
    echo "   • 'análisis financiero' - Reportes detallados"
    echo "   • 'clientes activos' - Lista de clientes"
    echo ""
    echo "📁 ARCHIVOS IMPORTANTES:"
    echo "   • start_server.py - Iniciar sistema"
    echo "   • final_verification.py - Verificar todo"
    echo "   • SISTEMA_ORDENADO.md - Documentación completa"
    echo ""
}

# Bucle principal del menú
while true; do
    show_menu
    read -p "🎯 Selecciona una opción (1-8): " choice
    
    case $choice in
        1) start_server ;;
        2) verify_system ;;
        3) stop_server ;;
        4) view_logs ;;
        5) open_dashboard ;;
        6) open_docs ;;
        7) show_help ;;
        8) echo "👋 ¡Hasta luego!"; exit 0 ;;
        *) echo "❌ Opción inválida. Intenta de nuevo." ;;
    esac
    
    echo ""
    read -p "📌 Presiona Enter para continuar..."
done
