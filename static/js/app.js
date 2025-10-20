// Funciones globales de la aplicación

// Formatear moneda
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
        minimumFractionDigits: 2
    }).format(amount);
}

// Formatear fecha
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Mostrar spinner de carga
function showLoading() {
    document.getElementById('loadingSpinner').style.display = 'flex';
}

// Ocultar spinner de carga
function hideLoading() {
    document.getElementById('loadingSpinner').style.display = 'none';
}

// Mostrar notificación toast moderna
function showMessage(message, type = 'info', duration = 4000) {
    const container = document.getElementById('notificationContainer');
    
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.setAttribute('role', 'alert');
    notification.setAttribute('aria-live', 'polite');
    
    // Definir iconos y títulos según el tipo
    const config = {
        success: { icon: '✅', title: 'Éxito', color: '#10b981' },
        error: { icon: '❌', title: 'Error', color: '#ef4444' },
        warning: { icon: '⚠️', title: 'Advertencia', color: '#f59e0b' },
        info: { icon: 'ℹ️', title: 'Información', color: '#3b82f6' }
    };
    
    const { icon, title, color } = config[type] || config.info;
    
    // Contenido de la notificación
    notification.innerHTML = `
        <div class="notification-icon" style="color: ${color}">${icon}</div>
        <div class="notification-content">
            <div class="notification-title">${title}</div>
            <div class="notification-message">${message}</div>
        </div>
        <button class="notification-close" onclick="closeNotification(this)" aria-label="Cerrar notificación">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
        </button>
        <div class="notification-progress"></div>
    `;
    
    // Agregar al contenedor
    container.appendChild(notification);
    
    // Animar entrada
    setTimeout(() => {
        notification.classList.add('notification-show');
    }, 10);
    
    // Animar barra de progreso
    const progressBar = notification.querySelector('.notification-progress');
    progressBar.style.animation = `notification-progress ${duration}ms linear`;
    
    // Auto-remover después de la duración especificada
    let timeoutId = setTimeout(() => {
        closeNotification(notification.querySelector('.notification-close'));
    }, duration);
    
    // Pausar/reanudar en hover
    notification.addEventListener('mouseenter', () => {
        progressBar.style.animationPlayState = 'paused';
        clearTimeout(timeoutId);
    });
    
    notification.addEventListener('mouseleave', () => {
        progressBar.style.animationPlayState = 'running';
        const progressElement = notification.querySelector('.notification-progress');
        const computedStyle = window.getComputedStyle(progressElement);
        const currentWidth = parseFloat(computedStyle.width);
        const totalWidth = notification.offsetWidth;
        const remainingPercentage = 1 - (currentWidth / totalWidth);
        const remainingTime = duration * remainingPercentage;
        
        timeoutId = setTimeout(() => {
            closeNotification(notification.querySelector('.notification-close'));
        }, remainingTime > 100 ? remainingTime : 100);
    });
    
    // Soporte para teclado
    notification.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeNotification(notification.querySelector('.notification-close'));
        }
    });
}

// Cerrar notificación
function closeNotification(closeBtn) {
    const notification = closeBtn.closest('.notification');
    notification.classList.add('notification-hide');
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

// Funciones auxiliares para diferentes tipos de notificaciones
function showSuccess(message, duration = 3000) {
    showMessage(message, 'success', duration);
}

function showError(message, duration = 5000) {
    showMessage(message, 'error', duration);
}

function showWarning(message, duration = 4000) {
    showMessage(message, 'warning', duration);
}

function showInfo(message, duration = 4000) {
    showMessage(message, 'info', duration);
}

// Cerrar sesión
async function logout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        try {
            const response = await fetch('/api/logout', {
                method: 'POST'
            });
            
            if (response.ok) {
                window.location.href = '/login';
            } else {
                showMessage('No se pudo cerrar la sesión correctamente. Inténtalo nuevamente.', 'error');
            }
        } catch (error) {
            showMessage('Problema de conexión. Verifica tu internet e inténtalo nuevamente.', 'error');
        }
    }
}

// Navegación móvil
function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    const navToggle = document.getElementById('navToggle');
    
    navMenu.classList.toggle('active');
    navToggle.classList.toggle('active');
}

