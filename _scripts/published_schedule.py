"""Convert the panel's public response to the data used by the homepage."""
import hashlib
import json
import sys
from datetime import datetime
from urllib.parse import urlsplit


def snapshot(feed):
    items = feed["items"]
    if not isinstance(items, list):
        raise ValueError("The panel has no published schedule")
    shows = []
    for item in items:
        if item.get("offSale"):
            continue
        show = {key: item.get(key, "") for key in ("day", "time", "city", "venue", "address", "ticket")}
        if not all(isinstance(value, str) for value in show.values()):
            raise ValueError("Invalid show fields")
        datetime.strptime(show["day"] + " " + show["time"], "%Y-%m-%d %H:%M")
        url = urlsplit(show["ticket"])
        if not show["venue"].strip() or url.scheme not in ("http", "https") or not url.hostname:
            raise ValueError("Invalid venue or ticket link")
        shows.append(show)
    serialized = json.dumps(shows, ensure_ascii=False, sort_keys=True).encode()
    return {"version": hashlib.sha256(serialized).hexdigest(), "items": shows}


if __name__ == "__main__":
    print(json.dumps(snapshot(json.load(sys.stdin)), ensure_ascii=False, indent=2))
