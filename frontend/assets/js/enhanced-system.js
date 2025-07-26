// === CHAT MEJORADO CON IA HOMOLOGADA ===
const EnhancedChat = {
  container: null,
  messagesContainer: null,
  inputContainer: null,
  isThinking: false,
  conversationHistory: [],
  
  async initialize() {
    console.log('💬 Inicializando chat mejorado...');
    
    this.container = document.getElementById('chat-container');
    if (!this.container) {
      console.warn('⚠️ Container de chat no encontrado');
      return;
    }
    
    this.setupChatInterface();
    this.bindEvents();
    this.showWelcomeMessage();
  },
  
  setupChatInterface() {
    this.container.innerHTML = `
      <div class="chat-header">
        <div class="chat-title">
          <i class="fas fa-robot"></i>
          <span>Asistente IA Red Soluciones</span>
          <span class="chat-status online">En línea</span>
        </div>
        <div class="chat-actions">
          <button onclick="EnhancedChat.refreshContext()" title="Refrescar contexto">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button onclick="EnhancedChat.clearChat()" title="Limpiar chat">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>
      
      <div class="chat-messages" id="chatMessages">
        <!-- Mensajes aparecerán aquí -->
      </div>
      
      <div class="chat-input-container">
        <div class="quick-actions" id="quickActions">
          <!-- Acciones rápidas aparecerán aquí -->
        </div>
        <div class="chat-input-wrapper">
          <input type="text" 
                 id="chatInput" 
                 placeholder="Pregunta sobre clientes, incidentes, estadísticas..."
                 autocomplete="off">
          <button id="sendButton" onclick="EnhancedChat.sendMessage()">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
    `;
    
    this.messagesContainer = document.getElementById('chatMessages');
    this.inputContainer = document.getElementById('chatInput');
    
    // Agregar listener para Enter
    this.inputContainer.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });
  },
  
  bindEvents() {
    // Escuchar cambios de estado del sistema
    SystemState.addListener((event, data) => {
      if (event === 'context_loaded') {
        this.updateQuickActions();
      }
    });
  },
  
  showWelcomeMessage() {
    const userName = SystemState.currentUser ? 
      SystemState.currentUser.charAt(0).toUpperCase() + SystemState.currentUser.slice(1) : 
      'Usuario';
    
    const welcomeMessage = `¡Hola ${userName}! Soy tu asistente IA empresarial. 

Puedo ayudarte con:
• Información de clientes y prospectos
• Análisis de incidentes pendientes
• Estadísticas del negocio
• Insights automáticos

¿En qué puedo ayudarte hoy?`;
    
    this.addMessage('assistant', welcomeMessage, { welcome: true });
    this.updateQuickActions();
  },
  
  updateQuickActions() {
    const quickActionsContainer = document.getElementById('quickActions');
    if (!quickActionsContainer) return;
    
    const context = SystemState.systemContext;
    const quickActions = context?.quick_actions || [
      { action: 'get_stats', label: 'Ver Estadísticas', icon: 'chart-bar' },
      { action: 'check_incidents', label: 'Incidentes Pendientes', icon: 'exclamation-triangle' },
      { action: 'client_search', label: 'Buscar Cliente', icon: 'search' },
      { action: 'add_client', label: 'Nuevo Cliente', icon: 'user-plus' }
    ];
    
    quickActionsContainer.innerHTML = quickActions.map(action => `
      <button class="quick-action-btn" onclick="EnhancedChat.executeQuickAction('${action.action}')">
        <i class="fas fa-${action.icon}"></i>
        ${action.label}
      </button>
    `).join('');
  },
  
  async executeQuickAction(actionType) {
    const actions = {
      'get_stats': 'Muéstrame las estadísticas del negocio',
      'check_incidents': 'Incidentes pendientes que necesitan atención',
      'client_search': 'Necesito buscar información de un cliente',
      'add_client': 'Quiero agregar un nuevo cliente'
    };
    
    const message = actions[actionType] || actionType;
    await this.sendMessage(message);
  },
  
  async sendMessage(customMessage = null) {
    const message = customMessage || this.inputContainer.value.trim();
    
    if (!message) return;
    
    // Limpiar input si no es mensaje personalizado
    if (!customMessage) {
      this.inputContainer.value = '';
    }
    
    // Agregar mensaje del usuario
    this.addMessage('user', message);
    
    // Mostrar indicador de "pensando"
    this.showThinking();
    
    try {
      // Enviar a la API mejorada
      const response = await fetch(`${API_V2_BASE}/chat/enhanced`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: message,
          user_name: SystemState.currentUser,
          session_id: SystemState.sessionId
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Agregar respuesta del asistente
        this.addMessage('assistant', data.message, {
          action_type: data.action_type,
          confidence: data.confidence,
          data: data.data,
          suggestions: data.suggestions,
          quick_actions: data.quick_actions,
          context_used: data.context_used
        });
        
        // Actualizar historial
        this.conversationHistory.push({
          user: message,
          assistant: data.message,
          timestamp: new Date().toISOString(),
          metadata: data
        });
        
      } else {
        this.addMessage('error', `Error: ${data.message}`, {
          suggestions: data.suggestions || []
        });
      }
      
    } catch (error) {
      console.error('Error enviando mensaje:', error);
      this.addMessage('error', 'Error de conexión. Verifica tu conexión a internet.', {
        suggestions: ['Intentar nuevamente', 'Refrescar página']
      });
    } finally {
      this.hideThinking();
    }
  },
  
  addMessage(type, content, metadata = {}) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}`;
    
    const timestamp = new Date().toLocaleTimeString('es-ES', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
    
    let messageHTML = `
      <div class="message-content">
        <div class="message-text">${this.formatMessage(content)}</div>
        <div class="message-time">${timestamp}</div>
      </div>
    `;
    
    // Agregar información adicional según el tipo
    if (type === 'assistant' && metadata.confidence) {
      messageHTML += `
        <div class="message-metadata">
          <span class="confidence">Confianza: ${(metadata.confidence * 100).toFixed(0)}%</span>
          ${metadata.action_type ? `<span class="action-type">${metadata.action_type}</span>` : ''}
        </div>
      `;
    }
    
    // Agregar sugerencias si las hay
    if (metadata.suggestions && metadata.suggestions.length > 0) {
      messageHTML += `
        <div class="message-suggestions">
          <div class="suggestions-title">Sugerencias:</div>
          ${metadata.suggestions.map(suggestion => `
            <button class="suggestion-btn" onclick="EnhancedChat.sendMessage('${suggestion}')">
              ${suggestion}
            </button>
          `).join('')}
        </div>
      `;
    }
    
    // Agregar acciones rápidas si las hay
    if (metadata.quick_actions && metadata.quick_actions.length > 0) {
      messageHTML += `
        <div class="message-actions">
          ${metadata.quick_actions.map(action => `
            <button class="action-btn" onclick="EnhancedChat.executeAction('${action.action}')">
              <i class="fas fa-${action.icon || 'arrow-right'}"></i>
              ${action.label}
            </button>
          `).join('')}
        </div>
      `;
    }
    
    messageDiv.innerHTML = messageHTML;
    this.messagesContainer.appendChild(messageDiv);
    
    // Scroll al final
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  },
  
  formatMessage(message) {
    // Formatear texto con markdown básico
    return message
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>')
      .replace(/•/g, '•');
  },
  
  showThinking() {
    this.isThinking = true;
    const thinkingDiv = document.createElement('div');
    thinkingDiv.id = 'thinkingIndicator';
    thinkingDiv.className = 'chat-message assistant thinking';
    thinkingDiv.innerHTML = `
      <div class="message-content">
        <div class="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="message-text">Analizando...</div>
      </div>
    `;
    
    this.messagesContainer.appendChild(thinkingDiv);
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  },
  
  hideThinking() {
    this.isThinking = false;
    const thinkingDiv = document.getElementById('thinkingIndicator');
    if (thinkingDiv) {
      thinkingDiv.remove();
    }
  },
  
  async executeAction(actionType) {
    // Implementar acciones específicas
    console.log('Ejecutando acción:', actionType);
    
    switch (actionType) {
      case 'view_client_history':
        await this.sendMessage('Muéstrame el historial completo del cliente');
        break;
      case 'create_incident':
        await this.sendMessage('Quiero crear un nuevo incidente');
        break;
      case 'list_all_clients':
        await this.sendMessage('Lista todos mis clientes activos');
        break;
      case 'detailed_analytics':
        await this.sendMessage('Análisis detallado del negocio');
        break;
      default:
        await this.sendMessage(`Ejecutar acción: ${actionType}`);
    }
  },
  
  async refreshContext() {
    console.log('🔄 Refrescando contexto del chat...');
    
    try {
      const result = await SystemState.refreshSystemData();
      if (result.success) {
        this.addMessage('system', 'Contexto actualizado. Los datos más recientes están disponibles.', {
          suggestions: ['Ver estadísticas actualizadas', 'Revisar incidentes nuevos']
        });
      } else {
        throw new Error(result.error || 'Error refrescando datos');
      }
    } catch (error) {
      this.addMessage('error', `Error refrescando contexto: ${error.message}`);
    }
  },
  
  clearChat() {
    this.messagesContainer.innerHTML = '';
    this.conversationHistory = [];
    this.showWelcomeMessage();
  }
};

// === DASHBOARD MEJORADO ===
const Dashboard = {
  initialized: false,
  widgets: new Map(),
  refreshInterval: null,
  
  async initialize() {
    console.log('📊 Inicializando dashboard homologado...');
    
    if (!SystemState.currentUser) {
      console.warn('⚠️ No hay usuario autenticado para el dashboard');
      return;
    }
    
    await this.setupDashboardLayout();
    await this.loadAllWidgets();
    this.startAutoRefresh();
    
    this.initialized = true;
    console.log('✅ Dashboard inicializado exitosamente');
  },
  
  async setupDashboardLayout() {
    const dashboardContainer = document.querySelector('.dashboard-content') || 
                              document.querySelector('.main-content');
    
    if (!dashboardContainer) {
      console.warn('⚠️ Container de dashboard no encontrado');
      return;
    }
    
    // Crear layout del dashboard mejorado
    dashboardContainer.innerHTML = `
      <div class="dashboard-header">
        <div class="user-welcome">
          <h1>Bienvenido, ${SystemState.currentUser.charAt(0).toUpperCase() + SystemState.currentUser.slice(1)}</h1>
          <p>Dashboard empresarial Red Soluciones ISP</p>
        </div>
        <div class="dashboard-actions">
          <button onclick="Dashboard.refreshAll()" class="btn btn-secondary">
            <i class="fas fa-sync-alt"></i> Refrescar
          </button>
          <button onclick="Dashboard.exportData()" class="btn btn-primary">
            <i class="fas fa-download"></i> Exportar
          </button>
        </div>
      </div>
      
      <div class="dashboard-insights" id="dashboardInsights">
        <!-- Insights automáticos aparecerán aquí -->
      </div>
      
      <div class="dashboard-grid">
        <div class="widget-container" id="businessMetricsWidget">
          <!-- Métricas de negocio -->
        </div>
        <div class="widget-container" id="personalKPIsWidget">
          <!-- KPIs personales -->
        </div>
        <div class="widget-container" id="incidentsWidget">
          <!-- Incidentes pendientes -->
        </div>
        <div class="widget-container" id="clientsOverviewWidget">
          <!-- Resumen de clientes -->
        </div>
      </div>
      
      <div class="dashboard-charts">
        <div class="chart-container" id="revenueChart">
          <!-- Gráfico de ingresos -->
        </div>
        <div class="chart-container" id="growthChart">
          <!-- Gráfico de crecimiento -->
        </div>
      </div>
    `;
  },
  
  async loadAllWidgets() {
    const dashboardData = SystemState.cache.dashboard;
    const insights = SystemState.cache.insights;
    
    if (!dashboardData) {
      console.warn('⚠️ No hay datos del dashboard disponibles');
      return;
    }
    
    try {
      // Cargar insights automáticos
      await this.loadInsightsWidget(insights);
      
      // Cargar widgets principales
      await Promise.all([
        this.loadBusinessMetricsWidget(dashboardData.global_metrics),
        this.loadPersonalKPIsWidget(dashboardData.personal_metrics),
        this.loadIncidentsWidget(dashboardData.quick_stats),
        this.loadClientsOverviewWidget(dashboardData.quick_stats)
      ]);
      
      console.log('✅ Todos los widgets cargados exitosamente');
      
    } catch (error) {
      console.error('❌ Error cargando widgets:', error);
    }
  },
  
  async loadInsightsWidget(insights) {
    const container = document.getElementById('dashboardInsights');
    if (!container || !insights || insights.length === 0) return;
    
    const insightsHTML = insights.map(insight => {
      const iconMap = {
        'warning': 'exclamation-triangle',
        'opportunity': 'lightbulb',
        'success': 'check-circle',
        'info': 'info-circle'
      };
      
      const colorMap = {
        'warning': '#f39c12',
        'opportunity': '#2ecc71',
        'success': '#27ae60',
        'info': '#3498db'
      };
      
      return `
        <div class="insight-card ${insight.type}" style="border-left-color: ${colorMap[insight.type]}">
          <div class="insight-header">
            <i class="fas fa-${iconMap[insight.type]}" style="color: ${colorMap[insight.type]}"></i>
            <span class="insight-title">${insight.title}</span>
            <span class="insight-impact ${insight.impact_level}">${insight.impact_level}</span>
          </div>
          <p class="insight-description">${insight.description}</p>
          <div class="insight-action">
            <strong>Acción recomendada:</strong> ${insight.recommended_action}
          </div>
        </div>
      `;
    }).join('');
    
    container.innerHTML = `
      <div class="insights-header">
        <h3><i class="fas fa-brain"></i> Insights Automáticos</h3>
        <span class="insights-count">${insights.length} insights generados</span>
      </div>
      <div class="insights-grid">
        ${insightsHTML}
      </div>
    `;
  },
  
  async loadBusinessMetricsWidget(globalMetrics) {
    const container = document.getElementById('businessMetricsWidget');
    if (!container || !globalMetrics) return;
    
    container.innerHTML = `
      <div class="widget-header">
        <h3><i class="fas fa-chart-line"></i> Métricas Globales</h3>
        <span class="widget-status">En tiempo real</span>
      </div>
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-value">${globalMetrics.total_clientes || 0}</div>
          <div class="metric-label">Total Clientes</div>
          <div class="metric-change">
            <i class="fas fa-arrow-up" style="color: #2ecc71"></i>
            <span>${globalMetrics.clientes_activos || 0} activos</span>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-value">$${(globalMetrics.ingresos_mensuales || 0).toLocaleString()}</div>
          <div class="metric-label">Ingresos Mensuales</div>
          <div class="metric-change">
            <i class="fas fa-dollar-sign" style="color: #f39c12"></i>
            <span>ARPU: $${(globalMetrics.arpu || 0).toFixed(2)}</span>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-value">${globalMetrics.incidentes_abiertos || 0}</div>
          <div class="metric-label">Incidentes Abiertos</div>
          <div class="metric-change ${globalMetrics.incidentes_abiertos > 10 ? 'negative' : 'positive'}">
            <i class="fas fa-${globalMetrics.incidentes_abiertos > 10 ? 'exclamation-triangle' : 'check-circle'}"></i>
            <span>${globalMetrics.incidentes_abiertos > 10 ? 'Requiere atención' : 'Bajo control'}</span>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-value">${(globalMetrics.churn_rate || 0).toFixed(1)}%</div>
          <div class="metric-label">Tasa de Churn</div>
          <div class="metric-change ${globalMetrics.churn_rate > 5 ? 'negative' : 'positive'}">
            <i class="fas fa-${globalMetrics.churn_rate > 5 ? 'arrow-down' : 'arrow-up'}"></i>
            <span>${globalMetrics.churn_rate > 5 ? 'Monitorear' : 'Excelente'}</span>
          </div>
        </div>
      </div>
    `;
  },
  
  startAutoRefresh() {
    // Refrescar dashboard cada 5 minutos
    this.refreshInterval = setInterval(async () => {
      await this.refreshAll();
    }, 5 * 60 * 1000);
  },
  
  async refreshAll() {
    console.log('🔄 Refrescando dashboard completo...');
    
    try {
      // Refrescar datos del sistema
      await SystemState.refreshSystemData();
      
      // Recargar widgets
      await this.loadAllWidgets();
      
      console.log('✅ Dashboard refrescado exitosamente');
      
    } catch (error) {
      console.error('❌ Error refrescando dashboard:', error);
    }
  },
  
  async exportData() {
    console.log('📤 Exportando datos del dashboard...');
    
    try {
      const dashboardData = SystemState.cache.dashboard;
      const insights = SystemState.cache.insights;
      
      const exportData = {
        usuario: SystemState.currentUser,
        fecha_exportacion: new Date().toISOString(),
        metricas_globales: dashboardData?.global_metrics,
        metricas_personales: dashboardData?.personal_metrics,
        insights: insights,
        sistema: dashboardData?.system_status
      };
      
      // Crear y descargar archivo JSON
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { 
        type: 'application/json' 
      });
      
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `dashboard_${SystemState.currentUser}_${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      console.log('✅ Datos exportados exitosamente');
      
    } catch (error) {
      console.error('❌ Error exportando datos:', error);
    }
  }
};

// === INICIALIZACIÓN DEL SISTEMA ===
document.addEventListener('DOMContentLoaded', async () => {
  console.log('🚀 Iniciando Red Soluciones ISP v4.0 Homologado...');
  
  try {
    // Inicializar sistema completo
    const initialized = await SystemState.initialize();
    
    if (initialized) {
      console.log('✅ Sistema homologado listo para usar');
    } else {
      throw new Error('Error en la inicialización del sistema');
    }
    
  } catch (error) {
    console.error('❌ Error crítico del sistema:', error);
    document.body.innerHTML = `
      <div class="error-screen">
        <div class="error-content">
          <i class="fas fa-exclamation-triangle" style="font-size: 4em; color: #e74c3c;"></i>
          <h2>Error del Sistema</h2>
          <p>No se pudo inicializar Red Soluciones ISP.</p>
          <button onclick="window.location.reload()" class="btn btn-primary">
            Recargar Página
          </button>
        </div>
      </div>
    `;
  }
});

// === UTILIDADES GLOBALES ===
window.RedSolucionesISP = {
  SystemState,
  UserAuth,
  EnhancedChat,
  Dashboard,
  version: '4.0 Homologado'
};
