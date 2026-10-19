// Live priority gauge — mirrors reliefrequests/scoring.py. Owner: Member 2 (Sadia)
document.addEventListener('DOMContentLoaded', () => {
  const panel = document.getElementById('gauge'); if (!panel) return;
  const $ = (id) => document.getElementById(id);
  const W = { medical_emergency: 5, no_supplies: 4, large: 3, has_vulnerable: 2 }, MAX = 14;
  const band = (s) => s >= 8 ? 'critical' : s >= 5 ? 'high' : s >= 3 ? 'medium' : 'low';
  function update() {
    const on = {
      medical_emergency: $('id_medical_emergency').checked, no_supplies: $('id_no_supplies').checked,
      large: (parseInt($('id_household_size').value, 10) || 0) > 50, has_vulnerable: $('id_has_vulnerable').checked };
    let score = Object.keys(W).reduce((a, k) => a + (on[k] ? W[k] : 0), 0) || 1;
    const b = band(score);
    panel.dataset.band = b;
    $('g-score').textContent = score;
    $('g-water').style.height = Math.max(7, (score / MAX) * 100) + '%';
    $('g-badge').className = 'badge b-' + b; $('g-badge').textContent = b[0].toUpperCase() + b.slice(1) + ' priority';
    document.querySelectorAll('[data-f]').forEach((li) => li.classList.toggle('active', !!on[li.dataset.f]));
  }
  document.querySelectorAll('#request-form input').forEach((e) => { e.addEventListener('input', update); e.addEventListener('change', update); });
  update();
});
