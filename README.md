# fake_identity

Generate clearly fictitious identities for testing:
- First name, last name
- Email (uses RFC 2606 example domains)
- Phone (US/CA NANP, AU mobile)
- Address (US, Canada, Australia) with **non-routable** defaults

## 🚀 Quick Start on GitHub

### Option 1: GitHub Codespaces (Recommended)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/yourusername/fake-identity)

1. Click the "Open in GitHub Codespaces" button above
2. Wait for the environment to load (auto-installs dependencies)
3. Run: `python app.py`
4. Access the API at the forwarded port (usually shown in VS Code)

### Option 2: Clone and Run Locally

## 🌐 Live API

**Public API Endpoint**: `https://your-deployment-url.com/`

Try it now:
- [Get random identity](https://your-deployment-url.com/identity)
- [Get random US address](https://your-deployment-url.com/address?country=US)
- [Get random person](https://your-deployment-url.com/person)

## Why it's safe by default
- Emails use `example.com` / `example.net` / `example.org` (RFC 2606 reserved).
- Addresses default to **guaranteed-nonexistent** postal codes and region codes:
  - US: state `ZZ`, ZIP `00000`
  - CA: invalid postal (starts with forbidden letter), province `ZZ`
  - AU: postcode `0000`, state `XX`

> You can set `format_valid=true` to get format-valid outputs that look real but are still randomly generated. Those may coincidentally match a real address, so keep the default if you must avoid any risk.

## 🚀 Quick Start

### API Usage (No Installation Required)

## Install
```
```bash
pip install .
```

## Usage
from fake_identity import random_person, random_address, random_email

p = random_person()  # dict: first_name, last_name
addr_us = random_address(country="US")     # non-routable by default
addr_ca = random_address(country="CA")
addr_au = random_address(country="AU")
email = random_email(p["first_name"], p["last_name"])  # example.com by default

## CLI
python -m fake_identity --count 3 --country US

## Flask API
To use the Flask API, run the following command:
```bash
flask run
```

The API will be available at `http://127.0.0.1:5000/`.

### Endpoints
- `/person`: Returns a random person (first name, last name).
- `/address`: Returns a random address. Accepts `country` as a query parameter (`US`, `CA`, `AU`).
- `/email`: Returns a random email. Accepts `first_name` and `last_name` as query parameters.
- `/identity`: Returns a random identity (first name, last name, email, address, phone). Accepts `country` as a query parameter (`US`, `CA`, `AU`).

## License
MIT

---

# `fake_identity/__init__.py`

```python
from .generator import (
    random_first_name,
    random_last_name,
    random_person,
    random_email,
    random_address,
)
__all__ = [
    "random_first_name",
    "random_last_name",
    "random_person",
    "random_email",
    "random_address",
]
