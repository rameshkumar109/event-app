import os
import time
import requests
from datetime import datetime, timedelta

# Popular cities database
POPULAR_CITIES = [
    # Europe
    {"name": "London", "country": "United Kingdom", "emoji": "🇬🇧", "region": "Europe"},
    {"name": "Paris", "country": "France", "emoji": "🇫🇷", "region": "Europe"},
    {"name": "Berlin", "country": "Germany", "emoji": "🇩🇪", "region": "Europe"},
    {"name": "Amsterdam", "country": "Netherlands", "emoji": "🇳🇱", "region": "Europe"},
    {"name": "Barcelona", "country": "Spain", "emoji": "🇪🇸", "region": "Europe"},
    {"name": "Rome", "country": "Italy", "emoji": "🇮🇹", "region": "Europe"},
    {"name": "Vienna", "country": "Austria", "emoji": "🇦🇹", "region": "Europe"},
    {"name": "Prague", "country": "Czech Republic", "emoji": "🇨🇿", "region": "Europe"},
    {"name": "Budapest", "country": "Hungary", "emoji": "🇭🇺", "region": "Europe"},
    {"name": "Athens", "country": "Greece", "emoji": "🇬🇷", "region": "Europe"},
    {"name": "Stockholm", "country": "Sweden", "emoji": "🇸🇪", "region": "Europe"},
    {"name": "Copenhagen", "country": "Denmark", "emoji": "🇩🇰", "region": "Europe"},
    
    # Asia
    {"name": "Tokyo", "country": "Japan", "emoji": "🇯🇵", "region": "Asia"},
    {"name": "Mumbai", "country": "India", "emoji": "🇮🇳", "region": "Asia"},
    {"name": "Delhi", "country": "India", "emoji": "🇮🇳", "region": "Asia"},
    {"name": "Singapore", "country": "Singapore", "emoji": "🇸🇬", "region": "Asia"},
    {"name": "Bangkok", "country": "Thailand", "emoji": "🇹🇭", "region": "Asia"},
    {"name": "Hong Kong", "country": "Hong Kong", "emoji": "🇭🇰", "region": "Asia"},
    {"name": "Seoul", "country": "South Korea", "emoji": "🇰🇷", "region": "Asia"},
    {"name": "Shanghai", "country": "China", "emoji": "🇨🇳", "region": "Asia"},
    {"name": "Beijing", "country": "China", "emoji": "🇨🇳", "region": "Asia"},
    {"name": "Dubai", "country": "United Arab Emirates", "emoji": "🇦🇪", "region": "Asia"},
    {"name": "Abu Dhabi", "country": "United Arab Emirates", "emoji": "🇦🇪", "region": "Asia"},
    {"name": "Istanbul", "country": "Turkey", "emoji": "🇹🇷", "region": "Asia"},
    
    # Americas
    {"name": "New York", "country": "United States", "emoji": "🇺🇸", "region": "Americas"},
    {"name": "Los Angeles", "country": "United States", "emoji": "🇺🇸", "region": "Americas"},
    {"name": "Chicago", "country": "United States", "emoji": "🇺🇸", "region": "Americas"},
    {"name": "Toronto", "country": "Canada", "emoji": "🇨🇦", "region": "Americas"},
    {"name": "Vancouver", "country": "Canada", "emoji": "🇨🇦", "region": "Americas"},
    {"name": "Mexico City", "country": "Mexico", "emoji": "🇲🇽", "region": "Americas"},
    {"name": "São Paulo", "country": "Brazil", "emoji": "🇧🇷", "region": "Americas"},
    {"name": "Rio de Janeiro", "country": "Brazil", "emoji": "🇧🇷", "region": "Americas"},
    {"name": "Buenos Aires", "country": "Argentina", "emoji": "🇦🇷", "region": "Americas"},
    
    # Oceania
    {"name": "Sydney", "country": "Australia", "emoji": "🇦🇺", "region": "Oceania"},
    {"name": "Melbourne", "country": "Australia", "emoji": "🇦🇺", "region": "Oceania"},
    {"name": "Auckland", "country": "New Zealand", "emoji": "🇳🇿", "region": "Oceania"},
    
    # Africa
    {"name": "Cairo", "country": "Egypt", "emoji": "🇪🇬", "region": "Africa"},
    {"name": "Lagos", "country": "Nigeria", "emoji": "🇳🇬", "region": "Africa"},
    {"name": "Cape Town", "country": "South Africa", "emoji": "🇿🇦", "region": "Africa"},
    {"name": "Johannesburg", "country": "South Africa", "emoji": "🇿🇦", "region": "Africa"},
]

