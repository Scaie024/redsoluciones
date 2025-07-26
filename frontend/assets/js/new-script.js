// new-script.js - Sistema homologado Red Soluciones ISP

const API_BASE = '/api';
const API_V2_BASE = '/api/v2'; // Nueva API homologada
const API_TIMEOUT = 15000;
const MAX_RETRIES = 3;

// === SISTEMA DE GESTIÓN DE ESTADO GLOBAL ===
const SystemState = {
  initialized: false,
  currentUser: null,
  sessionId: null,
  systemContext: null,
  lastSync: null,
  
  // Estado del sistema
  status: {
    context_engine: false,
    enhanced_agent: false,
    sheets_service: false
  },
  
  // Cache de datos
  cache: {
    dashboard: null,
    insights: null,
    entities: new Map()
  },
  
  // Listeners para cambios de estado
  listeners: new Set(),
  
  // Inicializar sistema completo
  async initialize() {
    console.log('🚀 Inicializando sistema homologado Red Soluciones ISP...');
    
    try {
      // 1. Verificar estado del sistema
      const systemStatus = await this.checkSystemStatus();
      if (!systemStatus.success) {
        throw new Error('Sistema no disponible');
      }
      
      // 2. Cargar usuarios disponibles
      await UserAuth.init();
      
      // 3. Marcar como inicializado
      this.initialized = true;
      this.notifyListeners('system_initialized', systemStatus);
      
      console.log('✅ Sistema homologado inicializado exitosamente');
      return true;
      
    } catch (error) {
      console.error('❌ Error inicializando sistema:', error);
      this.showErrorModal('Error del Sistema', 'No se pudo inicializar el sistema. Refresca la página.');
      return false;
    }
  },
  
  // Verificar estado del sistema backend
  async checkSystemStatus() {
    try {
      const response = await fetch(`${API_V2_BASE}/system/status`);
      const data = await response.json();
      
      this.status = {
        context_engine: data.entities_loaded > 0,
        enhanced_agent: data.status === 'operational',
        sheets_service: data.cache_health && Object.keys(data.cache_health.cached_sheets).length > 0
      };
      
      return data;
    } catch (error) {
      console.error('Error verificando estado del sistema:', error);
      return { success: false, error: error.message };
    }
  },
  
  // Cargar contexto completo para el usuario actual
  async loadUserContext(propietario) {
    try {
      console.log(`🧠 Cargando contexto completo para ${propietario}...`);
      
      const response = await fetch(`${API_V2_BASE}/context/${propietario}`);
      const data = await response.json();
      
      if (data.success) {
        this.systemContext = data.context;
        this.lastSync = new Date().toISOString();
        
        // Actualizar cache del dashboard
        await this.loadDashboardData(propietario);
        
        // Cargar insights automáticos
        await this.loadBusinessInsights(propietario);
        
        this.notifyListeners('context_loaded', this.systemContext);
        console.log('✅ Contexto cargado exitosamente');
        
        return this.systemContext;
      } else {
        throw new Error(data.error || 'Error cargando contexto');
      }
      
    } catch (error) {
      console.error(`❌ Error cargando contexto para ${propietario}:`, error);
      return null;
    }
  },
  
  // Cargar datos del dashboard mejorado
  async loadDashboardData(propietario) {
    try {
      const response = await fetch(`${API_V2_BASE}/dashboard/${propietario}`);
      const data = await response.json();
      
      if (data.success) {
        this.cache.dashboard = data.dashboard;
        this.notifyListeners('dashboard_updated', data.dashboard);
        return data.dashboard;
      }
    } catch (error) {
      console.error('Error cargando dashboard:', error);
    }
    return null;
  },
  
  // Cargar insights del negocio
  async loadBusinessInsights(propietario) {
    try {
      const response = await fetch(`${API_V2_BASE}/insights/${propietario}`);
      const data = await response.json();
      
      if (data.success) {
        this.cache.insights = data.insights;
        this.notifyListeners('insights_updated', data.insights);
        return data.insights;
      }
    } catch (error) {
      console.error('Error cargando insights:', error);
    }
    return [];
  },
  
  // Refrescar datos del sistema
  async refreshSystemData(sheetType = null) {
    try {
      console.log('🔄 Refrescando datos del sistema...');
      
      const response = await fetch(`${API_V2_BASE}/system/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sheet_type: sheetType })
      });
      
      const data = await response.json();
      
      if (data.success && this.currentUser) {
        // Recargar contexto después del refresh
        await this.loadUserContext(this.currentUser);
        console.log('✅ Datos refrescados exitosamente');
        this.notifyListeners('data_refreshed', data);
      }
      
      return data;
    } catch (error) {
      console.error('Error refrescando datos:', error);
      return { success: false, error: error.message };
    }
  },
  
  // Sistema de notificaciones
  addListener(callback) {
    this.listeners.add(callback);
  },
  
  removeListener(callback) {
    this.listeners.delete(callback);
  },
  
  notifyListeners(event, data) {
    this.listeners.forEach(callback => {
      try {
        callback(event, data);
      } catch (error) {
        console.error('Error en listener:', error);
      }
    });
  },
  
  // Modal de error
  showErrorModal(title, message) {
    const modal = document.createElement('div');
    modal.className = 'modal error-modal';
    modal.style.display = 'flex';
    
    modal.innerHTML = `
      <div class="modal-content error-content">
        <div class="error-header">
          <i class="fas fa-exclamation-triangle" style="color: #e74c3c;"></i>
          <h3>${title}</h3>
        </div>
        <p>${message}</p>
        <button onclick="this.closest('.modal').remove()" class="btn btn-primary">
          Entendido
        </button>
      </div>
    `;
    
    document.body.appendChild(modal);
  }
};

// === SISTEMA DE AUTENTICACIÓN MEJORADO ===
const UserAuth = {
  currentUser: null,
  sessionId: null,
  availableUsers: [],
  
  async init() {
    console.log('🔐 Inicializando autenticación homologada...');
    
    await this.loadAvailableUsers();
    
    const savedUser = localStorage.getItem('current_user');
    const savedSession = localStorage.getItem('session_id');
    
    if (savedUser && savedSession) {
      try {
        await this.loginUser(savedUser, savedSession);
      } catch (error) {
        console.warn('⚠️ Sesión anterior inválida');
        this.showUserSelection();
      }
    } else {
      this.showUserSelection();
    }
  },
  
  async loadAvailableUsers() {
    try {
      const response = await fetch(`${API_BASE}/auth/users`);
      const data = await response.json();
      
      if (data.success) {
        this.availableUsers = data.users;
        console.log('✅ Usuarios disponibles:', this.availableUsers.map(u => u.name));
      }
    } catch (error) {
      console.error('❌ Error cargando usuarios:', error);
      this.availableUsers = [
        { id: 'eduardo', name: 'Eduardo', icon: '👨‍💼', color: '#2563eb' },
        { id: 'omar', name: 'Omar', icon: '👤', color: '#dc2626' }
      ];
    }
  },
  
  showUserSelection() {
    const modal = document.createElement('div');
    modal.id = 'userSelectionModal';
    modal.className = 'modal user-selection-modal';
    modal.style.display = 'flex';
    
    modal.innerHTML = `
      <div class="modal-content user-selection-content">
        <div class="user-selection-header">
          <div class="company-logo">
            <i class="fas fa-wifi" style="color: #e74c3c; font-size: 2em;"></i>
            <h2>Red Soluciones ISP</h2>
            <span class="version-badge">v4.0 Homologado</span>
          </div>
          <h3>Selecciona tu perfil</h3>
          <p>Sistema empresarial completo con IA integrada</p>
        </div>
        <div class="user-options">
          ${this.availableUsers.map(user => `
            <button class="user-option" onclick="UserAuth.selectUser('${user.id}')" 
                    style="border-left: 4px solid ${user.color}">
              <div class="user-icon">${user.icon}</div>
              <div class="user-info">
                <div class="user-name">${user.name}</div>
                <div class="user-role">Propietario ISP</div>
                <div class="user-features">Dashboard • IA • Analytics</div>
              </div>
              <i class="fas fa-chevron-right"></i>
            </button>
          `).join('')}
        </div>
        <div class="user-selection-footer">
          <small>Sistema homologado con Google Sheets backend</small>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
  },
  
  async selectUser(userId) {
    try {
      console.log(`🔑 Iniciando sesión para ${userId}...`);
      
      const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          session_id: sessionId
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        await this.loginUser(userId, sessionId);
        document.getElementById('userSelectionModal')?.remove();
      } else {
        throw new Error(data.message || 'Error en autenticación');
      }
      
    } catch (error) {
      console.error('❌ Error seleccionando usuario:', error);
      SystemState.showErrorModal('Error de Autenticación', error.message);
    }
  },
  
  async loginUser(userId, sessionId) {
    this.currentUser = userId;
    this.sessionId = sessionId;
    
    // Guardar en localStorage
    localStorage.setItem('current_user', userId);
    localStorage.setItem('session_id', sessionId);
    
    // Actualizar estado global
    SystemState.currentUser = userId;
    SystemState.sessionId = sessionId;
    
    // Cargar contexto completo del usuario
    await SystemState.loadUserContext(userId);
    
    // Inicializar dashboard
    await Dashboard.initialize();
    
    // Inicializar chat
    await EnhancedChat.initialize();
    
    console.log(`✅ Usuario ${userId} autenticado exitosamente`);
    SystemState.notifyListeners('user_authenticated', { userId, sessionId });
  },
  
  async logout() {
    try {
      if (this.sessionId) {
        await fetch(`${API_BASE}/auth/logout`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: this.sessionId })
        });
      }
      
      // Limpiar estado
      this.currentUser = null;
      this.sessionId = null;
      SystemState.currentUser = null;
      SystemState.sessionId = null;
      SystemState.systemContext = null;
      
      localStorage.removeItem('current_user');
      localStorage.removeItem('session_id');
      
      // Mostrar selección de usuario nuevamente
      this.showUserSelection();
      
    } catch (error) {
      console.error('Error en logout:', error);
    }
  }
};
  
  // Seleccionar usuario
  async selectUser(userId) {
    try {
      const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      await this.loginUser(userId, sessionId);
      this.closeUserModal();
    } catch (error) {
      console.error('❌ Error seleccionando usuario:', error);
      alert('Error al iniciar sesión. Intenta de nuevo.');
    }
  },
  
  // Hacer login de usuario
  async loginUser(userId, sessionId = null) {
    try {
      if (!sessionId) {
        sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      }
      
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, session_id: sessionId })
      });
      
      const data = await response.json();
      
      if (data.success) {
        this.currentUser = data.user;
        this.sessionId = sessionId;
        
        // Guardar en localStorage
        localStorage.setItem('current_user', userId);
        localStorage.setItem('session_id', sessionId);
        localStorage.setItem('user_data', JSON.stringify(data.user));
        
        console.log('✅ Usuario autenticado:', this.currentUser);
        this.updateUIForUser();
        
        return data;
      } else {
        throw new Error(data.message || 'Error en autenticación');
      }
    } catch (error) {
      console.error('❌ Error en login:', error);
      throw error;
    }
  },
  
  // Actualizar UI con información del usuario
  updateUIForUser() {
    if (!this.currentUser) return;
    
    // Actualizar header con información del usuario
    const userInfoElement = document.getElementById('current-user-info');
    if (userInfoElement) {
      userInfoElement.innerHTML = `
        <div class="current-user" style="color: ${this.currentUser.color}">
          <span class="user-icon">${this.currentUser.icon}</span>
          <span class="user-name">${this.currentUser.name}</span>
          <button class="logout-btn" onclick="UserAuth.logout()" title="Cambiar usuario">
            <i class="fas fa-sign-out-alt"></i>
          </button>
        </div>
      `;
    }
    
    // Enviar mensaje de bienvenida al chat
    if (typeof sendMessage === 'function') {
      setTimeout(() => {
        document.getElementById('chat-input').value = 'Hola';
        sendMessage();
      }, 1000);
    }
  },
  
  // Cerrar modal de selección
  closeUserModal() {
    const modal = document.getElementById('userSelectionModal');
    if (modal) {
      modal.remove();
    }
  },
  
  // Cerrar sesión
  async logout() {
    try {
      if (this.sessionId) {
        await fetch(`${API_BASE}/auth/logout`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: this.sessionId })
        });
      }
    } catch (error) {
      console.error('❌ Error en logout:', error);
    }
    
    // Limpiar estado local
    this.currentUser = null;
    this.sessionId = null;
    localStorage.removeItem('current_user');
    localStorage.removeItem('session_id');
    localStorage.removeItem('user_data');
    
    // Mostrar selección de usuario nuevamente
    this.showUserSelection();
  },
  
  // Obtener contexto de usuario para envío al servidor
  getUserContext() {
    if (!this.currentUser) return null;
    
    return {
      user_id: this.currentUser.user_id,
      user_name: this.currentUser.name,
      session_id: this.sessionId
    };
  }
};

