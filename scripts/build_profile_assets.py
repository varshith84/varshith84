#!/usr/bin/env python3
"""Build the custom README's desktop and mobile SVGs."""

import base64
from pathlib import Path

from profile_visuals import BG, INK, ROSE, MUTED, LINE, eyebrow, path, rect, section_title, serif, svg, text

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def write(name, artwork):
    (ASSETS / name).write_text(artwork, encoding="utf-8")


def hero(mobile=False):
    w, h = (600, 520) if mobile else (1200, 452)
    image = base64.b64encode((ASSETS / "robot-portrait.jpg").read_bytes()).decode()
    c = [rect(1, 1, w - 2, h - 2, fill="url(#pv-wine)", radius=18), f'<rect width="{w}" height="{h}" fill="url(#pv-grid)"/>']
    c.append(f'<ellipse cx="{w - 140}" cy="160" rx="360" ry="300" fill="url(#pv-halo)"/>')
    c.extend([eyebrow(34 if mobile else 48, 49, "VARSHITH84 / DEVELOPER PROFILE", 12 if mobile else 14), text(34 if mobile else 48, 82, "FULL-STACK DEVELOPMENT  /  APPLIED AI", 12 if mobile else 13, ROSE, letter_spacing="1.5")])
    if mobile:
        c.extend([serif(30, 164, "Varshith Sai", 52), serif(30, 224, "Pasupuleti.", 52)])
        tx, ty, scale = 405, 102, .65
        c.extend([text(34, 286, "Aspiring Software Engineer", 23), text(34, 323, "Building useful software with", 20, ROSE), text(34, 354, "code, data, and curiosity.", 20, ROSE)])
        c.extend([path("M34 391H566", color="url(#pv-stroke)", width=1), text(34, 431, "KL UNIVERSITY", 15, ROSE, letter_spacing="1.6"), text(34, 465, "B.Tech CSE · 2023–2027 · Full-time", 18, INK)])
    else:
        c.extend([serif(42, 177, "Varshith Sai", 76, letter_spacing="-2"), serif(42, 259, "Pasupuleti.", 76, letter_spacing="-2")])
        tx, ty, scale = 900, 91, 1
        c.extend([text(48, 304, "Aspiring Software Engineer", 23), text(48, 342, "I build full-stack applications and explore applied AI.", 20, ROSE), path("M48 372H818", color="url(#pv-stroke)", width=1), text(48, 411, "KL UNIVERSITY  /  B.TECH CSE  /  2023–2027  /  FULL-TIME", 13, ROSE, letter_spacing="1.3")])
    c.append(f'<g transform="translate({tx} {ty}) scale({scale})"><rect x="-9" y="-9" width="258" height="306" rx="122" fill="#180D16" stroke="#B66B8E" stroke-opacity=".55"/><image xlink:href="data:image/jpeg;base64,{image}" width="240" height="288" preserveAspectRatio="xMidYMid slice" clip-path="url(#pv-portrait)"/><path d="M-8 160V85C-8-12 248-12 248 85V160" fill="none" stroke="#E5B5C7" stroke-width="1" opacity=".6"/><circle class="pulse" cx="220" cy="274" r="7" fill="#F1C4D6"/></g>')
    c.append(f'<path class="motion" d="M34 {h-19}H{w-34}" stroke="#E5B5C7" stroke-width="1" stroke-dasharray="55 {w}"><animate attributeName="stroke-dashoffset" from="{w}" to="{-w}" dur="18s" repeatCount="indefinite"/></path>')
    return svg(w, h, "Varshith Sai Pasupuleti — full-stack development and applied AI", c)


