import json
import os
import time
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from config import DIRECTORY_DOMAINS, MAX_PLACES_CALLS_PER_MONTH

PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = (
    "places.displayName,places.nationalPhoneNumber,places.websiteUri,"
    "places.businessStatus,places.addressComponents,nextPageToken"
)
KEY_FILE = "places_api_key.txt"
USAGE_FILE = "places_usage.json"  # API calls made this month


def _api_key():
    key = os.environ.get("GOOGLE_PLACES_API_KEY", "").strip()
    if not key and os.path.exists(KEY_FILE):
        with open(KEY_FILE) as f:
            key = f.read().strip()
    if not key:
        raise SystemExit(
            "No Google Places API key found. Set the GOOGLE_PLACES_API_KEY environment variable "
            f"or put the key in {KEY_FILE}."
        )
    return key


def _load_usage():
    month = date.today().strftime("%Y-%m")
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE) as f:
            usage = json.load(f)
        if usage.get("month") == month:
            return usage
    return {"month": month, "calls": 0}


def calls_this_month():
    return _load_usage()["calls"]


def quota_reached():
    return calls_this_month() >= MAX_PLACES_CALLS_PER_MONTH


def _record_call():
    usage = _load_usage()
    usage["calls"] += 1
    with open(USAGE_FILE, "w") as f:
        json.dump(usage, f)


def _is_directory(url):
    host = urlparse(url).netloc.lower().split(":")[0]
    return any(host == d or host.endswith("." + d) for d in DIRECTORY_DOMAINS)


def _city_state(place, fallback):
    parts = {}
    for comp in place.get("addressComponents", []):
        for t in comp.get("types", []):
            parts.setdefault(t, comp.get("shortText", ""))
    city = parts.get("locality") or parts.get("sublocality") or parts.get("neighborhood")
    state = parts.get("administrative_area_level_1")
    return f"{city}, {state}" if city and state else fallback


def search_businesses(keyword, city, page_token=None):
    """
    One page (up to 20) of Google Maps businesses for "<keyword> in <city>".
    Returns (businesses, next_page_token), or (None, None) if the request failed.
    Each business: {name, phone, website, city_state, open}. A Facebook/Yelp/booking page doesn't count as a website.
    """
    body = {"textQuery": f"{keyword} in {city}", "pageSize": 20}
    if page_token:
        body["pageToken"] = page_token
        time.sleep(2)  # Google needs a moment before a page token is valid

    req = Request(
        PLACES_URL,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": _api_key(),
            "X-Goog-FieldMask": FIELD_MASK,
        },
        method="POST",
    )
    _record_call()
    try:
        with urlopen(req, timeout=20) as resp:
            data = json.load(resp)
    except HTTPError as e:
        print(f"  Places API error {e.code}: {e.read().decode(errors='ignore')[:200]}")
        return None, None
    except (URLError, TimeoutError, OSError) as e:
        print(f"  Places API request failed: {e}")
        return None, None

    businesses = []
    for place in data.get("places", []):
        site = place.get("websiteUri", "")
        businesses.append({
            "name": place.get("displayName", {}).get("text", ""),
            "phone": place.get("nationalPhoneNumber", ""),
            "website": "" if not site or _is_directory(site) else site,
            "city_state": _city_state(place, city),
            "open": place.get("businessStatus", "OPERATIONAL") == "OPERATIONAL",
        })
    return businesses, data.get("nextPageToken")
