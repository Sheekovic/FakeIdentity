# Fake Identity (Static)

Generate clearly fictitious identities for testing:
- First name, last name
- Email (uses RFC 2606 example domains)
- Phone (US/CA NANP, AU mobile)
- Address (US, Canada, Australia) with optional format-valid output

## Online Demo (GitHub Pages)
Use it in your browser:
- https://sheekovic.github.io/FakeIdentity/

Features:
- Modern, simple, colorful UI
- Generates identity, address, phone, and email
- Works entirely on GitHub Pages (no server required)
- Service Worker exposes API-like endpoints under /api/* within the page scope

Note: Open the site first so the Service Worker can register, then you can call the endpoints from that page or same origin.

### Static API Endpoints (Service Worker)
Parameters:
- country: US (default), CA, AU
- format_valid: true (default), false (clearly fake but structured)

Endpoints:
- /api/person
- /api/address?country=US|CA|AU&format_valid=true|false
- /api/phone?country=US|CA|AU
- /api/email?first_name=...&last_name=...
- /api/identity?country=US|CA|AU&format_valid=true|false

Examples (run in the browser console on the site):
```
fetch('/FakeIdentity/api/person').then(res => res.json()).then(console.log);
fetch('/FakeIdentity/api/address?country=US').then(res => res.json()).then(console.log);
fetch('/FakeIdentity/api/identity?country=AU&format_valid=true').then(res => res.json()).then(console.log);
```

## Why it's safe by default
- Emails use `example.com` / `example.net` / `example.org` (RFC 2606 reserved).
- Addresses default to **guaranteed-nonexistent** postal codes and region codes:
  - US: state `ZZ`, ZIP `00000`
  - CA: invalid postal (starts with forbidden letter), province `ZZ`
  - AU: postcode `0000`, state `XX`

> You can set `format_valid=true` to get format-valid outputs that look real but are still randomly generated. Those may coincidentally match a real address, so keep the default if you must avoid any risk.

## 🚀 Quick Start

### API Usage (No Installation Required)
