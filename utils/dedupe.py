import os
import json

SENT_FILE = "sent_matches.json"

def load_sent_matches():
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r") as f:
        return set(json.load(f))

def save_sent_matches(match_keys):
    with open(SENT_FILE, "w") as f:
        json.dump(match_keys, f)