// Función para fetch con timeout y reintentos
async function fetchWithTimeout(url, options = {}, timeout = API_TIMEOUT, retries = MAX_RETRIES) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  
  const fetchOptions = {
    ...options,
    signal: controller.signal
  };
  
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await fetch(url, fetchOptions);
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return response;
      
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (attempt === retries) {
        // Último intento fallido
        if (error.name === 'AbortError') {
          throw new Error(`Timeout: La operación tardó más de ${timeout/1000} segundos`);
        }
        throw error;
      }
      
      // Esperar antes del siguiente intento (backoff exponencial)
      await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
    }
  }
}

// Estado global de la aplicación
const AppState = {
  isLoading: false,
  lastUpdate: null
};

// Función para manejar errores de API con más detalle
function handleApiError(error, action) {
  console.error(`Error al ${action}:`, error);
  
  let errorMessage = `Error al ${action}`;
  let errorType = 'unknown';
  
  // Determinar tipo de error
  if (error.name === 'TypeError' && error.message.includes('fetch')) {
    errorMessage = `No se pudo conectar al servidor. Verifica tu conexión.`;
    errorType = 'network';
  } else if (error.status === 404) {
    errorMessage = `Recurso no encontrado. El endpoint puede no existir.`;
    errorType = 'not_found';
  } else if (error.status >= 500) {
    errorMessage = `Error del servidor. Intenta de nuevo en unos momentos.`;
    errorType = 'server';
  } else if (error.status === 422) {
    errorMessage = `Datos inválidos. Verifica la información ingresada.`;
    errorType = 'validation';
  }
  
  // Mostrar notificación de error mejorada
  const notification = document.createElement('div');
  notification.className = `error-notification error-${errorType}`;
  notification.innerHTML = `
    <div class="error-content">
      <i class="fas fa-exclamation-triangle"></i>
      <div class="error-text">
        <strong>Error:</strong> ${errorMessage}
        <div class="error-details">Acción: ${action}</div>
      </div>
      <button class="error-close" onclick="this.parentElement.remove()">&times;</button>
    </div>
  `;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #ef4444;
    color: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 9999;
    font-size: 0.9rem;
    max-width: 350px;
    animation: slideIn 0.3s ease;
  `;
  
  document.body.appendChild(notification);
  
  // Auto-remove después de 8 segundos
  setTimeout(() => {
    if (notification.parentNode) {
      notification.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    }
  }, 8000);
  
  // Log detallado para debugging
  console.group(`🚨 Error Details - ${action}`);
  console.log('Error Type:', errorType);
  console.log('Original Error:', error);
  console.log('Timestamp:', new Date().toISOString());
  console.groupEnd();
}

// Función para validar datos de cliente/prospecto
function validateClientData(data, type = 'cliente') {
  const errors = [];
  
  // Validar nombre
  if (!data.Nombre || data.Nombre.trim().length < 2) {
    errors.push('El nombre debe tener al menos 2 caracteres');
  }
  
  // Validar teléfono
  if (data.Teléfono) {
    const phoneRegex = /^[\d\s\-\+\(\)]{10,15}$/;
    if (!phoneRegex.test(data.Teléfono)) {
      errors.push('El teléfono debe tener entre 10-15 dígitos');
    }
  }
  
  // Validar email
  if (data.Email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.Email)) {
      errors.push('El email no tiene un formato válido');
    }
  }
  
  // Validar zona
  const validZones = ['Norte', 'Sur', 'Centro', 'Este', 'Oeste', 'Salamanca', 'Bajio', 'Industrial', 'Residencial'];
  if (data.Zona && !validZones.includes(data.Zona)) {
    errors.push(`La zona debe ser una de: ${validZones.join(', ')}`);
  }
  
  // Validar pago (solo para clientes)
  if (type === 'cliente' && data.Pago) {
    const payment = parseFloat(data.Pago);
    if (isNaN(payment) || payment < 0) {
      errors.push('El pago debe ser un número positivo');
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors: errors
  };
}

// Función para mostrar errores de validación
function showValidationErrors(errors) {
  const errorContainer = document.createElement('div');
  errorContainer.className = 'validation-errors';
  errorContainer.innerHTML = `
    <div class="validation-content">
      <i class="fas fa-exclamation-circle"></i>
      <div class="validation-text">
        <strong>Errores de validación:</strong>
        <ul>
          ${errors.map(error => `<li>${error}</li>`).join('')}
        </ul>
      </div>
      <button class="validation-close" onclick="this.parentElement.remove()">&times;</button>
    </div>
  `;
  errorContainer.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #f59e0b;
    color: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 9999;
    font-size: 0.9rem;
    max-width: 350px;
  `;
  
  document.body.appendChild(errorContainer);
  
  setTimeout(() => {
    if (errorContainer.parentNode) {
      errorContainer.parentNode.removeChild(errorContainer);
    }
  }, 6000);
}

