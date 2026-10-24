// Coordinator queue: filter by priority band + text search. Owner: Sadia
document.addEventListener('DOMContentLoaded', () => {
  const rows = [...document.querySelectorAll('#queue tbody tr[data-band]')]; if (!rows.length) return;
  const search = document.getElementById('q-search'); let band = 'all';
  const apply = () => rows.forEach((r) => {
    const ok = (band === 'all' || r.dataset.band === band) && r.textContent.toLowerCase().includes((search.value || '').toLowerCase());
    r.style.display = ok ? '' : 'none';
  });
  document.querySelectorAll('.chip[data-band]').forEach((c) => c.addEventListener('click', () => {
    document.querySelectorAll('.chip[data-band]').forEach((x) => x.classList.remove('on'));
    c.classList.add('on'); band = c.dataset.band; apply();
  }));
  search.addEventListener('input', apply);
});
