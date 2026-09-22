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

const certificateViewer = document.querySelector('.certificate-viewer');
const certificateViewerImage = certificateViewer?.querySelector('.certificate-viewer__image');
const certificateViewerTitle = certificateViewer?.querySelector('.certificate-viewer__title');
const certificateViewerClose = certificateViewer?.querySelector('.certificate-viewer__close');
let certificateViewerTrigger = null;

const closeCertificateViewer = () => {
  if (certificateViewer?.open) certificateViewer.close();
};

document.querySelectorAll('.certificate-link').forEach((link) => {
  link.addEventListener('click', (event) => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    if (!certificateViewer || !certificateViewerImage || !certificateViewerTitle) return;

    const certificateImage = link.querySelector('img');
    if (!certificateImage) return;

    event.preventDefault();
    certificateViewerTrigger = link;
    certificateViewerImage.src = link.href;
    certificateViewerImage.alt = certificateImage.alt;
    certificateViewerTitle.textContent = certificateImage.alt;
    certificateViewer.showModal();
  });
});

certificateViewerClose?.addEventListener('click', closeCertificateViewer);

certificateViewer?.addEventListener('click', (event) => {
  if (event.target === certificateViewer) closeCertificateViewer();
});

certificateViewer?.addEventListener('close', () => {
  certificateViewerImage?.removeAttribute('src');
  if (certificateViewerImage) certificateViewerImage.alt = '';
  if (certificateViewerTitle) certificateViewerTitle.textContent = '';
  certificateViewerTrigger?.focus();
  certificateViewerTrigger = null;
});
