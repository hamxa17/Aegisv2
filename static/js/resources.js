// Resources page: count-up numbers, rising tanks, +/- steppers and live preview. Owner: Hamza
document.addEventListener('DOMContentLoaded', () => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // numbers count up from 0
  document.querySelectorAll('[data-count]').forEach((el) => {
    const end = +el.dataset.count, suffix = el.dataset.suffix || '';
    if (reduce || !end) return;
    const t0 = performance.now();
    const tick = (now) => {
      const k = Math.min(1, (now - t0) / 800);
      el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))) + suffix;
      if (k < 1) requestAnimationFrame(tick);
    };
    el.textContent = '0' + suffix;
    requestAnimationFrame(tick);
  });

  // tanks rise from empty to their level
  document.querySelectorAll('.rcard').forEach((card) => {
    const target = card.style.getPropertyValue('--h');
    if (!reduce) {
      card.style.setProperty('--h', '0%');
      requestAnimationFrame(() => requestAnimationFrame(() => card.style.setProperty('--h', target)));
    }
    const input = card.querySelector('input[type=number]');
    const cap = +card.dataset.cap || 1, shortBy = +card.dataset.short;

    const dirty = () => {
      const edited = (+input.value || 0) !== +input.defaultValue;
      card.classList.toggle('rcard-dirty', edited);
      card.querySelector('.rdirty').hidden = !edited;
      const n = document.querySelectorAll('.rcard-dirty').length;
      document.getElementById('saveBar').hidden = n === 0;
      document.getElementById('saveCount').textContent = n;
      document.getElementById('savePlural').textContent = n === 1 ? '' : 's';
    };

    const preview = () => {
      const v = Math.max(0, +input.value || 0);
      const pct = Math.min(100, v / cap * 100);
      card.style.setProperty('--h', pct + '%');
      card.querySelector('.rc-num').textContent = v;
      if (!shortBy) {                       // short state is decided by the server after Update
        card.classList.toggle('rcard-low', pct < 50);
      }
      dirty();
    };
    input.addEventListener('input', preview);
    card.querySelectorAll('[data-step]').forEach((b) => b.addEventListener('click', () => {
      input.value = Math.max(0, (+input.value || 0) + +b.dataset.step);
      preview();
    }));
  });
});
