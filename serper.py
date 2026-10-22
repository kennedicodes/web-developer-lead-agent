import json
import os
import re
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from config import DIRECTORY_DOMAINS, MAX_SERPER_CREDITS_PER_MONTH

MAPS_URL = "https://google.serper.dev/maps"
KEY_FILE = "serper_api_key.txt"
USAGE_FILE = "serper_usage.json"  # credits used this month


def _api_key():
    key = os.environ.get("SERPER_API_KEY", "").strip()
    if not key and os.path.exists(KEY_FILE):
        with open(KEY_FILE) as f:
            key = f.read().strip()
    if not key:
        raise SystemExit(
            f"No Serper API key found. Put the key in {KEY_FILE} or set the SERPER_API_KEY environment variable."
        )
    return key


def _load_usage():
    month = date.today().strftime("%Y-%m")
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE) as f:
            usage = json.load(f)
        if usage.get("month") == month:
            return usage
    return {"month": month, "credits": 0}


def credits_this_month():
    return _load_usage()["credits"]


def quota_reached():
    return credits_this_month() >= MAX_SERPER_CREDITS_PER_MONTH


def _record_credits(credits):
    usage = _load_usage()
    usage["credits"] += credits
    with open(USAGE_FILE, "w") as f:
        json.dump(usage, f)


def _is_directory(url):
    host = urlparse(url).netloc.lower().split(":")[0]
    return any(host == d or host.endswith("." + d) for d in DIRECTORY_DOMAINS)


def _city_state(address, fallback):
    """'4100 Corporate Square, Naples, FL 34104' -> 'Naples, FL'"""
    m = re.search(r"([^,]+),\s*([A-Z]{2})\s+\d{5}", address or "")
    return f"{m.group(1).strip()}, {m.group(2)}" if m else fallback


def search_businesses(keyword, city, page=1, ll=None):
    """
    One page (20 results) of Google Maps businesses for "<keyword> in <city>" via Serper.
    Pages after the first need the map location (ll) returned by page 1.
    Returns (businesses, ll), or (None, None) if the request failed.
    Each business: {id, name, phone, website, city_state}. A Facebook/Yelp/booking page doesn't count as a website.
    """
    body = {"q": f"{keyword} in {city}"}
    if page > 1:
        body.update({"page": page, "ll": ll})

    req = Request(
        MAPS_URL,
        data=json.dumps(body).encode(),
        headers={"X-API-KEY": _api_key(), "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except HTTPError as e:
        print(f"  Serper error {e.code}: {e.read().decode(errors='ignore')[:200]}")
        return None, None
    except (URLError, TimeoutError, OSError) as e:
        print(f"  Serper request failed: {e}")
        return None, None
    _record_credits(data.get("credits", 3))

    businesses = []
    for place in data.get("places", []):
        site = place.get("website", "")
        businesses.append({
            "id": place.get("cid") or place.get("placeId") or place.get("title"),
            "name": place.get("title", ""),
            "phone": place.get("phoneNumber", ""),
            "website": "" if not site or _is_directory(site) else site,
            "city_state": _city_state(place.get("address", ""), city),
        })
    return businesses, data.get("ll", ll)