def about(mobile=False):
    w, h = (600, 800) if mobile else (1200, 560)
    c = [eyebrow(28 if mobile else 40, 37, "01 / PLAYER PROFILE"), serif(28 if mobile else 40, 96, "Hello, I'm Varshith.", 38 if mobile else 46)]
    x, y, tw, th = (28, 132, 544, 438) if mobile else (40, 136, 760, 376)
    c.extend([rect(x, y, tw, th, fill="#160F18"), rect(x, y, tw, 45, fill="#2A1323", radius=13)])
    for i, color in enumerate(["#C77B9B", "#9C617D", "#6B4058"]):
        c.append(f'<circle cx="{x+22+i*19}" cy="{y+23}" r="5" fill="{color}"/>')
    c.append(text(x + 98, y + 29, "developer.config", 14, MUTED, family="monospace"))
    rows = [
        ("const developer = {", ROSE),
        ('  name: "Varshith Sai Pasupuleti",', INK),
        ('  degree: "B.Tech CSE",', MUTED),
        ('  college: "KL University",', MUTED),
        ('  focus: ["Full-stack", "Applied AI"],', INK),
        ('  foundations: ["Python", "SQL", "DSA"],', INK),
        ('  mindset: "Learn. Build. Improve.",', MUTED),
        ('  next: "Software engineering"', INK),
        ("};", ROSE),
    ]
    for i, (value, color) in enumerate(rows):
        c.append(text(x + 23, y + 86 + i * (34 if mobile else 31), value, 19 if mobile else 20, color, family="monospace"))
    c.append(text(x + 23, y + th - 20, "$ ready_to_build", 16, ROSE, family="monospace"))
    c.append(rect(x + 188, y + th - 36, 8, 19, fill=ROSE, stroke="none", radius=0, **{"class": "cursor"}))
    cards = [("8.72", "CURRENT CGPA", "KL University"), ("2027", "GRADUATING BATCH", "Full-time B.Tech CSE"), ("5", "CERTIFICATIONS", "Cloud AI · Data · English")]
    for i, (number, label, note) in enumerate(cards):
        if mobile:
            cx, cy, cw, ch = 28 + i * 184, 598, 176, 170
            c.extend([rect(cx, cy, cw, ch, fill="url(#pv-soft)"), serif(cx + 17, cy + 61, number, 39), text(cx + 17, cy + 96, label, 9.5, ROSE, letter_spacing=".6")])
            notes = ["KL University", "Full-time CSE", "AI · Data · English"]
            c.append(text(cx + 17, cy + 129, notes[i], 13, MUTED))
        else:
            cx, cy, cw, ch = 827, 136 + i * 129, 333, 118
            c.extend([rect(cx, cy, cw, ch, fill="url(#pv-soft)"), serif(cx + 23, cy + 54, number, 38), text(cx + 146, cy + 39, label, 11, ROSE, letter_spacing=".7"), text(cx + 146, cy + 68, note, 12, MUTED)])
    return svg(w, h, "About Varshith — education, focus, and foundations", c)


PROJECTS = [
    {"file": "swiftshare", "label": "01 / FULL-STACK APPLICATION", "title": "SwiftShare", "mobile_title": ["SwiftShare"], "lines": ["A file-sharing workspace with PassShare,", "a personal drive, and chat interfaces.", "Built around REST APIs and persistent storage."], "mobile_lines": ["A file-sharing workspace with PassShare,", "a personal drive, and chat interfaces.", "REST APIs connect the interface", "to persistent storage."], "stack": "REACT · JAVA · SPRING BOOT · MYSQL", "features": ["PassShare", "Shared drive", "Live chat"], "icon": "files"},
    {"file": "taskpilot", "label": "02 / AGENTIC AI · INFLOW AI", "title": "TaskPilot", "mobile_title": ["TaskPilot"], "lines": ["A document assistant that chooses the right tool:", "retrieve, summarize, or search the web.", "Source references keep responses grounded."], "mobile_lines": ["An AI assistant for uploaded documents.", "A LangGraph agent chooses retrieval,", "summarization, or web search,", "with source references in the chat."], "stack": "REACT · FASTAPI · LANGGRAPH · FAISS", "features": ["Retrieve", "Summarize", "Search"], "icon": "agent"},
    {"file": "medical-ai", "label": "03 / BRAIN TUMOR PROJECT · ACADEMIC DEMO", "title": "AI Medical Assistant", "mobile_title": ["AI Medical", "Assistant"], "lines": ["Image classification with ResNet-50 and Grad-CAM.", "Upload an image, explore the visual explanation,", "and export a report with local scan history."], "mobile_lines": ["Image classification with ResNet-50", "and Grad-CAM visual explanations.", "Includes local scan history, a dashboard,", "PDF reports, and a rule-based chatbot."], "stack": "REACT · FASTAPI · PYTORCH · SQLITE", "features": ["ResNet-50", "Grad-CAM", "PDF reports"], "icon": "scan", "note": "Current source: synthetic Normal / Pneumonia / Tumor demo."},
    {"file": "flight-intelligence", "label": "04 / PYTHON · DATA ANALYTICS", "title": "Flight Delay Intelligence", "mobile_title": ["Flight Delay", "Intelligence"], "lines": ["Turn flight CSVs into useful operations insight:", "delay metrics, route-risk tables, and rankings.", "A reusable CLI with charts and automated tests."], "mobile_lines": ["Turn flight CSV files into delay metrics,", "airport and carrier rankings,", "route-risk tables, and charts.", "A reusable CLI with automated tests."], "stack": "PYTHON · PANDAS · MATPLOTLIB · CLI", "features": ["CSV input", "Risk tables", "CLI + charts"], "icon": "chart"},
]


