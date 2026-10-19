import hashlib
import json
import os

PROGRESS_FILE = "search_progress.json"


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