// Función para sanitizar datos de entrada
function sanitizeData(data) {
  const sanitized = {};
  
  for (const [key, value] of Object.entries(data)) {
    if (typeof value === 'string') {
      // Limpiar espacios y caracteres peligrosos
      sanitized[key] = value.trim().replace(/[<>\"']/g, '');
    } else {
      sanitized[key] = value;
    }
  }
  
  return sanitized;
}

// Función mejorada para envío de datos con validación
async function sendDataWithValidation(url, data, type = 'cliente') {
  try {
    // 1. Sanitizar datos
    const sanitizedData = sanitizeData(data);
    
    // 2. Validar datos
    const validation = validateClientData(sanitizedData, type);
    if (!validation.isValid) {
      showValidationErrors(validation.errors);
      return { success: false, errors: validation.errors };
    }
    
    // 3. Enviar datos
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(sanitizedData)
    });
    
    // 4. Verificar respuesta
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const result = await response.json();
    return result;
    
  } catch (error) {
    handleApiError(error, `enviar ${type}`);
    return { success: false, error: error.message };
  }
}

// Función para mostrar notificaciones de éxito mejoradas
function showSuccessNotification(message, details = '') {
  const notification = document.createElement('div');
  notification.className = 'success-notification';
  notification.innerHTML = `
    <div class="success-content">
      <i class="fas fa-check-circle"></i>
      <div class="success-text">
        <strong>¡Éxito!</strong> ${message}
        ${details ? `<div class="success-details">${details}</div>` : ''}
      </div>
      <button class="success-close" onclick="this.parentElement.remove()">&times;</button>
    </div>
  `;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #10b981;
    color: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 9999;
    font-size: 0.9rem;
    max-width: 350px;
    animation: slideIn 0.3s ease;
  `;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    if (notification.parentNode) {
      notification.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    }
  }, 5000);
}

// Función para mostrar notificaciones de éxito
function showSuccessNotification(message) {
  const notification = document.createElement('div');
  notification.className = 'success-notification';
  notification.innerHTML = `
    <i class="fas fa-check-circle"></i>
    ${message}
  `;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #10b981;
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 9999;
    font-size: 0.9rem;
  `;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, 3000);
}

