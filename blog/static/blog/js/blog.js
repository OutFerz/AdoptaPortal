// autosubmit del buscador con pequeño debounce
(function(){
  const form = document.querySelector('form[data-autosubmit]');
  if(!form) return;
  const q = form.querySelector('input[name="q"]');
  if(!q) return;
  let t; q.addEventListener('input', () => {
    clearTimeout(t); t = setTimeout(() => form.submit(), 400);
  });
})();