# Simple in-memory cache for external city list
_CACHE = {
    "popular": {"data": None, "ts": 0}
}

GEONAMES_USERNAME = os.getenv("GEONAMES_USERNAME", "demo")
GEONAMES_MAX = int(os.getenv("GEONAMES_MAX", "200"))
CACHE_TTL = int(os.getenv("CITIES_CACHE_TTL_SECONDS", str(60 * 60 * 24)))  # 24h default


def country_code_to_emoji(code):
    if not code or len(code) != 2:
        return "📍"
    try:
        # Build flag emoji from ASCII country code letters
        return ''.join(chr(127397 + ord(c)) for c in code.upper())
    except Exception:
        # fallback manual conversion
        try:
            return ''.join(chr(127397 + ord(c)) for c in code.upper())
        except Exception:
            return "📍"


def fetch_popular_cities_external(limit=GEONAMES_MAX):
    """Fetch popular cities using GeoNames (ordered by population) and enrich with region via REST Countries API.
    Requires GEONAMES_USERNAME env var (defaults to 'demo' but demo is limited).
    Returns list of city dicts with keys: name, country, emoji, region
    """
    username = GEONAMES_USERNAME
    if not username:
        raise RuntimeError("GEONAMES_USERNAME not configured")

    url = f"http://api.geonames.org/searchJSON?featureClass=P&orderby=population&maxRows={limit}&username={username}"
    resp = requests.get(url, timeout=6)
    resp.raise_for_status()
    data = resp.json()
    geonames = data.get("geonames", [])

    # collect unique country codes to fetch regions
    country_codes = {g.get("countryCode") for g in geonames if g.get("countryCode")}
    country_region = {}
    for code in country_codes:
        try:
            r = requests.get(f"https://restcountries.com/v3.1/alpha/{code}", timeout=5)
            if r.status_code == 200:
                info = r.json()
                if isinstance(info, list) and len(info) > 0:
                    region = info[0].get("region", "")
                else:
                    region = info.get("region", "")
                country_region[code] = region
            else:
                country_region[code] = ""
        except Exception:
            country_region[code] = ""

    results = []
    seen = set()
    for g in geonames:
        name = g.get("name")
        country = g.get("countryName") or ""
        code = g.get("countryCode") or ""
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        emoji = "📍"
        try:
            if code:
                # convert country code to emoji safely
                emoji = ''.join([chr(127397 + ord(c)) for c in code.upper()])
        except Exception:
            emoji = "📍"
        region = country_region.get(code, "")
        results.append({"name": name, "country": country, "emoji": emoji, "region": region})

    return results


