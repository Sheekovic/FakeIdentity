/* FakeIdentity SW for GitHub Pages: provides /api/* endpoints within project scope */

const VERSION = '1.0.0-ghp';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET') return;

  // Only handle requests within our own scope and targeting /api/*
  const scopePath = new URL(self.registration.scope).pathname.replace(/\/+$/, '');
  if (!url.pathname.startsWith(scopePath)) return;
  const pathInScope = url.pathname.slice(scopePath.length) || '/';
  if (!pathInScope.startsWith('/api/')) return;

  event.respondWith(handleApi(pathInScope, url));
});

function json(data, init = 200) {
  return new Response(JSON.stringify(data), {
    status: typeof init === 'number' ? init : 200,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }
  });
}

/* ------------------- Random Data Generators ------------------- */
const FIRST = ["Avery","Cameron","Dakota","Dylan","Harper","Jordan","Logan","Morgan","Parker","Quinn","Riley","Rowan","Skyler","Taylor","Alex","Casey","Jamie","Jesse","Lee","Shawn","Sam","Noah","Mia","Liam","Emma"];
const LAST = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin","Clark","Lewis","Lee","Walker"];
const STREET_WORDS = ["Oak","Pine","Maple","Cedar","Elm","Birch","Willow","Sunset","Sunrise","Highland","Valley","Hill","Ridge","Creek","River","Lake","Park","Garden","Spring","Summer","Winter","Autumn","North","South","East","West","Central","Main","First","Second","Third","Lincoln","Washington","Madison","Franklin"];
const STREET_SUFFIX = ["St","Ave","Blvd","Rd","Ln","Dr","Way","Ct","Pl","Terrace","Circle","Loop","Trail","Path","Grove"];
const CITY_PREFIX = ["Spring","River","Lake","Hill","Valley","Park","Green","Fair","Pleasant","Bright","Clear","Grand","Red","Blue","New","Old","North","South","East","West","Port","Fort","Mount","Glen","Brook","Wood","Field","Stone","Golden","Silver"];
const CITY_SUFFIX = ["ville","town","city","burg","ford","field","wood","dale","view","haven","port","ridge","grove","falls","springs","heights","garden","meadow"];
const US_STATES = ["CA","NY","TX","FL","WA","CO","IL","MA","PA","GA","NC","AZ","MI","OH","VA","NJ","TN","OR","MN","MD"];
const CA_PROV = ["ON","QC","BC","AB","MB","SK","NS","NB","NL","PE","NT","YT","NU"];
const AU_STATES = ["NSW","VIC","QLD","WA","SA","TAS","ACT","NT"];
const NANP_AREA = [212,213,214,215,216,303,305,310,312,313,404,407,408,415,416,503,504,505,512,516,617,646,702,703,704,718,801,802,808,818,905];

function pick(a){ return a[Math.floor(Math.random()*a.length)]; }
function int(n, m){ return Math.floor(Math.random()*(m-n+1))+n; }
function slug(s){ return s.toLowerCase().replace(/[^a-z0-9]+/g,'.').replace(/\.+/g,'.').replace(/^\.+|\.+$/g,''); }

function randomPerson(){
  return { first_name: pick(FIRST), last_name: pick(LAST) };
}
function randomEmail(first, last){
  const dom = pick(["example.com","example.net","example.org"]);
  return `${slug(first)}.${slug(last)}@${dom}`;
}
function randomCity(){
  return `${pick(CITY_PREFIX)}${pick(CITY_SUFFIX)}`;
}
function randomAddress(country="US", formatValid=true){
  const line1 = `${int(10,9999)} ${pick(STREET_WORDS)} ${pick(STREET_SUFFIX)}`;
  const city = randomCity();
  let region, postcode;
  if (country === "CA") {
    region = pick(CA_PROV);
    // A1A 1A1 pattern
    const L = () => pick("ABCEGHJ-NPRSTVXY".split(""));
    const D = () => int(0,9);
    postcode = `${L()}${D()}${L()} ${D()}${L()}${D()}`;
  } else if (country === "AU") {
    region = pick(AU_STATES);
    postcode = String(int(200, 9999)).padStart(4,'0');
  } else {
    region = pick(US_STATES);
    postcode = String(int(10000, 99999));
  }
  if (!formatValid) {
    // Make it clearly fake but structured
    return { line1: "0000 Example St", city: "Nowhere", region, postcode: "00000", country };
  }
  return { line1, city, region, postcode, country };
}
function randomPhone(country="US"){
  if (country === "AU") {
    // 04xx xxx xxx
    const n = `04${int(10,99)} ${String(int(0,999)).padStart(3,'0')} ${String(int(0,999)).padStart(3,'0')}`;
    return n;
  }
  // NANP: (AAA) NXX-XXXX
  const area = pick(NANP_AREA);
  const nxx = int(200, 999);
  const xxxx = String(int(0,9999)).padStart(4,'0');
  return `(${area}) ${nxx}-${xxxx}`;
}
function buildIdentity(country="US", formatValid=true) {
  const p = randomPerson();
  const address = randomAddress(country, formatValid);
  return {
    first_name: p.first_name,
    last_name: p.last_name,
    email: randomEmail(p.first_name, p.last_name),
    phone: randomPhone(country),
    address
  };
}

/* ------------------- API HANDLERS ------------------- */
async function handleApi(pathInScope, url) {
  const qs = Object.fromEntries(url.searchParams.entries());
  const country = (qs.country || 'US').toUpperCase();
  const formatValid = (qs.format_valid ?? 'true') !== 'false';

  if (pathInScope === '/api/health') {
    return json({ status: 'ok', version: VERSION });
  }
  if (pathInScope === '/api/person') {
    return json(randomPerson());
  }
  if (pathInScope === '/api/email') {
    const first = qs.first_name || pick(FIRST);
    const last = qs.last_name || pick(LAST);
    return json({ email: randomEmail(first, last) });
  }
  if (pathInScope === '/api/phone') {
    return json({ phone: randomPhone(country) });
  }
  if (pathInScope === '/api/address') {
    return json(randomAddress(country, formatValid));
  }
  if (pathInScope === '/api/identity') {
    return json(buildIdentity(country, formatValid));
  }

  return json({ error: 'Not Found' }, 404);
}