// Función para activar/desactivar el chat IA
function toggleAIChat() {
  const chatPanel = document.getElementById('chat-panel');
  const mainContainer = document.querySelector('.main-container');
  
  if (chatPanel.style.display === 'none' || !chatPanel.style.display) {
    chatPanel.style.display = 'flex';
    mainContainer.classList.add('chat-expanded');
  } else {
    chatPanel.style.display = 'none';
    mainContainer.classList.remove('chat-expanded');
  }
}

// Función para enviar preguntas sugeridas
function sendSuggestedQuestion(question) {
  const chatInput = document.getElementById('chat-input');
  if (chatInput) {
    chatInput.value = question;
    sendMessage();
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  try {
    AppState.isLoading = true;
    await Promise.all([
      loadDashboard(),
      setupChat()
    ]);
  } catch (error) {
    handleApiError(error, 'inicializar la aplicación');
  } finally {
    AppState.isLoading = false;
    AppState.lastUpdate = new Date();
  }
});

/**
 * Actualiza el dashboard con los datos más recientes
 * @returns {Promise<void>}
 */
async function loadDashboard() {
  if (AppState.isLoading) return;
  
  AppState.isLoading = true;
  const loadingElements = document.querySelectorAll('.card-number');
  loadingElements.forEach(el => {
    el.textContent = '...';
    el.classList.add('loading');
  });

  try {
    const response = await fetch(`${API_BASE}/dashboard`);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const data = await response.json();

    // Actualizar las tarjetas del dashboard
    const totalClientsEl = document.getElementById('card-total-clients');
    const activeUsersEl = document.getElementById('card-active-users');
    const monthlyRevenueEl = document.getElementById('card-monthly-revenue');
    const satisfactionEl = document.getElementById('card-satisfaction');
    
    if (totalClientsEl) {
      totalClientsEl.innerHTML = `
        <span class="card-number">${data.total_clients?.toLocaleString() || '--'}</span>
        <span class="card-label">Total de Clientes</span>
      `;
    }
    
    if (activeUsersEl) {
      activeUsersEl.innerHTML = `
        <span class="card-number">${data.active_users?.toLocaleString() || '--'}</span>
        <span class="card-label">Usuarios Activos</span>
      `;
    }

    if (monthlyRevenueEl) {
      monthlyRevenueEl.innerHTML = `
        <span class="card-number">$${(data.monthly_revenue || 0).toLocaleString()}</span>
        <span class="card-label">Ingresos Mensuales</span>
      `;
    }

    if (satisfactionEl) {
      satisfactionEl.innerHTML = `
        <span class="card-number">${data.satisfaction || '--'}%</span>
        <span class="card-label">Satisfacción</span>
      `;
    }
    
    // Actualizar el estado del sistema
    const statusIndicator = document.getElementById('system-status-indicator');
    const statusText = document.getElementById('system-status-text');
    const lastUpdateTime = document.getElementById('last-update-time');
    
    if (statusIndicator) {
      statusIndicator.style.color = '#10b981'; // Verde
    }
    
    if (statusText) {
      statusText.textContent = 'Sistema Activo';
    }
    
    if (lastUpdateTime) {
      lastUpdateTime.textContent = new Date().toLocaleTimeString();
    }
    
    AppState.lastUpdate = new Date();
    
  } catch (error) {
    handleApiError(error, 'cargar el dashboard');
    
    // Restaurar estado de error
    const numberElements = document.querySelectorAll('.card-number');
    numberElements.forEach(el => {
      el.textContent = '--';
      el.classList.remove('loading');
    });
  } finally {
    AppState.isLoading = false;
    loadingElements.forEach(el => el.classList.remove('loading'));
  }
}function setupChat() {
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');
  document.querySelector('.chat-input-row').addEventListener('submit', function(e) {
    e.preventDefault();
    sendMessage();
  });
}

