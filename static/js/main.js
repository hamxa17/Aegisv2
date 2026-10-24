// Shared behaviour: mobile nav toggle. Owner: Sunita
document.addEventListener('DOMContentLoaded', () => {
  const t = document.querySelector('.nav-toggle'), l = document.getElementById('nav-links');
  if (t && l) t.addEventListener('click', () => l.classList.toggle('open'));
});
