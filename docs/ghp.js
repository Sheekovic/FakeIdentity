const elCountry = document.getElementById('country');
const elFormat = document.getElementById('formatValid');
const elCards = document.getElementById('cards');
const elJson = document.getElementById('json');
const elToast = document.getElementById('toast');

function toast(msg) {
  elToast.textContent = msg;
  elToast.classList.add('show');
  setTimeout(() => elToast.classList.remove('show'), 1600);
}

// Register Service Worker scoped to this folder (works at /FakeIdentity/)
(async function registerSW() {
  if ('serviceWorker' in navigator) {
    try {
      const reg = await navigator.serviceWorker.register('./sw-ghp.js', { scope: './' });
      await navigator.serviceWorker.ready;
      console.log('SW ready', reg.scope);
    } catch (e) {
      console.warn('SW registration failed', e);
    }
  }
})();

function row(k, v) {
  return `<div class="row"><div class="k">${k}</div><div class="v">${v}</div></div>`;
}

function render(identity) {
  elCards.innerHTML = `
    <div class="card">
      <div class="emoji">🧑</div>
      <div>
        <h3>${identity.first_name} ${identity.last_name}</h3>
        <div class="muted">${identity.email}</div>
      </div>
      <div class="rows">
        ${row('Phone', identity.phone)}
      </div>
    </div>
    <div class="card">
      <div class="emoji">📍</div>
      <div>
        <h3>Address</h3>
        <div class="muted">${identity.address.country}</div>
      </div>
      <div class="rows">
        ${row('Line 1', identity.address.line1)}
        ${row('City', identity.address.city)}
        ${row('Region', identity.address.region)}
        ${row('Postcode', identity.address.postcode)}
      </div>
    </div>
  `;
  elJson.textContent = JSON.stringify(identity, null, 2);
}

async function fetchIdentity() {
  // POST JSON instead of GET query params
  const res = await fetch(`./api/identity`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      country: elCountry.value,
      format_valid: elFormat.value
    }),
    cache: 'no-store'
  });
  if (!res.ok) throw new Error('API error');
  return res.json();
}

document.getElementById('btnGenerate').addEventListener('click', async () => {
  try {
    const identity = await fetchIdentity();
    render(identity);
  } catch (e) {
    toast('Failed to generate identity');
  }
});

document.getElementById('btnCopy').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(elJson.textContent);
    toast('Copied!');
  } catch { toast('Copy failed'); }
});

// Generate one on load
window.addEventListener('load', async () => {
  try { render(await fetchIdentity()); } catch {}
});