function sendMessage() {
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');
  const msg = chatInput.value.trim();
  if (!msg) return;
  
  // Verificar autenticación
  if (!UserAuth.currentUser) {
    console.warn('⚠️ Usuario no autenticado, solicitando login...');
    UserAuth.showUserSelection();
    return;
  }
  
  // Mostrar mensaje del usuario
  const userMsg = document.createElement('div');
  userMsg.className = 'message user';
  userMsg.innerHTML = `
    <div class="message-header">
      <span class="user-icon" style="color: ${UserAuth.currentUser.color}">
        ${UserAuth.currentUser.icon}
      </span>
      <strong>${UserAuth.currentUser.name}</strong>
    </div>
    <div class="message-content">${msg}</div>
  `;
  chatMessages.appendChild(userMsg);
  chatInput.value = '';
  chatMessages.scrollTop = chatMessages.scrollHeight;
  
  // Mostrar indicador de "escribiendo..."
  const typingMsg = document.createElement('div');
  typingMsg.className = 'message agent';
  typingMsg.innerHTML = '<strong>🤖 Agente</strong><br>Escribiendo...';
  typingMsg.id = 'typing-indicator';
  chatMessages.appendChild(typingMsg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  
  // Preparar datos del mensaje con contexto de usuario
  const messageData = {
    message: msg,
    ...UserAuth.getUserContext()
  };
  
  // Llamar al backend (agente) con contexto de usuario
  fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(messageData)
  })
    .then(res => {
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }
      return res.json();
    })
    .then(data => {
      // Remover indicador de escribiendo
      const typingIndicator = document.getElementById('typing-indicator');
      if (typingIndicator) {
        typingIndicator.remove();
      }
      
      // Mostrar respuesta del agente
      const agentMsg = document.createElement('div');
      agentMsg.className = 'message agent';
      
      // Formatear la respuesta para que se vea mejor
      let response = data.response || 'Sin respuesta del agente.';
      
      // Convertir markdown básico a HTML
      response = response
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
      
      agentMsg.innerHTML = `<strong>Agent</strong><br>${response}`;
      chatMessages.appendChild(agentMsg);
      chatMessages.scrollTop = chatMessages.scrollHeight;
      
      // Actualizar dashboard después de cualquier consulta
      loadDashboard();
    })
    .catch(err => {
      console.error('Error en chat:', err);
      
      // Remover indicador de escribiendo
      const typingIndicator = document.getElementById('typing-indicator');
      if (typingIndicator) {
        typingIndicator.remove();
      }
      
      // Mostrar error
      const agentMsg = document.createElement('div');
      agentMsg.className = 'message agent';
      agentMsg.innerHTML = `<strong>Agent</strong><br>Error de conexión: ${err.message}. Verifica que el servidor esté funcionando.`;
      chatMessages.appendChild(agentMsg);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    });
}

