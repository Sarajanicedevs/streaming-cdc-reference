"""Deterministic per-key state machine for CDC event streams."""
def process(events):
    seen = set()
    state = {}
    dead_letter = []
    metrics = {"accepted": 0, "duplicates": 0, "stale": 0, "invalid": 0}
    for event in events:
        try:
            event_id = str(event["event_id"])
            key = str(event["key"])
            version = int(event["version"])
            op = str(event["op"])
            if not event_id or not key or version < 0 or op not in ("upsert","delete"):
                raise ValueError("invalid CDC envelope")
        except (KeyError, TypeError, ValueError):
            dead_letter.append(event)
            metrics["invalid"] += 1
            continue
        if event_id in seen:
            metrics["duplicates"] += 1
            continue
        seen.add(event_id)
        previous = state.get(key)
        if previous is not None and version <= previous["version"]:
            metrics["stale"] += 1
            continue
        state[key] = {"version": version, "value": event.get("value") if op == "upsert" else None, "deleted": op == "delete"}
        metrics["accepted"] += 1
    return {"state": state, "metrics": metrics, "dead_letter": dead_letter}
