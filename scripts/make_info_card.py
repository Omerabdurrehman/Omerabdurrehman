#!/usr/bin/env python3

import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")

WIDTH = 490
HEIGHT = 390

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TEXT = "#c9d1d9"
MUTED = "#7d8590"

TITLE = "Windows Terminal"

ROWS = [
    ("Name", "Omer Abdur Rehman"),
    ("Role", "Computer Systems Engineer"),
    ("Focus", "Machine Learning • AI • Data Analytics"),
    ("Location", "Punjab, Pakistan"),
    ("Education", "The Islamia University of Bahawalpur"),
    ("Current", "AI / ML Engineer"),
    ("Languages", "Python • C++ • Dart"),
    ("Frameworks", "Flutter • FastAPI • Django"),
    ("Database", "Firebase • MongoDB • SQL"),
    ("Tools", "Git • VS Code • Android Studio"),
    ("Research", "AI Prediction Models"),
    ("Interests", "Deep Learning • NLP"),
]

parts = []

parts.append(f'''
<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}"
font-family="Consolas, 'Courier New', monospace">

<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="{BG2}"/>
<stop offset="100%" stop-color="{BG}"/>
</linearGradient>
</defs>

<rect width="{WIDTH}" height="{HEIGHT}" rx="12" fill="url(#bg)"/>
<rect x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="12"
fill="none" stroke="{FRAME}"/>

<text
x="20"
y="22"
fill="{MUTED}"
font-size="12">{TITLE}</text>

<text
x="{WIDTH-80}"
y="22"
fill="{MUTED}"
font-size="12">— □ ✕</text>

<line
x1="0"
y1="32"
x2="{WIDTH}"
y2="32"
stroke="{FRAME}"/>
''')

y = 58

delay = 0.0

for key, value in ROWS:

    parts.append(f'''
<g opacity="0">
<animate
attributeName="opacity"
from="0"
to="1"
begin="{delay:.2f}s"
dur="0.35s"
fill="freeze"/>

<animateTransform
attributeName="transform"
type="translate"
from="0 8"
to="0 0"
begin="{delay:.2f}s"
dur="0.35s"
fill="freeze"/>

<text
x="22"
y="{y}"
fill="#58a6ff"
font-size="14">{key:<12}</text>

<text
x="150"
y="{y}"
fill="{TEXT}"
font-size="14">{value}</text>
</g>
''')

    y += 24
    delay += 0.15

parts.append("</svg>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("".join(parts))

print("Generated:", OUT)