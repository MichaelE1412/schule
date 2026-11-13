#!/usr/bin/env python3
"""Erzeugt beschriftete Kartenbilder aus bilder/etappen.json (wird von build.py geschrieben).

Ergebnis (in bilder/):
  karte-beschriftet.svg   Hintergrund mit Etappen-Kürzeln (wird in der H5P verwendet)
  karte-orientierung.svg  Orientierungskarte mit Wegen, Punkten, Kürzeln und Legende
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BILDER = os.path.join(HERE, "bilder")
W, H = 1600, 1000

stages = json.load(open(os.path.join(BILDER, "etappen.json"), encoding="utf-8"))

# Kategorie -> (Füllfarbe, Textfarbe, Legendentext)
KAT = {
    "Start": ("#e9eef5", "#14273d", "Start und Ziel"),
    "D": ("#8e7cc3", "#ffffff", "D – Vorwissen"),
    "M": ("#4ba3c3", "#ffffff", "M – Mathematische Werkzeuge (Trigonometrie, Vektoren)"),
    "E": ("#e9b949", "#14273d", "E – Erarbeitung"),
    "A": ("#e4572e", "#ffffff", "A – Beispielaufgaben 1–3"),
    "H": ("#9aa5b1", "#14273d", "H, T – Hilfe-Abzweig, nur nach Rückmeldung"),
    "X": ("#3fa37a", "#ffffff", "X – Vertiefung (optional)"),
}


def kategorie(code):
    if code in ("Start", "Ziel"):
        return "Start"
    if code[0] in "HT":
        return "H"
    return code[0]


def schild(s):
    fill, ink, _ = KAT[kategorie(s["code"])]
    x, y = s["cx"] + s["ldx"], s["cy"] + s["ldy"]
    w = 24 + 19 * len(s["code"])
    return (f'<g><rect x="{x - w / 2:.1f}" y="{y - 18:.1f}" width="{w}" height="36" rx="5" '
            f'fill="{fill}" stroke="#0b1726" stroke-width="2"/>'
            f'<text x="{x:.1f}" y="{y + 8:.1f}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="23" font-weight="bold" fill="{ink}">{s["code"]}</text></g>')


hintergrund = open(os.path.join(BILDER, "karte.svg"), encoding="utf-8").read()
kopf = re.search(r"<svg[^>]*>", hintergrund).group(0)
innen = re.search(r"<svg[^>]*>(.*)</svg>", hintergrund, re.S).group(1)
schilder = "\n".join(schild(s) for s in stages)

with open(os.path.join(BILDER, "karte-beschriftet.svg"), "w", encoding="utf-8") as f:
    f.write(f'{kopf}{innen}\n{schilder}\n</svg>\n')

wege = []
for i, s in enumerate(stages):
    for j in s["nb"]:
        if i < j:
            t = stages[j]
            wege.append(f'<line x1="{s["cx"]}" y1="{s["cy"]}" x2="{t["cx"]}" y2="{t["cy"]}" '
                        f'stroke="#c8dcf0" stroke-width="6" stroke-linecap="round" stroke-dasharray="0.1 14"/>')
punkte = []
for s in stages:
    fill = KAT[kategorie(s["code"])][0]
    punkte.append(f'<circle cx="{s["cx"]}" cy="{s["cy"]}" r="27" fill="{fill}" stroke="#0b1726" stroke-width="3"/>')
    if s["finish"]:
        punkte.append(f'<text x="{s["cx"]}" y="{s["cy"] + 10}" text-anchor="middle" font-size="26">🏁</text>')

LH = 300
legende = [f'<rect x="0" y="{H}" width="{W}" height="{LH}" fill="#0f1f31"/>',
           f'<line x1="0" y1="{H}" x2="{W}" y2="{H}" stroke="#5d7fa3" stroke-width="3"/>',
           f'<text x="40" y="{H + 48}" font-family="Helvetica,Arial,sans-serif" font-size="28" font-weight="bold" '
           f'fill="#e9eef5">Orientierung</text>']
for k, key in enumerate(["Start", "D", "M", "E", "A", "X", "H"]):
    fill, _, txt = KAT[key]
    col, row = (0, k) if k < 4 else (1, k - 4)
    x, y = 40 + col * 640, H + 95 + row * 44
    legende.append(f'<rect x="{x}" y="{y - 24}" width="30" height="30" rx="5" fill="{fill}"/>')
    legende.append(f'<text x="{x + 44}" y="{y}" font-family="Helvetica,Arial,sans-serif" font-size="22" '
                   f'fill="#dbe6f2">{txt}</text>')
legende.append(f'<text x="40" y="{H + LH - 22}" font-family="Helvetica,Arial,sans-serif" font-size="21" '
               f'fill="#9fb8d3">Weg: Start → D1 → M1 → M2 → E1 → E2 → E3 → E4 → A1 → A2 → A3 → (X1–X3) → Ziel</text>')

with open(os.path.join(BILDER, "karte-orientierung.svg"), "w", encoding="utf-8") as f:
    f.write(kopf.replace(f'height="{H}"', f'height="{H + LH}"').replace(f'0 0 {W} {H}', f'0 0 {W} {H + LH}')
            + f'{innen}\n' + "\n".join(wege) + "\n" + "\n".join(punkte) + f"\n{schilder}\n"
            + "\n".join(legende) + "\n</svg>\n")
print("geschrieben: karte-beschriftet.svg, karte-orientierung.svg")
