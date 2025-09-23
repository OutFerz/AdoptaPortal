// blog.js — efectos premium pero livianos

// 1) Auto-submit del buscador (con debounce)
(function(){
  const forms = [
    document.querySelector('form[data-autosubmit]'),
    document.querySelector('.blog-search')
  ].filter(Boolean);
  forms.forEach(form=>{
    const q = form.querySelector('input[name="q"]');
    if(!q) return;
    let t; q.addEventListener('input', ()=>{
      clearTimeout(t); t = setTimeout(()=> form.submit(), 450);
    });
  });
})();

// 2) Revelar tarjetas al hacer scroll
(function(){
  const items = document.querySelectorAll('.js-reveal, .post-card');
  if(!items.length || !('IntersectionObserver' in window)) return;
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      if(e.isIntersecting){
        e.target.classList.add('is-visible');
        io.unobserve(e.target);
      }
    });
  }, {threshold:.12});
  items.forEach(el=>io.observe(el));
})();

// 3) Barra de progreso de lectura + tiempo estimado
(function(){
  const bar = document.getElementById('readProgress');
  const article = document.getElementById('postContent');
  if(!bar || !article) return;

  // Tiempo de lectura
  const target = document.querySelector('[data-readtime]');
  if(target){
    const txt = article.textContent || '';
    const words = txt.trim().split(/\s+/).filter(Boolean).length;
    const minutes = Math.max(1, Math.round(words / 200)); // 200 wpm
    target.textContent = `⏱️ ${minutes} min de lectura`;
  }

  // Progreso
  const clamp = (v,min,max)=>Math.max(min,Math.min(max,v));
  const onScroll = ()=>{
    const rect = article.getBoundingClientRect();
    const total = article.offsetHeight - window.innerHeight;
    const scrolled = clamp(window.scrollY - article.offsetTop, 0, total > 0 ? total : 1);
    const pct = clamp(scrolled / (total || 1), 0, 1) * 100;
    bar.style.width = pct + '%';
  };
  let ticking = false;
  const raf = () => { ticking=false; onScroll(); };
  const handler = () => { if(!ticking){ ticking=true; requestAnimationFrame(raf); } };
  window.addEventListener('scroll', handler, {passive:true});
  window.addEventListener('resize', handler);
  handler();
})();

// 4) Copiar enlace del post
(function(){
  const btn = document.querySelector('[data-copy-link]');
  if(!btn) return;
  const url = btn.getAttribute('data-url') || location.href;
  btn.addEventListener('click', async ()=>{
    try{
      await navigator.clipboard.writeText(url);
      const old = btn.textContent;
      btn.textContent = '¡Enlace copiado!';
      setTimeout(()=> btn.textContent = old, 1400);
    }catch(_){
      // Fallback
      const t = document.createElement('input');
      t.value = url; document.body.appendChild(t); t.select();
      document.execCommand('copy'); t.remove();
      alert('Enlace copiado');
    }
  });
})();