def get_city_suggestions(search_text):
    """
    Get city suggestions based on alphabetic search text
    Matches cities starting with the search text (case-insensitive)
    Returns top 10 results sorted alphabetically
    """
    search_lower = search_text.lower().strip()
    
    if len(search_lower) == 0:
        return []
    
    # Prefer live external suggestions by prefix (GeoNames), fallback to cached list
    try:
        external = fetch_city_suggestions_external(search_lower, limit=10)
        if external:
            return external
    except Exception:
        pass

    # Fallback: use cached popular list and score locally
    try:
        cities_source = get_all_cities()
    except Exception:
        cities_source = POPULAR_CITIES

    # We'll collect matches with a relevance score so we can prioritize startswith > word-start > initials > contains
    scored = []

    for city in cities_source:
        city_name = city.get("name", "")
        name_lower = city_name.lower()

        score = None

        # Exact startswith
        if name_lower.startswith(search_lower):
            score = 100
        else:
            # Any word in the city starts with the search (e.g. 'new' matches 'New York')
            words = name_lower.split()
            if any(w.startswith(search_lower) for w in words):
                score = 80

        # Initials match (e.g., 'ny' → 'New York')
        if score is None:
            initials = "".join([w[0] for w in name_lower.split() if w])
            if initials.startswith(search_lower):
                score = 70

        # Substring match anywhere in the name (lower priority)
        if score is None and search_lower in name_lower:
            score = 50

        if score is not None:
            scored.append((score, city_name, city))

    # Sort by score desc, then alphabetically
    scored.sort(key=lambda x: (-x[0], x[1]))

    # Return only the city dicts (top 10)
    return [item[2] for item in scored][:10]


def fetch_city_suggestions_external(search_text, limit=10):
    """
    Fetch city suggestions from GeoNames by prefix.
    Requires GEONAMES_USERNAME env var (free account or demo for limited use).
    """
    username = GEONAMES_USERNAME
    if not username:
        raise RuntimeError("GEONAMES_USERNAME not configured")

    url = (
        "http://api.geonames.org/searchJSON"
        f"?name_startsWith={requests.utils.quote(search_text)}"
        f"&featureClass=P&maxRows={int(limit)}&username={username}"
    )
    resp = requests.get(url, timeout=6)
    resp.raise_for_status()
    data = resp.json()
    geonames = data.get("geonames", [])

    results = []
    seen = set()
    for g in geonames:
        name = g.get("name")
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        country = g.get("countryName") or ""
        code = g.get("countryCode") or ""
        emoji = country_code_to_emoji(code)
        results.append({"name": name, "country": country, "emoji": emoji, "region": ""})

    return results


def get_all_cities():
    """
    Get all cities sorted alphabetically
    """
    # Use cached external list when available
    try:
        now = int(time.time())
        cached = _CACHE.get("popular", {})
        if cached and cached.get("data") and (now - cached.get("ts", 0) < CACHE_TTL):
            cities = cached.get("data")
        else:
            try:
                fetched = fetch_popular_cities_external()
                # Only use fetched list if non-empty
                if fetched and len(fetched) > 0:
                    cities = fetched
                    _CACHE["popular"] = {"data": cities, "ts": now}
                else:
                    # fallback to bundled list
                    cities = POPULAR_CITIES
            except Exception as e:
                # Log in server logs and fallback
                try:
                    import logging
                    logging.warning(f"fetch_popular_cities_external failed: {e}")
                except Exception:
                    pass
                cities = POPULAR_CITIES

        # ensure consistent shape and sort
        cities_sorted = sorted(cities, key=lambda x: x.get("name", ""))
        return cities_sorted
    except Exception:
        return sorted(POPULAR_CITIES, key=lambda x: x["name"])


def get_cities_by_region(region):
    """
    Get cities filtered by region
    """
    region_lower = region.lower()
    cities = [city for city in POPULAR_CITIES if city.get("region", "").lower() == region_lower]
    cities.sort(key=lambda x: x["name"])
    return cities


def get_cities_by_country(country):
    """
    Get cities filtered by country
    """
    country_lower = country.lower()
    cities = [city for city in POPULAR_CITIES if city.get("country", "").lower() == country_lower]
    cities.sort(key=lambda x: x["name"])
    return cities


def get_available_regions():
    """
    Get all available regions
    """
    regions = list(set([city.get("region", "") for city in POPULAR_CITIES]))
    regions.sort()
    return regions


def get_available_countries():
    """
    Get all available countries
    """
    countries = list(set([city.get("country", "") for city in POPULAR_CITIES]))
    countries.sort()
    return countries
