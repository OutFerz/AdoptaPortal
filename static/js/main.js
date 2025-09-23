// JavaScript principal del Portal de Mascotas

document.addEventListener('DOMContentLoaded', () => {
  // Inicializar funcionalidades existentes
  initFormValidation();
  initTooltips();
  initAnimations();

  // Mobile nav (nuevo header)
  const btn = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');
  if (btn && nav) {
    btn.addEventListener('click', () => nav.classList.toggle('is-open'));
  }

  // “Ver más / Ver menos” de descripciones (coincide con home.html)
  document.querySelectorAll('.toggle-desc').forEach(btn => {
    const id = btn.dataset.target;
    const el = document.getElementById(id);
    if (!el) return;

    // si no hay overflow, ocultamos el botón
    requestAnimationFrame(() => {
      if (el.scrollHeight <= el.clientHeight + 1) btn.style.display = 'none';
    });

    btn.addEventListener('click', () => {
      el.classList.toggle('expanded');
      btn.textContent = el.classList.contains('expanded') ? 'Ver menos' : 'Ver más';
    });
  });

  // Autosize de textarea (mensaje opcional en solicitud rápida)
  const autosize = ta => {
    ta.style.height = 'auto';
    ta.style.height = Math.min(ta.scrollHeight, 260) + 'px';
  };
  document.querySelectorAll('textarea.msg-optional').forEach(ta => {
    autosize(ta);
    ta.addEventListener('input', () => autosize(ta));
  });
});

// =======================
// Validación de formularios
// =======================
function initFormValidation() {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function (e) {
      if (!validateForm(this)) e.preventDefault();
    });
  });
}

function validateForm(form) {
  let isValid = true;
  const requiredFields = form.querySelectorAll('[required]');
  requiredFields.forEach(field => {
    if (!String(field.value || '').trim()) {
      showFieldError(field, 'Este campo es obligatorio');
      isValid = false;
    } else {
      clearFieldError(field);
    }
  });
  return isValid;
}

function showFieldError(field, message) {
  clearFieldError(field);
  const errorDiv = document.createElement('div');
  errorDiv.className = 'field-error';
  errorDiv.style.color = '#f44336';
  errorDiv.style.fontSize = '0.9em';
  errorDiv.style.marginTop = '5px';
  errorDiv.textContent = message;
  field.parentNode.appendChild(errorDiv);
  field.style.borderColor = '#f44336';
}

function clearFieldError(field) {
  const existingError = field.parentNode.querySelector('.field-error');
  if (existingError) existingError.remove();
  field.style.borderColor = '#ddd';
}

// =======================
// Tooltips simples
// =======================
function initTooltips() {
  const els = document.querySelectorAll('[data-tooltip]');
  els.forEach(el => {
    el.addEventListener('mouseenter', showTooltip);
    el.addEventListener('mouseleave', hideTooltip);
  });
}

function showTooltip(e) {
  const msg = e.currentTarget.getAttribute('data-tooltip');
  if (!msg) return;
  const tip = document.createElement('div');
  tip.className = 'tooltip';
  tip.textContent = msg;
  tip.style.cssText = `
    position: absolute; background:#333; color:#fff; padding:8px 12px;
    border-radius:4px; font-size:.9em; z-index:1000; pointer-events:none;
  `;
  document.body.appendChild(tip);
  const rect = e.currentTarget.getBoundingClientRect();
  tip.style.left = rect.left + 'px';
  tip.style.top = (rect.top - tip.offsetHeight - 6) + 'px';
}

function hideTooltip() {
  const tip = document.querySelector('.tooltip');
  if (tip) tip.remove();
}

// =======================
// Animaciones suaves
// =======================
function initAnimations() {
  // Animar tarjetas reales que existen en el sitio
  const cards = document.querySelectorAll('.pet-card, .feature-card');
  if (!cards.length) return;

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(16px)';
    card.style.transition = 'opacity .5s ease, transform .5s ease';
    observer.observe(card);
  });
}

// =======================
// Utilidades y stats
// =======================
function showAlert(message, type = 'info') {
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type}`;
  alertDiv.textContent = message;
  const container = document.querySelector('.container, .ap-container');
  if (container) {
    container.insertBefore(alertDiv, container.firstChild);
    setTimeout(() => alertDiv.remove(), 5000);
  }
}

function confirmAction(message) {
  return confirm(message);
}

// Funciones específicas para solicitudes
function confirmSolicitud() {
  return confirmAction('¿Estás seguro de que quieres enviar esta solicitud?');
}

function confirmRespuesta() {
  return confirmAction('¿Estás seguro de tu decisión? Esta acción no se puede deshacer.');
}

// Auto-actualizar estadísticas (simulado)
function updateStats() {
  const statNumbers = document.querySelectorAll('.stat-number');
  statNumbers.forEach(stat => {
    const currentValue = parseInt(stat.textContent) || 0;
    const newValue = currentValue + Math.floor(Math.random() * 3);
    animateNumber(stat, currentValue, newValue, 1000);
  });
}

function animateNumber(element, start, end, duration) {
  const startTime = performance.now();
  function step(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    element.textContent = Math.floor(start + (end - start) * progress);
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// Inicializar actualización de estadísticas cada 30 segundos
setInterval(updateStats, 30000);