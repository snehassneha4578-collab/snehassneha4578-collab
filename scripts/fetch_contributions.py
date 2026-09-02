import json
import re
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

USERNAME = "snehassneha4578-collab"
URL = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for cell in soup.select("td.ContributionCalendar-day"):
    date = cell.get("data-date")
    count_text = cell.get("data-count")

    if not date:
        continue

    count = int(count_text or 0)

    days.append({
        "date": date,
        "count": count
    })

if not days:
    raise RuntimeError("No contribution data found.")

output = {
    "username": USERNAME,
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "days": days
}

with open("data/contributions.json", "w", encoding="utf-8") as file:
    json.dump(output, file, indent=2)

print(f"Fetched {len(days)} contribution days for {USERNAME}")
