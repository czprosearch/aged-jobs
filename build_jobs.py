import json, datetime, requests
from dateutil import parser

# Edit these lists with the companies you care about.
# Use the company's Greenhouse/Lever slug (what appears in the URL).
COMPANIES = {
    "greenhouse": ["asana", "datadog", "mongodb"],   # examples; replace with your list
    "lever": ["rippling", "segment", "benchling"],   # examples; replace with your list
}

DAYS_OLD = 30

def older_than_days(dt_str, days=DAYS_OLD):
    dt = parser.parse(dt_str)
    # naive-ify
    if dt.tzinfo:
        dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return (datetime.datetime.utcnow() - dt).days > days

def fetch_greenhouse(slug):
    url = f"https://boards.greenhouse.io/{slug}.json"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    out = []
    for job in r.json().get("jobs", []):
        posted = job.get("updated_at") or job.get("created_at")
        if posted and older_than_days(posted):
            out.append({
                "source": "greenhouse",
                "company": slug,
                "title": job.get("title"),
                "location": (job.get("location") or {}).get("name"),
                "url": job.get("absolute_url"),
                "postedAt": posted,
            })
    return out

def fetch_lever(slug):
    url = f"https://jobs.lever.co/{slug}.json"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    out = []
    for job in r.json():
        posted = job.get("createdAt") or job.get("listedAt")
        # Normalize Lever timestamps (often ms since epoch)
        if isinstance(posted, (int, float)):
            posted_dt = datetime.datetime.utcfromtimestamp(posted/1000).isoformat() + "Z"
        else:
            posted_dt = posted
        if posted_dt and older_than_days(posted_dt):
            out.append({
                "source": "lever",
                "company": slug,
                "title": job.get("text"),
                "location": (job.get("categories") or {}).get("location"),
                "url": job.get("hostedUrl") or job.get("applyUrl"),
                "postedAt": posted_dt,
            })
    return out

def main():
    results = []
    for gh in COMPANIES["greenhouse"]:
        try:
            results.extend(fetch_greenhouse(gh))
        except Exception as e:
            print(f"[warn] greenhouse {gh}: {e}")
    for lv in COMPANIES["lever"]:
        try:
            results.extend(fetch_lever(lv))
        except Exception as e:
            print(f"[warn] lever {lv}: {e}")

    # Exclude obvious recruiting agencies
    filtered = [r for r in results if r.get("company") and "recruit" not in r["company"].lower() and "staff" not in r["company"].lower()]
    filtered.sort(key=lambda x: (x.get("company") or "", x.get("title") or ""))

    with open("jobs_30plus.json", "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)

    print(f"Wrote jobs_30plus.json with {len(filtered)} records.")

if __name__ == "__main__":
    main()
