/* ========================================
   JAVASCRIPT ESPECÍFICO PARA AUTENTICACIÓN
   (Login y Register)
======================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades de autenticación
    initAuthFeatures();
});

function initAuthFeatures() {
    // Configurar formularios
    setupFormValidation();
    
    // Configurar mensajes
    setupMessages();
    
    // Configurar animaciones
    setupAnimations();
    
    // Configurar validación en tiempo real
    setupRealTimeValidation();
}

/* ========================================
   VALIDACIÓN DE FORMULARIOS
======================================== */

function setupFormValidation() {
    const forms = document.querySelectorAll('.auth-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                return false;
            }
            
            // Mostrar estado de carga
            showLoadingState(this);
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required]');
    
    // Limpiar errores previos
    clearFormErrors(form);
    
    inputs.forEach(input => {
        if (!validateInput(input)) {
            isValid = false;
        }
    });
    
    // Validación específica para registro
    if (form.classList.contains('register-form')) {
        if (!validatePasswordMatch(form)) {
            isValid = false;
        }
    }
    
    return isValid;
}

function validateInput(input) {
    const value = input.value.trim();
    const type = input.type;
    let isValid = true;
    let errorMessage = '';
    
    // Validación básica de campo requerido
    if (input.hasAttribute('required') && !value) {
        errorMessage = 'Este campo es obligatorio';
        isValid = false;
    }
    
    // Validación de email
    if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            errorMessage = 'Ingresa un email válido';
            isValid = false;
        }
    }
    
    // Validación de contraseña
    if (type === 'password' && value) {
        if (value.length < 8) {
            errorMessage = 'La contraseña debe tener al menos 8 caracteres';
            isValid = false;
        }
    }
    
    // Validación de nombre de usuario
    if (input.name === 'username' && value) {
        const usernameRegex = /^[a-zA-Z0-9_]+$/;
        if (!usernameRegex.test(value)) {
            errorMessage = 'El nombre de usuario solo puede contener letras, números y guiones bajos';
            isValid = false;
        }
        if (value.length < 3) {
            errorMessage = 'El nombre de usuario debe tener al menos 3 caracteres';
            isValid = false;
        }
    }
    
    if (!isValid) {
        showInputError(input, errorMessage);
    } else {
        showInputSuccess(input);
    }
    
    return isValid;
}

function validatePasswordMatch(form) {
    const password1 = form.querySelector('input[name="password1"]');
    const password2 = form.querySelector('input[name="password2"]');
    
    if (password1 && password2) {
        if (password1.value !== password2.value) {
            showInputError(password2, 'Las contraseñas no coinciden');
            return false;
        }
    }
    
    return true;
}

/* ========================================
   VALIDACIÓN EN TIEMPO REAL
======================================== */

function setupRealTimeValidation() {
    const inputs = document.querySelectorAll('.auth-form input');
    
    inputs.forEach(input => {
        // Validar al perder el foco
        input.addEventListener('blur', function() {
            validateInput(this);
        });
        
        // Validar al escribir (con debounce)
        let timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                if (this.value.trim()) {
                    validateInput(this);
                }
            }, 500);
        });
    });
}

/* ========================================
   GESTIÓN DE ERRORES Y ÉXITO
======================================== */

function showInputError(input, message) {
    const formGroup = input.closest('.form-group');
    const existingError = formGroup.querySelector('.form-errors');
    
    // Remover error existente
    if (existingError) {
        existingError.remove();
    }
    
    // Agregar clase de error
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
    
    // Crear elemento de error
    const errorElement = document.createElement('div');
    errorElement.className = 'form-errors';
    errorElement.textContent = message;
    
    // Insertar después del input
    input.parentNode.insertBefore(errorElement, input.nextSibling);
}

function showInputSuccess(input) {
    const formGroup = input.closest('.form-group');
    const existingError = formGroup.querySelector('.form-errors');
    
    // Remover error existente
    if (existingError) {
        existingError.remove();
    }
    
    // Agregar clase de éxito
    input.classList.add('is-valid');
    input.classList.remove('is-invalid');
}

function clearFormErrors(form) {
    const errors = form.querySelectorAll('.form-errors');
    errors.forEach(error => error.remove());
    
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        input.classList.remove('is-invalid', 'is-valid');
    });
}

