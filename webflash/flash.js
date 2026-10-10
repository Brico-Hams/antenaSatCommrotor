const support = document.querySelector('#support');
const installer = document.querySelector('#installer');
const acknowledgement = document.querySelector('#acknowledge');
let available = false;

if (!window.isSecureContext) {
  support.textContent = 'Se requiere HTTPS (o localhost para desarrollo). No abras el archivo directamente.';
} else if (!('serial' in navigator)) {
  support.textContent = 'Web Serial no está disponible. Usa Chrome/Edge de escritorio; móvil, Firefox y Safari no son compatibles.';
} else {
  try {
    // Copied in full by CI; relative dynamic-import chunks remain beside this entry point.
    await import('./vendor/esp-web-tools/web/install-button.js');
    available = true;
    support.textContent = 'Permiso USB opcional: sólo se pide al pulsar Conectar. Si lo deniegas o cancelas, no se instala nada; vuelve a intentarlo cuando quieras.';
  } catch (error) {
    support.textContent = 'No se pudo cargar ESP Web Tools. Comprueba que CI generó la página completa; no hay fallback CDN.';
    console.error('ESP Web Tools load failed', error);
  }
}
acknowledgement.addEventListener('change', () => {
  installer.hidden = !available || !acknowledgement.checked;
});
try {
  const response = await fetch('./build-info.json', { cache: 'no-store' });
  if (!response.ok) throw Error('Missing build metadata');
  const info = await response.json();
  document.querySelector('#version').textContent =
    `Versión: ${info.version}\nCommit: ${info.sourceSha || 'SIN COMMIT — compilación local'}\nESP Web Tools: ${info.espWebTools.version}\n` +
    info.assets.map(asset => `${asset.path} @ ${asset.offset}: ${asset.sha256}`).join('\n');
} catch {
  document.querySelector('#version').textContent = 'Sin artefactos de compilación. No intentes instalar una copia de fuentes sin generar.';
}
