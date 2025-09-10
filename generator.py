import random
import re
import argparse
import sys
import requests  # Add this import for API requests
from typing import Dict

# A small built-in pool to avoid external deps
_FIRST_NAMES = [
    "Avery","Cameron","Dakota","Dylan","Harper","Jordan","Logan","Morgan",
    "Parker","Quinn","Riley","Rowan","Skyler","Taylor","Alex","Casey",
    "Jamie","Jesse","Lee","Shawn","Sam","Noah","Mia","Liam","Emma"
]
_LAST_NAMES = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
    "Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson",
    "Thomas","Taylor","Moore","Jackson","Martin","Clark","Lewis","Lee","Walker"
]

_STREET_SUFFIX = ["St", "Ave", "Blvd", "Rd", "Ln", "Dr", "Way", "Ct", "Pl", "Terrace", "Circle", "Loop", "Trail", "Path", "Grove"]

# Fun but fictitious-looking words to reduce collision risk
_WORDS = [
    "Test", "Fiction", "Mock", "Sample", "Demo", "Dummy", "Placeholder",
    "Acme", "Foobar", "Example", "Sandbox", "Alpha", "Beta", "Gamma"
]

# Enhanced word lists for better variety
_STREET_WORDS = [
    "Oak", "Pine", "Maple", "Cedar", "Elm", "Birch", "Willow", "Sunset", "Sunrise",
    "Highland", "Valley", "Hill", "Ridge", "Creek", "River", "Lake", "Park", "Garden",
    "Spring", "Summer", "Winter", "Autumn", "North", "South", "East", "West", "Central",
    "Main", "First", "Second", "Third", "Lincoln", "Washington", "Madison", "Franklin"
]

_CITY_PREFIXES = [
    "Spring", "River", "Lake", "Hill", "Valley", "Park", "Green", "Fair", "Pleasant",
    "Mount", "Glen", "Brook", "Wood", "Field", "Stone", "Clear", "Golden", "Silver"
]
_CITY_SUFFIXES = [
    "ville", "town", "city", "burg", "ford", "field", "wood", "dale", "view", "haven",
    "port", "ridge", "grove", "falls", "springs", "heights", "garden", "meadow"
]

# More realistic area codes for different regions
_US_AREA_CODES = [
    212, 213, 214, 215, 216, 301, 302, 303, 305, 310, 312, 313, 314, 315, 316,
    401, 402, 404, 405, 407, 408, 410, 412, 413, 414, 415, 416, 417, 419, 501,
    502, 503, 504, 505, 507, 508, 509, 510, 512, 513, 515, 516, 517, 518, 601,
    602, 603, 605, 606, 607, 608, 609, 610, 612, 614, 615, 616, 617, 618, 619,
    701, 702, 703, 704, 706, 707, 708, 712, 713, 714, 715, 716, 717, 718, 719,
    801, 802, 803, 804, 805, 806, 808, 810, 812, 813, 814, 815, 816, 817, 818,
    901, 902, 903, 904, 906, 907, 908, 909, 910, 912, 913, 914, 915, 916, 917
]

_RESERVED_EMAIL_DOMAINS = ["example.com", "example.net", "example.org"]  # RFC 2606

def _slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", ".", s.strip().lower())
    return re.sub(r"\.+", ".", s).strip(".")

def random_first_name() -> str:
    return random.choice(_FIRST_NAMES)

def random_last_name() -> str:
    return random.choice(_LAST_NAMES)

def random_person() -> Dict[str, str]:
    return {"first_name": random_first_name(), "last_name": random_last_name()}