/* ========================================
   GESTIÓN DE MENSAJES
======================================== */

function setupMessages() {
    const messages = document.querySelectorAll('.auth-message');
    
    messages.forEach(message => {
        // Auto-ocultar mensajes de éxito después de 5 segundos
        if (message.classList.contains('success')) {
            setTimeout(() => {
                fadeOutMessage(message);
            }, 5000);
        }
        
        // Agregar botón de cerrar a mensajes de error
        if (message.classList.contains('error')) {
            addCloseButton(message);
        }
    });
}

function fadeOutMessage(message) {
    message.style.transition = 'opacity 0.5s ease';
    message.style.opacity = '0';
    
    setTimeout(() => {
        message.remove();
    }, 500);
}

function addCloseButton(message) {
    const closeButton = document.createElement('button');
    closeButton.innerHTML = '×';
    closeButton.className = 'close-btn';
    closeButton.style.cssText = `
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        float: right;
        color: inherit;
        opacity: 0.7;
    `;
    
    closeButton.addEventListener('click', () => {
        message.remove();
    });
    
    message.appendChild(closeButton);
}

/* ========================================
   ESTADOS DE CARGA
======================================== */

function showLoadingState(form) {
    const submitButton = form.querySelector('.auth-btn');
    const originalText = submitButton.textContent;
    
    // Deshabilitar botón y cambiar texto
    submitButton.disabled = true;
    submitButton.textContent = 'Procesando...';
    submitButton.style.opacity = '0.6';
    
    // Restaurar después de 3 segundos (fallback)
    setTimeout(() => {
        submitButton.disabled = false;
        submitButton.textContent = originalText;
        submitButton.style.opacity = '1';
    }, 3000);
}

/* ========================================
   ANIMACIONES
======================================== */

function setupAnimations() {
    // Animación de entrada para la tarjeta
    const authCard = document.querySelector('.auth-card');
    if (authCard) {
        authCard.style.opacity = '0';
        authCard.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            authCard.style.transition = 'all 0.6s ease';
            authCard.style.opacity = '1';
            authCard.style.transform = 'translateY(0)';
        }, 100);
    }
    
    // Animación de entrada para mensajes
    const messages = document.querySelectorAll('.auth-message');
    messages.forEach((message, index) => {
        message.style.opacity = '0';
        message.style.transform = 'translateX(-20px)';
        
        setTimeout(() => {
            message.style.transition = 'all 0.4s ease';
            message.style.opacity = '1';
            message.style.transform = 'translateX(0)';
        }, 200 + (index * 100));
    });
}

/* ========================================
   UTILIDADES
======================================== */

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `auth-message ${type}`;
    notification.textContent = message;
    
    const messagesContainer = document.querySelector('.auth-messages') || 
                            document.querySelector('.auth-card');
    
    if (messagesContainer) {
        messagesContainer.insertBefore(notification, messagesContainer.firstChild);
        
        // Auto-ocultar después de 5 segundos
        setTimeout(() => {
            fadeOutMessage(notification);
        }, 5000);
    }
}

function togglePasswordVisibility(input) {
    const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
    input.setAttribute('type', type);
}

/* ========================================
   EVENTOS ESPECÍFICOS
======================================== */

// Agregar botones para mostrar/ocultar contraseña
document.addEventListener('DOMContentLoaded', function() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    
    passwordInputs.forEach(input => {
        const toggleButton = document.createElement('button');
        toggleButton.type = 'button';
        toggleButton.innerHTML = '👁️';
        toggleButton.className = 'password-toggle';
        toggleButton.style.cssText = `
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1rem;
        `;
        
        const formGroup = input.closest('.form-group');
        formGroup.style.position = 'relative';
        
        toggleButton.addEventListener('click', () => {
            togglePasswordVisibility(input);
        });
        
        formGroup.appendChild(toggleButton);
    });
});

// Prevenir envío múltiple de formularios
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.auth-form');
    
    forms.forEach(form => {
        let isSubmitting = false;
        
        form.addEventListener('submit', function(e) {
            if (isSubmitting) {
                e.preventDefault();
                return false;
            }
            
            isSubmitting = true;
            
            // Restablecer después de 3 segundos
            setTimeout(() => {
                isSubmitting = false;
            }, 3000);
        });
    });
});