// Funciones para modales
function showClients() {
  document.getElementById('clients-modal').style.display = 'flex';
  loadClients();
}

function showProspects() {
  document.getElementById('prospects-modal').style.display = 'flex';
  loadProspects();
}

function closeModal(modalId) {
  document.getElementById(modalId).style.display = 'none';
}

function loadClients() {
  const clientsList = document.getElementById('clients-list');
  clientsList.innerHTML = 'Cargando clientes...';
  
  fetch(`${API_BASE}/clients`)
    .then(res => res.json())
    .then(clients => {
      if (clients.length === 0) {
        clientsList.innerHTML = '<p>No hay clientes registrados.</p>';
        return;
      }
      
      let html = '';
      clients.forEach(client => {
        const pkg = client.paquete_info || {};
        html += `
          <div class="client-item">
            <h4>${client.Nombre || 'Sin nombre'}</h4>
            <p><strong>Email:</strong> ${client.Email || 'No especificado'}</p>
            <p><strong>Teléfono:</strong> ${client.Teléfono || 'No especificado'}</p>
            <p><strong>Zona:</strong> ${client.Zona || 'No especificada'}</p>
            <p><strong>Pago:</strong> $${(client.Pago || 0).toLocaleString()}</p>
            <p><strong>Paquete:</strong> ${pkg.speed || 'No determinado'} (${pkg.status || 'Sin clasificar'})</p>
          </div>
        `;
      });
      clientsList.innerHTML = html;
    })
    .catch(err => {
      console.error('Error cargando clientes:', err);
      clientsList.innerHTML = '<p>Error al cargar los clientes.</p>';
    });
}

