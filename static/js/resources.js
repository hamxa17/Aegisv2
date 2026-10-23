// Resource page: live stock bar preview while typing. Owner: Hamza
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.res-form input[name=stock]').forEach((input) => {
    input.addEventListener('input', () => {
      const res = input.closest('.res'), cap = +res.dataset.cap || 1;
      const pct = Math.min(100, (+input.value || 0) / cap * 100);
      res.querySelector('.track i').style.width = pct + '%';
      res.classList.toggle('res-low', pct < 50 && !res.classList.contains('res-short'));
    });
  });
});
