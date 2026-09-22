document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      event.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

const buildContinuousTicker = () => {
  const ticker = document.querySelector('.ticker');
  const track = ticker?.querySelector('.ticker-track');
  const source = track?.querySelector('.ticker-item');

  if (!ticker || !track || !source) return;

  track.querySelectorAll('[data-ticker-clone]').forEach((item) => item.remove());
  track.querySelectorAll('.ticker-item').forEach((item) => {
    if (item !== source) item.remove();
  });

  const sequenceWidth = source.getBoundingClientRect().width;
  if (!sequenceWidth) return;

  const copiesNeeded = Math.max(
    2,
    Math.ceil((ticker.clientWidth + sequenceWidth) / sequenceWidth) + 1,
  );
  const clones = document.createDocumentFragment();

  for (let index = 1; index < copiesNeeded; index += 1) {
    const clone = source.cloneNode(true);
    clone.setAttribute('aria-hidden', 'true');
    clone.dataset.tickerClone = 'true';
    clones.append(clone);
  }

  track.append(clones);
  track.style.setProperty('--ticker-shift', `-${Math.ceil(sequenceWidth)}px`);
};

let tickerResizeFrame;
const refreshTicker = () => {
  cancelAnimationFrame(tickerResizeFrame);
  tickerResizeFrame = requestAnimationFrame(buildContinuousTicker);
};

refreshTicker();
window.addEventListener('resize', refreshTicker, { passive: true });

if (document.fonts?.ready) {
  document.fonts.ready.then(refreshTicker);
}
