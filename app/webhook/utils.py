from datetime import datetime, timezone

def parse_github_timestamp(ts):
    if ts.endswith("Z"):
        ts = ts.replace("Z", "+00:00")

    dt = datetime.fromisoformat(ts)
    return dt.astimezone(timezone.utc)
