document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('gallery-container');
  const mainImg = document.getElementById('main-gallery-image');

  console.log('Gallery JS Loaded:', { container, mainImg }); // برای تست لود شدن

  if (!container || !mainImg) return;

  container.addEventListener('click', (e) => {
    const btn = e.target.closest('.thumb-item');
    if (!btn) return;

    const newSrc = btn.getAttribute('data-src');
    const newAlt = btn.getAttribute('data-alt');

    if (newSrc) mainImg.src = newSrc;
    if (newAlt) mainImg.alt = newAlt;

    container.querySelectorAll('.thumb-item').forEach((el) => {
      el.classList.remove('border-brand-500', 'ring-2', 'ring-brand-500/20');
      el.classList.add('border-transparent', 'opacity-60');
    });

    btn.classList.remove('border-transparent', 'opacity-60');
    btn.classList.add('border-brand-500', 'ring-2', 'ring-brand-500/20');
  });
});
