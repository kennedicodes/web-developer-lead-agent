import hashlib
import json
import os
from datetime import date

PROGRESS_FILE = "search_progress.json"
DAILY_FILE = "daily_leads.json"  # leads added today, for the daily cap


def leads_added_today():
    if os.path.exists(DAILY_FILE):
        with open(DAILY_FILE) as f:
            data = json.load(f)
        if data.get("date") == date.today().isoformat():
            return data["leads"]
    return 0


def record_lead():
    count = leads_added_today() + 1
    with open(DAILY_FILE, "w") as f:
        json.dump({"date": date.today().isoformat(), "leads": count}, f)


def query_signature(queries):
    """Fingerprint of the query list, so saved progress resets when the list changes."""
    return hashlib.md5(json.dumps(queries).encode()).hexdigest()


def load_progress(signature):
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            data = json.load(f)
        if data.get("signature") == signature:
            return data["query_index"]
    return 0


def save_progress(query_index, signature):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"query_index": query_index, "signature": signature}, f)
