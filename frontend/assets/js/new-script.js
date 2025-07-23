// new-script.js - Lógica para el nuevo dashboard/chat

const API_BASE = '/api';

// Estado global de la aplicación
const AppState = {
  isLoading: false,
  lastUpdate: null
};

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
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);
    
    const response = await fetch(`${API_BASE}/dashboard`, {
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const data = await response.json();
    
    // Actualizar la interfaz con los datos
    const totalClientsEl = document.getElementById('card-total-clients');
    const activeUsersEl = document.getElementById('card-active-users');
    
    if (totalClientsEl) {
      totalClientsEl.innerHTML = `
        <span class="card-number">${data.total_clients?.toLocaleString() || '--'}</span>
        <span class="card-label">Total de clientes</span>
      `;
    }
    
    if (activeUsersEl) {
      activeUsersEl.innerHTML = `
        <span class="card-number">${data.active_users?.toLocaleString() || '--'}</span>
        <span class="card-label">Usuarios activos</span>
      `;
    }
    
    // Actualizar el contador de clientes en el botón si existe
    const clientCountBadge = document.querySelector('.quick-link:nth-child(1) small');
    if (clientCountBadge && data.total_clients !== undefined) {
      clientCountBadge.textContent = `${data.total_clients.toLocaleString()} registrados`;
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
}

function setupChat() {
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
  
  // Mostrar mensaje del usuario
  const userMsg = document.createElement('div');
  userMsg.className = 'message user';
  userMsg.textContent = msg;
  chatMessages.appendChild(userMsg);
  chatInput.value = '';
  chatMessages.scrollTop = chatMessages.scrollHeight;
  
  // Mostrar indicador de "escribiendo..."
  const typingMsg = document.createElement('div');
  typingMsg.className = 'message agent';
  typingMsg.innerHTML = '<strong>Agent</strong><br>Escribiendo...';
  typingMsg.id = 'typing-indicator';
  chatMessages.appendChild(typingMsg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  
  // Llamar al backend (agente)
  fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: msg })
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
            <p><strong>Pago:</strong> $${client.Pago || 'No especificado'}</p>
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
