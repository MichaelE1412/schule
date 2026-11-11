#!/usr/bin/env python3
"""Erzeugt beschriftete Kartenbilder aus den Etappen der fertigen H5P-Datei.

Aufruf:  python3 karte_beschriften.py volumen-pyramide-gamemap.h5p

Ergebnis (in bilder/):
  karte-beschriftet.svg       Hintergrund mit Etappen-Kürzeln (wird in der H5P verwendet)
  karte-orientierung.svg      Orientierungskarte mit Wegen, Punkten, Kürzeln und Legende
Die SVGs werden anschließend mit render.js (Playwright) zu JPG/PNG gerendert.
"""
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
BILDER = os.path.join(HERE, "bilder")
W, H = 1600, 1000

with zipfile.ZipFile(sys.argv[1]) as z:
    content = json.loads(z.read("content/content.json"))
elements = content["gamemapSteps"]["gamemap"]["elements"]

# Kategorie -> (Füllfarbe, Textfarbe, Legendentext)
KAT = {
    "Start": ("#3b3b3b", "#ffffff", "Start und Ziel"),
    "D": ("#7b5ea7", "#ffffff", "D = Diagnose"),
    "H": ("#e07b24", "#ffffff", "H, T, F = Abzweig – nur wenn dich eine Rückmeldung hinschickt"),
    "P": ("#f2c200", "#3a2a00", "P = Pflicht (gelb)"),
    "B": ("#1f6fb2", "#ffffff", "B = Stufe 2 (blau)"),
    "S": ("#2e8b57", "#ffffff", "S = Wahlaufgabe (Stufe 3)"),
}


def kategorie(code):
    if code in ("Start", "Ziel"):
        return "Start"
    if code[0] in "TF":
        return "H"
    return code[0]


# Lage des Schildes relativ zum Punkt: (dx, dy) in Pixeln, so gewählt, dass keine Wege verdeckt werden
LAGE = {
    "Start": (0, 58), "D0": (0, 58), "D1": (0, 58), "D2": (0, 58), "D3": (0, 58), "P1": (0, 58),
    "H1": (0, -58), "H2": (0, -58), "H3": (0, -58),
    "P2": (78, 0), "T": (-70, 0), "P3": (78, 0), "F": (0, -58),
    "B1": (0, 58), "B2": (0, 58), "B3": (0, 58),
    "S1": (0, 58), "S2": (-50, 52), "S3": (74, 0), "S4": (74, 0), "Ziel": (-88, 0),
}

stages = []
for el in elements:
    code = el["label"].split()[0]
    t = el["telemetry"]
    cx = (float(t["x"]) + float(t["width"]) / 2) / 100 * W
    cy = (float(t["y"]) + float(t["height"]) / 2) / 100 * H
    stages.append(dict(code=code, cx=cx, cy=cy, nb=[int(n) for n in el["neighbors"]],
                       finish=el.get("specialStageType") == "finish"))


def schild(s):
    fill, ink, _ = KAT[kategorie(s["code"])]
    dx, dy = LAGE.get(s["code"], (0, 58))
    x, y = s["cx"] + dx, s["cy"] + dy
    w = 26 + 22 * len(s["code"])
    return (f'<g><rect x="{x - w / 2:.1f}" y="{y - 21:.1f}" width="{w}" height="42" rx="21" '
            f'fill="{fill}" stroke="#ffffff" stroke-width="3"/>'
            f'<text x="{x:.1f}" y="{y + 10:.1f}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
            f'font-size="28" font-weight="bold" fill="{ink}">{s["code"]}</text></g>')


hintergrund = open(os.path.join(BILDER, "karte.svg"), encoding="utf-8").read()
innen = re.search(r"<svg[^>]*>(.*)</svg>", hintergrund, re.S).group(1)
schilder = "\n".join(schild(s) for s in stages)

# 1) Hintergrund für die H5P: nur Schilder ergänzen (Punkte und Wege zeichnet Game Map selbst)
with open(os.path.join(BILDER, "karte-beschriftet.svg"), "w", encoding="utf-8") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{innen}\n{schilder}\n</svg>\n')

# 2) Orientierungskarte: Wege, Punkte, Schilder und Legende
wege = []
for i, s in enumerate(stages):
    for j in s["nb"]:
        if i < j:
            t = stages[j]
            wege.append(f'<line x1="{s["cx"]:.1f}" y1="{s["cy"]:.1f}" x2="{t["cx"]:.1f}" y2="{t["cy"]:.1f}" '
                        f'stroke="#3a2f22" stroke-width="7" stroke-linecap="round" stroke-dasharray="0.1 16"/>')
punkte = []
for s in stages:
    fill = KAT[kategorie(s["code"])][0]
    punkte.append(f'<circle cx="{s["cx"]:.1f}" cy="{s["cy"]:.1f}" r="30" fill="{fill}" fill-opacity="1" '
                  f'stroke="#ffffff" stroke-width="4"/>')
    if s["finish"]:
        punkte.append(f'<text x="{s["cx"]:.1f}" y="{s["cy"] + 11:.1f}" text-anchor="middle" font-size="30">🏁</text>')

LH = 280
legende = [f'<rect x="0" y="{H}" width="{W}" height="{LH}" fill="#fbf0d4"/>',
           f'<line x1="0" y1="{H}" x2="{W}" y2="{H}" stroke="#8a6230" stroke-width="4"/>',
           f'<text x="40" y="{H + 48}" font-family="Arial,Helvetica,sans-serif" font-size="30" font-weight="bold" '
           f'fill="#5a3d1a">So findest du dich zurecht</text>']
eintraege = ["Start", "D", "P", "B", "S", "H"]
for k, key in enumerate(eintraege):
    fill, _, txt = KAT[key]
    col, row = (0, k) if k < 3 else (1, k - 3)
    x = 40 + col * 560
    y = H + 95 + row * 48
    legende.append(f'<circle cx="{x + 16}" cy="{y - 9}" r="16" fill="{fill}" stroke="#fff" stroke-width="3"/>')
    legende.append(f'<text x="{x + 44}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="24" '
                   f'fill="#3a2a10">{txt}</text>')
legende.append(f'<text x="40" y="{H + LH - 22}" font-family="Arial,Helvetica,sans-serif" font-size="22" '
               f'fill="#5a3d1a">Weg: Start → D0 → D1 → D2 → D3 → P1 → P2 → P3 → B1 → B2 → B3 → eine oder mehrere S-Etappen → Ziel</text>')

with open(os.path.join(BILDER, "karte-orientierung.svg"), "w", encoding="utf-8") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H + LH}" viewBox="0 0 {W} {H + LH}">'
            f'{innen}\n' + "\n".join(wege) + "\n" + "\n".join(punkte) + f"\n{schilder}\n" +
            "\n".join(legende) + "\n</svg>\n")
print("geschrieben: karte-beschriftet.svg, karte-orientierung.svg")