def illustration(kind, x, y, scale=1):
    c = [f'<g transform="translate({x} {y}) scale({scale})" opacity=".85">']
    if kind == "files":
        c.extend([rect(28, 12, 104, 130, fill="#391528", radius=10), rect(62, 42, 104, 130, fill="#481A32", radius=10), path("M87 82h52M87 103h38M87 124h45", width=2), path("M13 122H-13m0 0 12-12m-12 12 12 12M185 60h27m0 0-12-12m12 12-12 12", width=2)])
    elif kind == "agent":
        for cx, cy in [(86, 40), (18, 136), (155, 136)]:
            c.append(f'<circle cx="{cx}" cy="{cy}" r="29" fill="#421A30" stroke="#C77B9B"/>')
        c.extend([path("M69 64 35 111M103 64l35 47M49 136h75"), text(86, 49, "AI", 20, ROSE, text_anchor="middle"), path("M7 132h22M7 141h15M145 136h20M155 126v20")])
    elif kind == "scan":
        c.extend([rect(6, 5, 174, 161, fill="#2B1424", radius=12), path("M25 45V25h23M138 25h23v20M25 127v20h23M138 147h23v-20", width=2)])
        for cx, cy, rx, ry in [(90, 85, 49, 54), (90, 85, 31, 39), (90, 85, 14, 24)]:
            c.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#C77B9B" stroke-opacity=".6"/>')
        c.append('<circle class="pulse" cx="111" cy="73" r="14" fill="#D982AB" opacity=".6"/>')
    else:
        c.extend([path("M0 155H192M0 155V8", color="#703C58", width=1), path("M13 135 42 111 70 125 101 70 132 89 173 28", width=3)])
        for cx, cy in [(13, 135), (42, 111), (70, 125), (101, 70), (132, 89), (173, 28)]:
            c.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="#E5B5C7"/>')
    c.append('</g>')
    return ''.join(c)


def project(data, mobile=False):
    w, h = (600, 700 if len(data["mobile_title"]) == 2 else 640) if mobile else (1200, 360)
    c = [rect(1, 1, w - 2, h - 2, fill="url(#pv-soft)", radius=17), eyebrow(30 if mobile else 38, 40, data["label"], 11 if mobile else 13)]
    if mobile:
        for i, line in enumerate(data["mobile_title"]):
            c.append(serif(28, 101 + i * 53, line, 46))
        shift = 55 if len(data["mobile_title"]) == 2 else 0
        for i, line in enumerate(data["mobile_lines"]):
            c.append(text(30, 162 + shift + i * 31, line, 22, MUTED))
        c.append(illustration(data["icon"], 371, 330 + shift, .78))
        for i, feature in enumerate(data["features"]):
            cy = 321 + shift + i * 54
            c.extend([rect(30, cy, 275, 42, fill="#38172B", radius=8), text(47, cy + 28, feature, 18, ROSE)])
        c.append(path(f"M30 {h-112}H570", color=LINE, width=1))
        c.append(text(30, h - 74, data["stack"], 13, ROSE, letter_spacing=".4"))
        c.append(text(30, h - 31, data.get("note", "EXPLORE THE REPOSITORY →"), 13 if data.get("note") else 14, MUTED))
    else:
        c.append(serif(36, 105, data["title"], 46))
        for i, line in enumerate(data["lines"]):
            c.append(text(39, 152 + i * 29, line, 21, MUTED))
        c.append(illustration(data["icon"], 946, 72))
        for i, feature in enumerate(data["features"]):
            fx = 38 + i * 264
            c.extend([rect(fx, 242, 248, 48, fill="#39182C", radius=8), text(fx + 17, 273, feature, 18, ROSE)])
        c.extend([text(39, 328, data["stack"], 14, ROSE, letter_spacing=".8"), text(1161, 328, "EXPLORE →", 14, ROSE, text_anchor="end")])
        if data.get("note"):
            c.append(text(905, 295, "SYNTHETIC DATA DEMO", 11, MUTED, letter_spacing="1"))
    c.append(f'<path class="motion" d="M18 {h-1}H{w-18}" stroke="#B96C90" stroke-dasharray="45 {w}" opacity=".6"><animate attributeName="stroke-dashoffset" from="{w}" to="{-w}" dur="21s" repeatCount="indefinite"/></path>')
    return svg(w, h, data["title"], c, ' '.join(data["lines"]) + ' ' + data["stack"] + '. ' + data.get("note", ""))