def random_email(first_name: str, last_name: str, domain: str = None) -> str:
    """
    By default uses RFC 2606 reserved domains to avoid real mailboxes.
    Enhanced with more email format variety.
    """
    if domain is None:
        domain = random.choice(_RESERVED_EMAIL_DOMAINS)
    
    # Various email format styles
    formats = [
        f"{_slug(first_name)}.{_slug(last_name)}{random.randint(10, 9999)}",
        f"{_slug(first_name)}{_slug(last_name)}{random.randint(10, 999)}",
        f"{first_name[0].lower()}{_slug(last_name)}{random.randint(10, 9999)}",
        f"{_slug(first_name)}_{_slug(last_name)}{random.randint(10, 999)}",
        f"{_slug(first_name)}{random.randint(10, 999)}"
    ]
    local = random.choice(formats)
    return f"{local}@{domain}"

def _random_street() -> str:
    """Generate more realistic street names"""
    # Mix of realistic and obviously fake elements
    if random.random() < 0.3:  # 30% chance of using "fake" words
        word = random.choice(_WORDS)
        second = random.choice(_WORDS)
        base = f"{word} {second}".strip()
    else:  # 70% chance of more realistic street names
        if random.random() < 0.5:  # Single word streets
            base = random.choice(_STREET_WORDS)
        else:  # Two word streets
            base = f"{random.choice(_STREET_WORDS)} {random.choice(_STREET_WORDS)}"
    
    return f"{random.randint(10, 9999)} {base} {random.choice(_STREET_SUFFIX)}"

def _random_city_like() -> str:
    """Generate more varied city names"""
    if random.random() < 0.2:  # 20% chance of obviously fake
        return f"{random.choice(_WORDS)}town"
    else:  # 80% chance of realistic-sounding
        prefix = random.choice(_CITY_PREFIXES)
        suffix = random.choice(_CITY_SUFFIXES)
        return f"{prefix}{suffix}"

def _random_us_address(guarantee_nonexistent: bool) -> Dict[str, str]:
    if guarantee_nonexistent:
        # Intentionally invalid state code and ZIP
        state = "ZZ"
        postcode = "00000"
    else:
        # Realistic state codes
        states = ["CA","NY","TX","FL","WA","IL","PA","OH","MI","NC","GA","VA","AZ","MA","CO"]
        state = random.choice(states)
        postcode = f"{random.randint(10000, 99999)}"
    return {
        "line1": _random_street(),
        "line2": "",  # optional
        "city": _random_city_like(),
        "region": state,
        "postcode": postcode,
        "country": "US",
    }

# Canadian postal: A1A 1A1; Forbidden letters: D, F, I, O, Q, U (use them to make it invalid)
_FORBIDDEN_CA = set("DFIOQU")
_ALLOWED_CA = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in _FORBIDDEN_CA]
_DIG = "0123456789"

def _random_ca_postal(valid: bool) -> str:
    if valid:
        # Valid-looking: first letter from allowed set
        pat = [
            random.choice(_ALLOWED_CA),
            random.choice(_DIG),
            random.choice(_ALLOWED_CA),
            " ",
            random.choice(_DIG),
            random.choice(_ALLOWED_CA),
            random.choice(_DIG),
        ]
    else:
        # Intentionally invalid: use forbidden first letter for non-routable
        pat = [
            random.choice(list(_FORBIDDEN_CA)),
            random.choice(_DIG),
            random.choice(_ALLOWED_CA),
            " ",
            random.choice(_DIG),
            random.choice(_ALLOWED_CA),
            random.choice(_DIG),
        ]
    return "".join(pat)

def _random_ca_address(guarantee_nonexistent: bool) -> Dict[str, str]:
    if guarantee_nonexistent:
        province = "ZZ"
        postcode = _random_ca_postal(valid=False)
    else:
        provinces = ["ON","QC","BC","AB","MB","SK","NS","NB","NL","PE","NT","YT","NU"]
        province = random.choice(provinces)
        postcode = _random_ca_postal(valid=True)
    return {
        "line1": _random_street(),
        "line2": "",
        "city": _random_city_like(),
        "region": province,
        "postcode": postcode,
        "country": "CA",
    }