function loadProspects() {
  const prospectsList = document.getElementById('prospects-list');
  prospectsList.innerHTML = 'Cargando prospectos...';
  
  fetch(`${API_BASE}/prospects`)
    .then(res => res.json())
    .then(prospects => {
      if (prospects.length === 0) {
        prospectsList.innerHTML = '<p>No hay prospectos pendientes de contactar.</p>';
        return;
      }
      
      let html = '';
      prospects.forEach(prospect => {
        html += `
          <div class="prospect-item">
            <h4>${prospect.Nombre || 'Sin nombre'}</h4>
            <p><strong>Email:</strong> ${prospect.Email || 'No especificado'}</p>
            <p><strong>Teléfono:</strong> ${prospect.Teléfono || 'No especificado'}</p>
            <p><strong>Zona:</strong> ${prospect.Zona || 'No especificada'}</p>
            <p><strong>Estado:</strong> ${prospect.Estado || 'Prospecto'}</p>
            <p><strong>Acción:</strong> ${prospect.Accion || 'Contactar'}</p>
          </div>
        `;
      });
      prospectsList.innerHTML = html;
    })
    .catch(err => {
      console.error('Error cargando prospectos:', err);
      prospectsList.innerHTML = '<p>Error al cargar los prospectos.</p>';
    });
}