def toolkit(mobile=False):
    w, h = (600, 1060) if mobile else (1200, 690)
    c = [eyebrow(28 if mobile else 40, 37, "03 / TOOLKIT"), serif(28 if mobile else 40, 96, "The tools I reach for.", 38 if mobile else 46)]
    cards = [
        ("LANGUAGES", "The foundations", ["Python · Java · SQL", "JavaScript · TypeScript"]),
        ("INTERFACES", "The experience", ["React · HTML + CSS", "Vite · Responsive UI"]),
        ("BACKEND & APIs", "The engine", ["Spring Boot · FastAPI · Flask", "REST APIs · WebSockets"]),
        ("APPLIED AI", "The intelligence", ["PyTorch · RAG · LangChain", "LangGraph · FAISS · Grad-CAM"]),
        ("DATA", "The memory", ["MySQL · SQLite", "pandas · Data analysis"]),
        ("DEVELOPMENT", "The workflow", ["Git · GitHub · Docker Compose", "Postman · VS Code · PyCharm"]),
    ]
    for i, (label, title, lines) in enumerate(cards):
        if mobile:
            x, y, cw, ch = 28 + (i % 2) * 280, 135 + (i // 2) * 272, 264, 248
        else:
            x, y, cw, ch = 40 + (i % 3) * 380, 138 + (i // 3) * 246, 360, 225
        c.extend([rect(x, y, cw, ch, fill="url(#pv-soft)"), eyebrow(x + 20, y + 38, label, 10 if mobile else 12), serif(x + 20, y + 89, title, 25 if mobile else 29), path(f"M{x+20} {y+112}H{x+cw-20}", color=LINE, width=1)])
        if mobile:
            expanded = {0:["Python · Java · SQL", "JavaScript", "TypeScript"],1:["React · HTML + CSS", "Vite", "Responsive UI"],2:["Spring Boot · FastAPI", "Flask · REST APIs", "WebSockets"],3:["PyTorch · RAG", "LangChain · LangGraph", "FAISS · Grad-CAM"],4:["MySQL · SQLite", "pandas", "Data analysis"],5:["Git · GitHub · Docker", "Postman · VS Code", "PyCharm"]}[i]
            for j, line in enumerate(expanded):
                c.append(text(x + 20, y + 151 + j * 30, line, 16.5, MUTED))
        else:
            for j, line in enumerate(lines):
                c.append(text(x + 20, y + 155 + j * 31, line, 18, MUTED))
    c.append(text(28 if mobile else 40, h - 35, "CORE CONCEPTS / DSA · OOP · DBMS · OPERATING SYSTEMS", 14 if mobile else 16, ROSE, letter_spacing=".6"))
    return svg(w, h, "Technical toolkit", c)


def credentials(mobile=False):
    w, h = (600, 1450) if mobile else (1200, 960)
    c = [eyebrow(28 if mobile else 40, 37, "05 / CREDENTIALS"), serif(28 if mobile else 40, 96, "Learning, made tangible.", 34 if mobile else 46)]
    values = [
        (["Microsoft Certified:", "Azure AI Engineer Associate"], "MICROSOFT", "AI-102 · Azure AI engineering"),
        (["Salesforce Certified", "AI Associate"], "SALESFORCE", "Artificial intelligence fundamentals"),
        (["Certified Implementation Specialist", "Data Foundations", "(CMDB & CSDM)"], "SERVICENOW", "Enterprise data foundations"),
        (["MongoDB", "Associate Developer"], "MONGODB", "Document database development"),
        (["Cambridge English", "Linguaskill"], "CAMBRIDGE ENGLISH", "English language proficiency"),
    ]
    for i, (title, issuer, detail) in enumerate(values):
        x, y, cw, ch = (28, 136 + i * 260, 544, 240) if mobile else (40 + (i % 2) * 570, 143 + (i // 2) * 266, 550, 240)
        c.extend([rect(x, y, cw, ch, fill="url(#pv-soft)"), eyebrow(x + 24, y + 33, f"0{i+1} / CERTIFICATION", 11)])
        for j, line in enumerate(title):
            c.append(serif(x + 24, y + 80 + j * 34, line, 26 if i == 2 else 29))
        c.extend([text(x + 24, y + 187, issuer, 11, ROSE, letter_spacing="1.3"), text(x + 24, y + 218, detail, 17, MUTED)])
        c.append(path(f"M{x+cw-62} {y+36}l9 9 18-22", width=2))
    if not mobile:
        c.extend([eyebrow(639, 727, "05 / CONTINUOUS LEARNING", 12), serif(637, 784, "Five credentials.", 37), text(640, 826, "Cloud AI, enterprise data, databases,", 19, MUTED), text(640, 857, "and clear communication.", 19, MUTED)])
    return svg(w, h, "Five certifications — Microsoft, Salesforce, ServiceNow, MongoDB, and Cambridge English", c)


def recruiter(mobile=False):
    w, h = (600, 445) if mobile else (1200, 300)
    c = [rect(1, 1, w-2, h-2, fill="url(#pv-soft)", radius=16), eyebrow(30 if mobile else 40, 40, "QUICK SCAN / RECRUITER CODE TOURS", 12), serif(28 if mobile else 38, 100, "Choose a role. Follow the code.", 33 if mobile else 49)]
    lanes = [("01", "Full-stack & APIs", "SwiftShare / React + Spring Boot"), ("02", "Applied AI", "TaskPilot / LangGraph + RAG"), ("03", "Python & data", "Flight analytics / CLI + tests")]
    for i, (number, title, detail) in enumerate(lanes):
        x, y, cw, ch = (28, 132+i*88, 544, 73) if mobile else (40+i*378, 144, 364, 113)
        c.append(rect(x,y,cw,ch,fill="#25121F",radius=10))
        c.append(text(x+16,y+30,number,13,ROSE,family="monospace"))
        c.append(text(x+52,y+31,title,22 if mobile else 23,INK))
        c.append(text(x+52 if mobile else x+17,y+57 if mobile else y+76,detail,15, MUTED))
    c.append(text(30 if mobile else 40,h-24,"EXPAND A TRACK BELOW TO INSPECT THE SOURCE ↓",12,ROSE,letter_spacing="1"))
    return svg(w,h,"Recruiter quick scan — choose a full-stack, applied AI, or Python and data code tour",c)


def footer(mobile=False):
    w, h = (600, 236) if mobile else (1200, 215)
    c = [rect(1, 1, w - 2, h - 2, fill="url(#pv-wine)", radius=15), eyebrow(30 if mobile else 40, 43, "NEXT / LET'S BUILD SOMETHING USEFUL")]
    c.append(serif(28 if mobile else 38, 105, "Code. Learn. Repeat.", 38 if mobile else 53))
    c.append(text(30 if mobile else 40, 153, "Open to software engineering opportunities.", 19 if mobile else 22, ROSE))
    c.append(text(30 if mobile else 1160, 198 if mobile else 153, "CONNECT ON LINKEDIN →", 14, ROSE, text_anchor="start" if mobile else "end", letter_spacing="1.2"))
    return svg(w, h, "Connect with Varshith on LinkedIn", c)


def main():
    ASSETS.mkdir(exist_ok=True)
    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        write(f"hero{suffix}.svg", hero(mobile))
        write(f"about{suffix}.svg", about(mobile))
        write(f"recruiter{suffix}.svg", recruiter(mobile))
        write(f"work-heading{suffix}.svg", section_title("02 / SELECTED WORK", "Built to be useful.", mobile=mobile))
        for item in PROJECTS:
            write(f"project-{item['file']}{suffix}.svg", project(item, mobile))
        write(f"toolkit{suffix}.svg", toolkit(mobile))
        write(f"credentials{suffix}.svg", credentials(mobile))
        write(f"footer{suffix}.svg", footer(mobile))
    print("Built 22 desktop/mobile visual panels.")


if __name__ == "__main__":
    main()
