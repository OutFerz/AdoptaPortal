// --- AUTH (login + register) v3 cache-bust ---
document.addEventListener('DOMContentLoaded', () => {
  relaxConstraints();
  setupFormValidation();
  setupMessages();
  setupAnimations();
  setupRealTimeValidation();
  setupPasswordToggle();
  preventDoubleSubmit();
});

/* ---------------- core ---------------- */

function setupFormValidation() {
  document.querySelectorAll('.auth-form').forEach(form => {
    form.addEventListener('submit', e => {
      if (!validateForm(form)) { e.preventDefault(); return false; }
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

function validateInput(input) {
  const val = (input.value || '').trim();
  const onRegister = isRegisterForm(input.closest('form'));
  let ok = true, msg = '';

  if (input.hasAttribute('required') && !val) { ok = false; msg = 'Este campo es obligatorio'; }

  // email nativo
  if (ok && input.type === 'email' && val) {
    const emailRx = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRx.test(val)) { ok = false; msg = 'Ingresa un email válido'; }
  }

  // contraseña: solo exigente en registro
  if (ok && input.type === 'password' && val && onRegister && ['password1','password2'].includes(input.name)) {
    if (val.length < 8) { ok = false; msg = 'La contraseña debe tener al menos 8 caracteres'; }
  }

  // ✅ username permite email O usuario sin restricciones estrictas
  if (ok && input.name === 'username' && val) {
    if (val.includes('@')) {
      const emailRx = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRx.test(val)) { ok = false; msg = 'Ingresa un email válido'; }
    } else {
      // Si NO es email, solo verificamos que tenga algo (mínimo 1 char).
      if (val.length < 1) { ok = false; msg = 'Ingresa tu usuario'; }
    }
  }

  paintFieldValidation(input, ok, msg);
  return ok;
}

function validatePasswordMatch(form) {
  const p1 = form.querySelector('input[name="password1"]');
  const p2 = form.querySelector('input[name="password2"]');
  if (p1 && p2 && p1.value !== p2.value) { showInputError(p2, 'Las contraseñas no coinciden'); return false; }
  return true;
}

function isRegisterForm(form) { return !!(form && form.querySelector('input[name="password2"]')); }

/* ---------------- realtime ---------------- */

function setupRealTimeValidation() {
  document.querySelectorAll('.auth-form input').forEach(input => {
    input.addEventListener('blur', function(){ validateInput(this); });
    let t; input.addEventListener('input', function(){
      clearTimeout(t); t = setTimeout(()=>{ if (this.value.trim()) validateInput(this); }, 200);
    });
  });
}

/* ---------------- ui helpers ---------------- */

function paintFieldValidation(input, ok, msg) {
  const group = input.closest('.form-group'); if (!group) return;
  const prev = group.querySelector('.form-errors'); if (prev) prev.remove();

  if (!ok) {
    input.classList.add('is-invalid'); input.classList.remove('is-valid');
    const err = document.createElement('div'); err.className = 'form-errors'; err.textContent = msg;
    input.parentNode.insertBefore(err, input.nextSibling);
  } else {
    input.classList.add('is-valid'); input.classList.remove('is-invalid');
  }
}

function showInputError(input, message){ paintFieldValidation(input, false, message); }
function clearFormErrors(form){
  form.querySelectorAll('.form-errors').forEach(e=>e.remove());
  form.querySelectorAll('input').forEach(i=>i.classList.remove('is-invalid','is-valid'));
}

function setupMessages(){
  document.querySelectorAll('.auth-message').forEach(m=>{
    if (m.classList.contains('success')) setTimeout(()=>{ m.style.transition='opacity .5s'; m.style.opacity='0'; setTimeout(()=>m.remove(),500); }, 5000);
    if (m.classList.contains('error')) {
      const b = document.createElement('button'); b.type='button'; b.textContent='×'; b.className='close-btn';
      b.style.cssText='background:none;border:none;font-size:1.5rem;cursor:pointer;float:right;opacity:.7;'; b.onclick=()=>m.remove(); m.appendChild(b);
    }
  });
}

function showLoadingState(form){
  const btn=form.querySelector('.auth-btn'); if(!btn) return;
  const t=btn.textContent; btn.disabled=true; btn.textContent='Procesando...'; btn.style.opacity='0.6';
  setTimeout(()=>{ btn.disabled=false; btn.textContent=t; btn.style.opacity='1'; },3000);
}

function setupAnimations(){
  const card=document.querySelector('.auth-card');
  if(card){ card.style.opacity='0'; card.style.transform='translateY(30px)';
    setTimeout(()=>{ card.style.transition='all .6s ease'; card.style.opacity='1'; card.style.transform='translateY(0)'; },100);
  }
}

function setupPasswordToggle(){
  document.querySelectorAll('input[type="password"]').forEach(input=>{
    const g=input.closest('.form-group'); if(!g) return; g.style.position='relative';
    const btn=document.createElement('button'); btn.type='button'; btn.innerHTML='👁️'; btn.className='password-toggle';
    btn.style.cssText='position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;font-size:1rem;';
    btn.onclick=()=>{ input.setAttribute('type', input.getAttribute('type')==='password'?'text':'password'); };
    g.appendChild(btn);
  });
}

function preventDoubleSubmit(){
  document.querySelectorAll('.auth-form').forEach(form=>{
    let sending=false;
    form.addEventListener('submit',e=>{
      if(sending){ e.preventDefault(); return false; }
      sending=true; setTimeout(()=>sending=false,3000);
    });
  });
}

/* --------------- constraints/native validation --------------- */

function relaxConstraints() {
  document.querySelectorAll('.auth-form').forEach(f => f.setAttribute('novalidate','novalidate'));
  document.querySelectorAll('input[type="password"]').forEach(i=>['minlength','pattern','title'].forEach(a=>i.removeAttribute(a)));

  // Asegura que el username NO tenga pattern ni handlers heredados
  const u = document.getElementById('username');
  if (u) {
    ['pattern','title','minlength','maxlength'].forEach(a=>u.removeAttribute(a));
    u.onkeypress = null; u.onkeydown = null; u.onkeyup = null;
  }

  // Marca de versión de JS (para comprobar en consola)
  console.log('auth.js v3 cargado');
}

