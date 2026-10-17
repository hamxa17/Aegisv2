// Landing page: count-up numbers + delivery confirmation prompt. Owner: Sunita
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-count]').forEach((el) => {
    const end = +el.dataset.count; let n = 0; const step = Math.max(1, Math.ceil(end / 40));
    const t = setInterval(() => { n = Math.min(end, n + step); el.textContent = n.toLocaleString(); if (n >= end) clearInterval(t); }, 25);
  });
  document.querySelectorAll('form[data-confirm]').forEach((f) =>
    f.addEventListener('submit', (e) => { if (!confirm(f.dataset.confirm)) e.preventDefault(); }));
});
