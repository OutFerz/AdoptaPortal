/* AUTH – login & register */

document.addEventListener('DOMContentLoaded', () => {
  initAuthFeatures();
  setupPasswordToggle();
  preventDoubleSubmit();
});

function initAuthFeatures() {
  relaxLoginPasswordLength();
  setupFormValidation();
  setupMessages();
  setupAnimations();
  setupRealTimeValidation();
}

/* ------------ Validación de formularios ------------ */

function setupFormValidation() {
  const forms = document.querySelectorAll('.auth-form');
  forms.forEach(form => {
    form.addEventListener('submit', e => {
      if (!validateForm(form)) {
        e.preventDefault();
        return false;
      }
      showLoadingState(form);
    });
  });
}

function validateForm(form) {
  let ok = true;
  clearFormErrors(form);
  form.querySelectorAll('input[required]').forEach(i => {
    if (!validateInput(i)) ok = false;
  });
  if (isRegisterForm(form) && !validatePasswordMatch(form)) ok = false;
  return ok;
}

/* === REGLA CENTRAL: solo pide 8+ en formularios con password2 === */
function validateInput(input) {
  const value = (input.value || '').trim();
  const form = input.closest('form');
  const onRegister = isRegisterForm(form);

  let ok = true;
  let msg = '';

  if (input.hasAttribute('required') && !value) {
    msg = 'Este campo es obligatorio';
    ok = false;
  }

  if (ok && input.type === 'email' && value) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!re.test(value)) {
      msg = 'Ingresa un email válido';
      ok = false;
    }
  }

  if (ok && input.type === 'password' && value) {
    // SOLO en registro (no en login)
    if (onRegister && value.length < 8) {
      msg = 'La contraseña debe tener al menos 8 caracteres';
      ok = false;
    }
  }

  if (ok && input.name === 'username' && value) {
    const reUser = /^[a-zA-Z0-9_]+$/;
    if (!reUser.test(value)) {
      msg = 'El nombre de usuario solo puede contener letras, números y guiones bajos';
      ok = false;
    } else if (value.length < 3) {
      msg = 'El nombre de usuario debe tener al menos 3 caracteres';
      ok = false;
    }
  }

  paintFieldValidation(input, ok, msg);
  return ok;
}

function validatePasswordMatch(form) {
  const p1 = form.querySelector('input[name="password1"]');
  const p2 = form.querySelector('input[name="password2"]');
  if (p1 && p2 && p1.value !== p2.value) {
    showInputError(p2, 'Las contraseñas no coinciden');
    return false;
  }
  return true;
}

function isRegisterForm(form) {
  // Considera "registro" si existe el segundo campo de contraseña
  return !!(form && form.querySelector('input[name="password2"]'));
}

/* ------------ Validación en tiempo real ------------ */

function setupRealTimeValidation() {
  const inputs = document.querySelectorAll('.auth-form input');
  inputs.forEach(input => {
    input.addEventListener('blur', function () { validateInput(this); });
    let t;
    input.addEventListener('input', function () {
      clearTimeout(t);
      t = setTimeout(() => {
        if (this.value.trim()) validateInput(this);
      }, 400);
    });
  });
}

/* ------------ Mensajes/Errores ------------ */

function paintFieldValidation(input, ok, msg) {
  const group = input.closest('.form-group');
  if (!group) return;
  const prev = group.querySelector('.form-errors');
  if (prev) prev.remove();

  if (!ok) {
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
    const err = document.createElement('div');
    err.className = 'form-errors';
    err.textContent = msg;
    input.parentNode.insertBefore(err, input.nextSibling);
  } else {
    input.classList.add('is-valid');
    input.classList.remove('is-invalid');
  }
}

function showInputError(input, message) {
  paintFieldValidation(input, false, message);
}

function clearFormErrors(form) {
  form.querySelectorAll('.form-errors').forEach(e => e.remove());
  form.querySelectorAll('input').forEach(i => i.classList.remove('is-invalid', 'is-valid'));
}

function setupMessages() {
  document.querySelectorAll('.auth-message').forEach(msg => {
    if (msg.classList.contains('success')) {
      setTimeout(() => fadeOutMessage(msg), 5000);
    }
    if (msg.classList.contains('error')) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = '×';
      btn.className = 'close-btn';
      btn.style.cssText =
        'background:none;border:none;font-size:1.5rem;cursor:pointer;float:right;opacity:.7;';
      btn.onclick = () => msg.remove();
      msg.appendChild(btn);
    }
  });
}

function fadeOutMessage(el) {
  el.style.transition = 'opacity .5s';
  el.style.opacity = '0';
  setTimeout(() => el.remove(), 500);
}

/* ------------ Carga/Animaciones ------------ */

function showLoadingState(form) {
  const btn = form.querySelector('.auth-btn');
  if (!btn) return;
  const txt = btn.textContent;
  btn.disabled = true;
  btn.textContent = 'Procesando...';
  btn.style.opacity = '0.6';
  setTimeout(() => {
    btn.disabled = false;
    btn.textContent = txt;
    btn.style.opacity = '1';
  }, 3000);
}

function setupAnimations() {
  const card = document.querySelector('.auth-card');
  if (card) {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    setTimeout(() => {
      card.style.transition = 'all .6s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 100);
  }
}

/* ------------ Utilidades ------------ */

function showNotification(message, type = 'info') {
  const n = document.createElement('div');
  n.className = `auth-message ${type}`;
  n.textContent = message;
  const box = document.querySelector('.auth-messages') || document.querySelector('.auth-card');
  if (box) {
    box.insertBefore(n, box.firstChild);
    setTimeout(() => fadeOutMessage(n), 5000);
  }
}

/* hace que el login NO tenga restricciones de longitud nativas */
function relaxLoginPasswordLength() {
  document.querySelectorAll('input[type="password"]').forEach(input => {
    const form = input.closest('form');
    const onRegister = isRegisterForm(form);
    if (!onRegister) {
      ['minlength', 'pattern', 'title'].forEach(a => input.removeAttribute(a));
    }
  });
}

/* toggler ojo contraseña */
function setupPasswordToggle() {
  document.querySelectorAll('input[type="password"]').forEach(input => {
    const group = input.closest('.form-group');
    if (!group) return;
    group.style.position = 'relative';
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.innerHTML = '👁️';
    btn.className = 'password-toggle';
    btn.style.cssText =
      'position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;font-size:1rem;';
    btn.onclick = () => {
      const t = input.getAttribute('type') === 'password' ? 'text' : 'password';
      input.setAttribute('type', t);
    };
    group.appendChild(btn);
  });
}

/* evita doble submit */
function preventDoubleSubmit() {
  document.querySelectorAll('.auth-form').forEach(form => {
    let sending = false;
    form.addEventListener('submit', e => {
      if (sending) {
        e.preventDefault();
        return false;
      }
      sending = true;
      setTimeout(() => (sending = false), 3000);
    });
  });
}