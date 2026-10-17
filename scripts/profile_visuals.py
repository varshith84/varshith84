"""Self-contained SVG artwork for the GitHub profile; standard library only."""

from datetime import date, timedelta
from html import escape

BG = "#0F0B12"
INK = "#F8F0F3"
ROSE = "#E5B5C7"
MUTED = "#B79BAA"
LINE = "#583044"


def text(x, y, value, size=20, color=INK, family="Arial,Helvetica,sans-serif", **attrs):
    extra = " ".join(f'{key.replace("_", "-")}="{escape(str(v))}"' for key, v in attrs.items())
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" {extra}>{escape(str(value))}</text>'


def serif(x, y, value, size=42, **attrs):
    return text(x, y, value, size=size, family="Georgia,Times,serif", **attrs)


def rect(x, y, width, height, fill="#1C101A", stroke=LINE, radius=14, **attrs):
    extra = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}" stroke="{stroke}" {extra}/>'


def path(d, color=ROSE, width=2, **attrs):
    extra = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def svg(width, height, title, content, description=None):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="pv-title pv-description">
<title id="pv-title">{escape(title)}</title><desc id="pv-description">{escape(description or title)}</desc>
<defs>
<linearGradient id="pv-wine" x2="1" y2="1"><stop stop-color="#23101E"/><stop offset=".55" stop-color="#451126"/><stop offset="1" stop-color="#771F48"/></linearGradient>
<linearGradient id="pv-soft" x2="1" y2=".7"><stop stop-color="#24101D"/><stop offset="1" stop-color="#140D16"/></linearGradient>
<linearGradient id="pv-stroke"><stop stop-color="#70334F"/><stop offset=".5" stop-color="#E5B5C7"/><stop offset="1" stop-color="#70334F"/></linearGradient>
<radialGradient id="pv-halo"><stop stop-color="#BB477A" stop-opacity=".35"/><stop offset="1" stop-color="#BB477A" stop-opacity="0"/></radialGradient>
<pattern id="pv-grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#E5B5C7" stroke-opacity=".045"/></pattern>
<clipPath id="pv-portrait"><rect x="0" y="0" width="240" height="288" rx="110"/></clipPath>
</defs>
<style>
@keyframes pv-blink{{0%,45%{{opacity:1}}50%,95%{{opacity:.15}}100%{{opacity:1}}}}
@keyframes pv-pulse{{0%,100%{{opacity:.4}}50%{{opacity:.95}}}}
.cursor{{animation:pv-blink 1.8s steps(1) infinite}}.pulse{{animation:pv-pulse 4s ease-in-out infinite}}
@media(prefers-reduced-motion:reduce){{.motion{{display:none}}.cursor,.pulse{{animation:none}}}}
</style>
<rect width="{width}" height="{height}" fill="{BG}"/>
{''.join(content)}
</svg>\n'''


def eyebrow(x, y, value, size=13):
    return text(x, y, value, size, ROSE, letter_spacing="2")


def section_title(label, title, subtitle="", mobile=False):
    width = 600 if mobile else 1200
    c = [eyebrow(28 if mobile else 40, 35, label), serif(28 if mobile else 40, 91, title, 37 if mobile else 46)]
    if subtitle:
        c.append(text(40, 128, subtitle, 18, MUTED))
    return svg(width, 145 if subtitle else 115, title, c)


def render_activity(days, retrieved, mobile=False):
    """Recolor actual GitHub cells; statistics are derived only from those cells."""
    width, height = (600, 840) if mobile else (1200, 565)
    first = date.fromisoformat(days[0]["date"])
    sunday = first - timedelta(days=(first.weekday() + 1) % 7)
    total = sum(day["count"] for day in days)
    active = sum(day["count"] > 0 for day in days)
    run = longest = 0
    for day in days:
        run = run + 1 if day["count"] else 0
        longest = max(longest, run)
    c = [eyebrow(28 if mobile else 40, 35, "04 / ACTIVITY LOG"), serif(28 if mobile else 40, 92, "A year of building.", 39 if mobile else 46)]
    metrics = [(str(total), "PUBLIC CONTRIBUTIONS"), (str(active), "ACTIVE DAYS"), (str(longest), "LONGEST RUN / DAYS")]
    for i, (value, label) in enumerate(metrics):
        x = 28 + i * 184 if mobile else 40 + i * 375
        w = 176 if mobile else 360
        c.extend([rect(x, 125, w, 111, fill="url(#pv-soft)"), serif(x + 20, 184, value, 42 if mobile else 48), text(x + 20, 213, label, 10 if mobile else 13, ROSE, letter_spacing="1")])
    colors = ["#281823", "#52213B", "#8A2B55", "#C77B9B", "#F1C4D6"]
    c.append(rect(28 if mobile else 40, 263, 544 if mobile else 1120, 429 if mobile else 224, fill="#150D16"))
    if mobile:
        # Two chronological panels keep every genuine day readable on narrow screens.
        c.extend([text(48, 293, "PUBLIC GITHUB CALENDAR", 14, ROSE, letter_spacing="1.5"), text(48, 465, "CONTINUED →", 13, MUTED)])
    seen_months = set()
    for day in days:
        value = date.fromisoformat(day["date"])
        column, row = divmod((value - sunday).days, 7)
        panel = column // 27 if mobile else 0
        px = column % 27 if mobile else column
        x = (49 if mobile else 90) + px * (18 if mobile else 19.3)
        y = (323 + panel * 172 if mobile else 314) + row * (17 if mobile else 20)
        month_key = (panel, value.year, value.month)
        if month_key not in seen_months and (value.day <= 7 or not seen_months):
            c.append(text(x, y - row * (17 if mobile else 20) - 11, value.strftime("%b"), 11 if mobile else 12, MUTED))
            seen_months.add(month_key)
        c.append(f'<rect x="{x:.1f}" y="{y}" width="{13 if mobile else 15}" height="{13 if mobile else 15}" rx="2.5" fill="{colors[day["level"]]}"><title>{day["date"]}: {day["count"]} contributions</title></rect>')
    if not mobile:
        for label, row in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
            c.append(text(54, 325 + row * 20, label, 11, MUTED))
    y = 728 if mobile else 522
    c.extend([text(28 if mobile else 40, y, f'{days[0]["date"]} → {days[-1]["date"]}', 16 if mobile else 15, ROSE), text(28 if mobile else 40, y + 29, f"Retrieved {retrieved} UTC · Genuine GitHub public data", 14 if mobile else 14, MUTED)])
    if mobile:
        c.append(text(28, y + 57, "Dated snapshot. Updated by the repository workflow.", 14, MUTED))
    else:
        c.extend([text(927, 522, "LESS", 11, MUTED)])
        for i, color in enumerate(colors):
            c.append(rect(971 + i * 23, 509, 16, 16, fill=color, stroke="none", radius=3))
        c.append(text(1093, 522, "MORE", 11, MUTED))
    return svg(width, height, "Varshith's genuine GitHub contribution calendar", c, f"Public contribution data from {days[0]['date']} to {days[-1]['date']}. Retrieved {retrieved} UTC. {total} contributions, {active} active days, longest run {longest} days within this displayed range.")
