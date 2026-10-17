#!/usr/bin/env python3
"""Render a dated SVG from GitHub's public contribution calendar. No token needed."""

import argparse
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.cells = {}
        self.labels = {}
        self.label_target = None
        self.label_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-date" in attrs:
            day = date.fromisoformat(attrs["data-date"])
            level = int(attrs["data-level"])
            if not 0 <= level <= 4:
                raise ValueError("Unexpected contribution intensity")
            self.cells[attrs["id"]] = {"date": day.isoformat(), "level": level}
        if tag == "tool-tip":
            self.label_target = attrs.get("for")
            self.label_text = []

    def handle_data(self, data):
        if self.label_target:
            self.label_text.append(data)

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.label_target:
            self.labels[self.label_target] = "".join(self.label_text).strip()
            self.label_target = None

    def records(self):
        days = []
        for cell_id, cell in self.cells.items():
            label = self.labels.get(cell_id, "")
            if re.match(r"No contributions\b", label):
                count = 0
            else:
                match = re.match(r"([\d,]+) contributions?\b", label)
                if not match:
                    raise ValueError("GitHub calendar format changed: missing day count")
                count = int(match.group(1).replace(",", ""))
            if (count == 0) != (cell["level"] == 0):
                raise ValueError("Contribution count and intensity disagree")
            days.append({**cell, "count": count})
        days.sort(key=lambda item: item["date"])
        dates = [date.fromisoformat(item["date"]) for item in days]
        if not 350 <= len(days) <= 378 or len(set(dates)) != len(dates):
            raise ValueError("Expected one complete year of unique contribution days")
        if any(b - a != timedelta(days=1) for a, b in zip(dates, dates[1:])):
            raise ValueError("Contribution calendar has gaps")
        return days


def render(days, retrieved):
    colors = ["#24131D", "#451126", "#701A3D", "#C77B9B", "#E5B5C7"]
    first = date.fromisoformat(days[0]["date"])
    sunday = first - timedelta(days=(first.weekday() + 1) % 7)
    total = sum(day["count"] for day in days)
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="310" viewBox="0 0 1200 310" role="img" aria-labelledby="vc-title vc-desc">',
        '<title id="vc-title">Public GitHub contribution calendar for varshith84</title>',
        f'<desc id="vc-desc">Genuine GitHub contribution data from {days[0]["date"]} to {days[-1]["date"]}. Retrieved {escape(retrieved)}. {total} contributions in this displayed range.</desc>',
        '<rect width="1200" height="310" rx="18" fill="#10070C"/>',
        '<rect x=".5" y=".5" width="1199" height="309" rx="18" fill="none" stroke="#451126"/>',
        '<g font-family="Arial,Helvetica,sans-serif">',
        '<text x="40" y="43" fill="#F8F0F3" font-size="21">A year of building</text>',
        f'<text x="1160" y="42" text-anchor="end" fill="#E5B5C7" font-size="14">{total:,} public contributions</text>',
    ]
    months = set()
    for day in days:
        value = date.fromisoformat(day["date"])
        column, row = divmod((value - sunday).days, 7)
        x, y = 80 + column * 20, 87 + row * 20
        month_key = (value.year, value.month)
        if month_key not in months and (value.day <= 7 or not months):
            parts.append(f'<text x="{x}" y="73" font-size="12" fill="#C77B9B">{value.strftime("%b")}</text>')
            months.add(month_key)
        parts.append(
            f'<rect x="{x}" y="{y}" width="15" height="15" rx="3" fill="{colors[day["level"]]}"><title>{day["date"]}: {day["count"]} contributions</title></rect>'
        )
    for label, row in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        parts.append(f'<text x="40" y="{98 + row * 20}" fill="#C77B9B" font-size="11">{label}</text>')
    parts.extend([
        f'<text x="40" y="262" fill="#E5B5C7" font-size="13">{days[0]["date"]} — {days[-1]["date"]}</text>',
        f'<text x="40" y="286" fill="#C77B9B" font-size="11">Source: GitHub public calendar · Retrieved {escape(retrieved)} · Dated snapshot</text>',
        '<text x="944" y="274" fill="#C77B9B" font-size="12">Less</text>',
    ])
    for index, color in enumerate(colors):
        parts.append(f'<rect x="{980 + index * 20}" y="262" width="15" height="15" rx="3" fill="{color}"/>')
    parts.extend(['<text x="1088" y="274" fill="#C77B9B" font-size="12">More</text>', '</g></svg>'])
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html-file", type=Path, help="Use an already retrieved GitHub calendar")
    parser.add_argument("--retrieved-date", type=date.fromisoformat, help="Date the supplied HTML was retrieved (UTC)")
    args = parser.parse_args()
    if args.html_file:
        if not args.retrieved_date:
            parser.error("--html-file requires --retrieved-date")
        html = args.html_file.read_text(encoding="utf-8")
        retrieved = args.retrieved_date.isoformat()
    else:
        if args.retrieved_date:
            parser.error("--retrieved-date is only for an existing HTML snapshot")
        request = urllib.request.Request(
            "https://github.com/users/varshith84/contributions",
            headers={"User-Agent": "varshith84-profile-calendar", "Accept": "text/html", "Accept-Language": "en-US"},
        )
        with urllib.request.urlopen(request, timeout=45) as response:
            html = response.read().decode("utf-8")
        retrieved = datetime.now(timezone.utc).date().isoformat()
    calendar = CalendarParser()
    calendar.feed(html)
    days = calendar.records()
    root = Path(__file__).resolve().parents[1]
    assets = root / "assets"
    assets.mkdir(exist_ok=True)
    data = {"username": "varshith84", "source": "https://github.com/users/varshith84/contributions", "retrieved_date_utc": retrieved, "days": days}
    # Validate and render everything before replacing either last-good output.
    svg = render(days, retrieved)
    payload = json.dumps(data, indent=2) + "\n"
    for path, content in [(assets / "contributions.svg", svg), (assets / "contributions.json", payload)]:
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(path)
    print(f"Updated contribution calendar: {len(days)} genuine day records; retrieved {retrieved}")


if __name__ == "__main__":
    main()