function searchClients() {
  const searchTerm = document.getElementById('client-search').value.trim();
  const clientsList = document.getElementById('clients-list');
  
  if (!searchTerm) {
    loadClients();
    return;
  }
  
  clientsList.innerHTML = 'Buscando...';
  
  fetch(`${API_BASE}/clients?search=${encodeURIComponent(searchTerm)}`)
    .then(res => res.json())
    .then(clients => {
      if (clients.length === 0) {
        clientsList.innerHTML = '<p>No se encontraron clientes con ese criterio.</p>';
        return;
      }
      
      let html = '';
      clients.forEach(client => {
        const pkg = client.paquete_info || {};
        html += `
          <div class="client-item">
            <h4>${client.Nombre || 'Sin nombre'}</h4>
            <p><strong>Email:</strong> ${client.Email || 'No especificado'}</p>
            <p><strong>Teléfono:</strong> ${client.Teléfono || 'No especificado'}</p>
            <p><strong>Zona:</strong> ${client.Zona || 'No especificada'}</p>
            <p><strong>Pago:</strong> $${client.Pago || 'No especificado'}</p>
            <p><strong>Paquete:</strong> ${pkg.speed || 'No determinado'} (${pkg.status || 'Sin clasificar'})</p>
          </div>
        `;
      });
      clientsList.innerHTML = html;
    })
    .catch(err => {
      console.error('Error buscando clientes:', err);
      clientsList.innerHTML = '<p>Error al buscar clientes.</p>';
    });
}

// Cerrar modales al hacer clic fuera
window.onclick = function(event) {
  const modals = document.querySelectorAll('.modal');
  modals.forEach(modal => {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });
}

// Función para agregar cliente desde el panel de administración
async function addClient() {
  const form = document.getElementById('add-client-form');
  if (!form) return;
  
  const formData = new FormData(form);
  const clientData = {
    name: formData.get('name'),
    email: formData.get('email'),
    phone: formData.get('phone'),
    zone: formData.get('zone'),
    monthly_fee: formData.get('monthly_fee'),
    notes: formData.get('notes')
  };
  
  // Validación básica
  if (!clientData.name || !clientData.email) {
    alert('Nombre y email son obligatorios');
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/clients`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(clientData)
    });
    
    const result = await response.json();
    
    if (result.success) {
      showSuccessNotification('Cliente agregado correctamente');
      form.reset();
      // Actualizar el dashboard si estamos en esa página
      if (typeof loadDashboard === 'function') {
        loadDashboard();
      }
    } else {
      alert(`Error: ${result.message}`);
    }
  } catch (error) {
    handleApiError(error, 'agregar cliente');
  }
}

// Función para buscar clientes con filtros
async function searchClients() {
  const searchTerm = document.getElementById('client-search')?.value.trim();
  const clientsList = document.getElementById('clients-list');
  
  if (!clientsList) return;
  
  if (!searchTerm) {
    loadClients();
    return;
  }
  
  clientsList.innerHTML = 'Buscando...';
  
  try {
    const response = await fetch(`${API_BASE}/clients?search=${encodeURIComponent(searchTerm)}`);
    const clients = await response.json();
    
    if (clients.length === 0) {
      clientsList.innerHTML = '<p>No se encontraron clientes con ese criterio.</p>';
      return;
    }
    
    let html = '';
    clients.forEach(client => {
      const pkg = client.paquete_info || {};
      html += `
        <div class="client-item">
          <h4>${client.Nombre || 'Sin nombre'}</h4>
          <p><strong>Email:</strong> ${client.Email || 'No especificado'}</p>
          <p><strong>Teléfono:</strong> ${client.Teléfono || 'No especificado'}</p>
          <p><strong>Zona:</strong> ${client.Zona || 'No especificada'}</p>
          <p><strong>Pago:</strong> $${(client.Pago || 0).toLocaleString()}</p>
          <p><strong>Paquete:</strong> ${pkg.speed || 'No determinado'} (${pkg.status || 'Sin clasificar'})</p>
        </div>
      `;
    });
    clientsList.innerHTML = html;
  } catch (error) {
    handleApiError(error, 'buscar clientes');
    clientsList.innerHTML = '<p>Error al buscar clientes.</p>';
  }
}

// Auto-actualizar el dashboard cada 30 segundos
setInterval(() => {
  if (typeof loadDashboard === 'function' && !AppState.isLoading) {
    loadDashboard();
  }
}, 30000);