// Event listeners globales
document.addEventListener('DOMContentLoaded', function() {
    // Cerrar modal al hacer clic en la X
    const messageModal = document.getElementById('messageModal');
    const closeBtn = messageModal.querySelector('.close');
    
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            messageModal.style.display = 'none';
        });
    }
    
    // Cerrar modal al hacer clic fuera
    window.addEventListener('click', function(e) {
        if (e.target === messageModal) {
            messageModal.style.display = 'none';
        }
    });
    
    // Toggle móvil
    const navToggle = document.getElementById('navToggle');
    if (navToggle) {
        navToggle.addEventListener('click', toggleMobileMenu);
    }
    
    // Cerrar menú móvil al hacer clic en un enlace
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            const navMenu = document.getElementById('navMenu');
            if (navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                document.getElementById('navToggle').classList.remove('active');
            }
        });
    });
});

// Detectar si está offline
function isOnline() {
    return navigator.onLine;
}

// Manejar estado offline
window.addEventListener('online', function() {
    showMessage('¡Conexión restaurada! Todos los datos están actualizados.', 'success', 3000);
});

window.addEventListener('offline', function() {
    showMessage('😑 Sin conexión a internet. La aplicación seguirá funcionando con datos guardados.', 'warning', 5000);
});

// Utilidades para PWA
function isInstallable() {
    return 'serviceWorker' in navigator && 'PushManager' in window;
}

// Agregar estilos CSS dinámicos para mensajes
const messageStyles = `
    .message-content {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .message-success {
        background-color: #dcfce7;
        border-left: 4px solid #10b981;
        color: #065f46;
    }
    
    .message-error {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        color: #991b1b;
    }
    
    .message-info {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        color: #1e3a8a;
    }
    
    .message-warning {
        background-color: #fefce8;
        border-left: 4px solid #f59e0b;
        color: #92400e;
    }
    
    .message-content h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .message-content p {
        margin: 0;
        line-height: 1.5;
    }
`;

// Agregar estilos al head
if (!document.getElementById('messageStyles')) {
    const style = document.createElement('style');
    style.id = 'messageStyles';
    style.textContent = messageStyles;
    document.head.appendChild(style);
}

// Función para manejar errores de red
function handleNetworkError(error) {
    console.error('Error de red:', error);
    if (!isOnline()) {
        showMessage('Sin conexión a internet. Algunos datos pueden no estar actualizados.', 'warning');
    } else {
        showMessage('Error de conexión con el servidor. Intenta nuevamente.', 'error');
    }
}

// Función para validar formularios
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#ef4444';
            isValid = false;
        } else {
            field.style.borderColor = '#e2e8f0';
        }
    });
    
    return isValid;
}

// Función para limpiar formularios
function clearForm(formElement) {
    const inputs = formElement.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        if (input.type !== 'hidden') {
            input.value = '';
            input.style.borderColor = '#e2e8f0';
        }
    });
}

// Función para debounce (útil para búsquedas)
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Función para guardar datos en localStorage (para modo offline)
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
        console.warn('No se pudo guardar en localStorage:', error);
    }
}

// Función para obtener datos de localStorage
function getFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (error) {
        console.warn('No se pudo leer de localStorage:', error);
        return null;
    }
}

// Función para limpiar localStorage
function clearLocalStorage() {
    try {
        const keysToKeep = ['theme', 'language']; // Mantener algunas preferencias
        const keys = Object.keys(localStorage);
        
        keys.forEach(key => {
            if (!keysToKeep.includes(key)) {
                localStorage.removeItem(key);
            }
        });
    } catch (error) {
        console.warn('No se pudo limpiar localStorage:', error);
    }
}

// Función para formatear números
function formatNumber(number) {
    return new Intl.NumberFormat('es-MX').format(number);
}

// Función para capitalizar texto
function capitalize(text) {
    return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}

// Función para truncar texto
function truncateText(text, maxLength) {
    if (text.length <= maxLength) {
        return text;
    }
    return text.slice(0, maxLength - 3) + '...';
}

// Exportar funciones para uso global
window.FinanzasApp = {
    formatCurrency,
    formatDate,
    showLoading,
    hideLoading,
    showMessage,
    logout,
    isOnline,
    handleNetworkError,
    validateForm,
    clearForm,
    debounce,
    saveToLocalStorage,
    getFromLocalStorage,
    clearLocalStorage,
    formatNumber,
    capitalize,
    truncateText
};