def _random_au_address(guarantee_nonexistent: bool) -> Dict[str, str]:
    if guarantee_nonexistent:
        state = "XX"
        postcode = "0000"
    else:
        states = ["NSW","VIC","QLD","WA","SA","TAS","ACT","NT"]
        state = random.choice(states)
        postcode = f"{random.randint(1000, 9999)}"
    # AU often uses "Suburb, State POSTCODE"
    return {
        "line1": _random_street(),
        "line2": "",
        "city": _random_city_like(),   # suburb-like
        "region": state,
        "postcode": postcode,
        "country": "AU",
    }

def random_address(country: str = "US", guarantee_nonexistent: bool = True) -> Dict[str, str]:
    """
    Generate a fake address.

    guarantee_nonexistent=True (default):
      - US: region "ZZ", ZIP "00000"
      - CA: province "ZZ", invalid postal (forbidden starting letter)
      - AU: state "XX", postcode "0000"

    Set to False for format-valid addresses that *look* real but are still random.
    """
    country = country.upper().strip()
    if country == "US":
        return _random_us_address(guarantee_nonexistent)
    if country in ("CA", "CAN", "CANADA"):
        return _random_ca_address(guarantee_nonexistent)
    if country in ("AU", "AUS", "AUSTRALIA"):
        return _random_au_address(guarantee_nonexistent)
    raise ValueError("Unsupported country. Use 'US', 'CA', or 'AU'.")

def fetch_random_user(api_url: str = "https://randomuser.me/api/", params: dict = None) -> dict:
    """
    Fetch a random user from the Random User Generator API.
    """
    params = params or {}
    response = requests.get(api_url, params=params)
    response.raise_for_status()  # Raise an error for HTTP issues
    data = response.json()
    if "results" not in data or not data["results"]:
        raise ValueError("No results returned from the API.")
    return data["results"][0]

def _random_nanp_phone() -> str:
    """Generate NANP phone with realistic area codes"""
    area = random.choice(_US_AREA_CODES)
    exchange = f"{random.randint(2,9)}{random.randint(0,9)}{random.randint(0,9)}"
    subscriber = f"{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}"
    return f"({area}) {exchange}-{subscriber}"

def _random_au_mobile() -> str:
    # AU mobile: 04xx xxx xxx
    return f"04{random.randint(10,99)} {random.randint(100,999)} {random.randint(100,999)}"

def random_phone(country: str = "US") -> str:
    c = country.upper().strip()
    if c in ("US", "CA", "CAN", "CANADA"):
        return _random_nanp_phone()
    if c in ("AU", "AUS", "AUSTRALIA"):
        return _random_au_mobile()
    return _random_nanp_phone()

# --- Simple CLI ---
def _cli():
    ap = argparse.ArgumentParser(description="Generate clearly fictitious identities.")
    ap.add_argument("--count", type=int, default=1, help="Number of identities")
    ap.add_argument("--country", type=str, default="US", help="US | CA | AU")
    ap.add_argument("--format-valid", action="store_true",
                    help="If set, generate format-valid addresses (may coincidentally exist).")
    ap.add_argument("--use-api", action="store_true",
                    help="If set, fetch random user data from the Random User Generator API.")
    args = ap.parse_args()

    for _ in range(args.count):
        if args.use_api:
            user = fetch_random_user(params={"nat": args.country.lower(), "results": 1})
            person = {
                "first_name": user["name"]["first"],
                "last_name": user["name"]["last"],
            }
            addr = {
                "line1": f"{user['location']['street']['number']} {user['location']['street']['name']}",
                "city": user["location"]["city"],
                "region": user["location"]["state"],
                "postcode": user["location"]["postcode"],
                "country": user["location"]["country"],
            }
            email = user["email"]
        else:
            person = random_person()
            addr = random_address(country=args.country, guarantee_nonexistent=not args.format_valid)
            email = random_email(person["first_name"], person["last_name"])
        
        print({
            "first_name": person["first_name"],
            "last_name": person["last_name"],
            "email": email,
            "address": addr,
        })

if __name__ == "__main__":
    _cli()
