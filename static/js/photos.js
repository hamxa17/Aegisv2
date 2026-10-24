// Live image preview before upload. Owner: Sunita
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('input[type=file][data-preview]').forEach((input) => {
    const img = document.getElementById(input.dataset.preview);
    if (!img) return;
    input.addEventListener('change', () => {
      const file = input.files[0];
      if (!file || !file.type.startsWith('image/')) { img.hidden = true; return; }
      img.src = URL.createObjectURL(file);
      img.hidden = false;
    });
  });
});
