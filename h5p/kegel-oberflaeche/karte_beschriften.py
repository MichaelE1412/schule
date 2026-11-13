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
    "Start": ("#3b3b3b", "#ffffff", "Start und Ziel"),
    "D": ("#7b5ea7", "#ffffff", "D = Vorwissen prüfen"),
    "E": ("#138d90", "#ffffff", "E, V, W = Einstieg, Video, Wissen"),
    "P": ("#f2c200", "#3a2a00", "P = Basisaufgaben (Pflicht)"),
    "B": ("#1f6fb2", "#ffffff", "B = weiterführende Aufgaben"),
    "S": ("#2e8b57", "#ffffff", "S = Profi-Aufgaben zur Wahl"),
    "H": ("#e07b24", "#ffffff", "H, T, F = Hilfe-Abzweig – nur wenn dich eine Rückmeldung hinschickt"),
}


def kategorie(code):
    if code in ("Start", "Ziel"):
        return "Start"
    if code[0] in "TF":
        return "H"
    if code[0] in "EVW":
        return "E"
    return code[0]


# Lage des Schildes relativ zum Punkt (dx, dy) in Pixeln; Standard: unter dem Punkt
UNTEN, OBEN = (0, 58), (0, -58)
LAGE = {
    "H1": OBEN, "H2": OBEN,
    "P2": (-78, 0), "T": (0, 58), "P3": (0, 58), "P4": (0, 58), "P5": (0, 58),
    "F": (-62, 0),
    "B4": (78, 0), "B5": (-74, 0),
    "S1": (70, -26), "S2": (70, -26), "S3": (70, 26), "S4": (70, 26),
    "Ziel": (0, -58),
}


def schild(s):
    fill, ink, _ = KAT[kategorie(s["code"])]
    dx, dy = LAGE.get(s["code"], UNTEN)
    x, y = s["cx"] + dx, s["cy"] + dy
    w = 26 + 22 * len(s["code"])
    return (f'<g><rect x="{x - w / 2:.1f}" y="{y - 21:.1f}" width="{w}" height="42" rx="21" '
            f'fill="{fill}" stroke="#ffffff" stroke-width="3"/>'
            f'<text x="{x:.1f}" y="{y + 10:.1f}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
            f'font-size="28" font-weight="bold" fill="{ink}">{s["code"]}</text></g>')


hintergrund = open(os.path.join(BILDER, "karte.svg"), encoding="utf-8").read()
innen = re.search(r"<svg[^>]*>(.*)</svg>", hintergrund, re.S).group(1)
schilder = "\n".join(schild(s) for s in stages)

with open(os.path.join(BILDER, "karte-beschriftet.svg"), "w", encoding="utf-8") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{innen}\n{schilder}\n</svg>\n')

wege = []
for i, s in enumerate(stages):
    for j in s["nb"]:
        if i < j:
            t = stages[j]
            wege.append(f'<line x1="{s["cx"]}" y1="{s["cy"]}" x2="{t["cx"]}" y2="{t["cy"]}" '
                        f'stroke="#2d2a22" stroke-width="7" stroke-linecap="round" stroke-dasharray="0.1 16"/>')
punkte = []
for s in stages:
    fill = KAT[kategorie(s["code"])][0]
    punkte.append(f'<circle cx="{s["cx"]}" cy="{s["cy"]}" r="30" fill="{fill}" stroke="#ffffff" stroke-width="4"/>')
    if s["finish"]:
        punkte.append(f'<text x="{s["cx"]}" y="{s["cy"] + 11}" text-anchor="middle" font-size="30">🏁</text>')

LH = 330
legende = [f'<rect x="0" y="{H}" width="{W}" height="{LH}" fill="#fffbea"/>',
           f'<line x1="0" y1="{H}" x2="{W}" y2="{H}" stroke="#5a7a2a" stroke-width="4"/>',
           f'<text x="40" y="{H + 48}" font-family="Arial,Helvetica,sans-serif" font-size="30" font-weight="bold" '
           f'fill="#3d5a12">So findest du dich zurecht</text>']
for k, key in enumerate(["Start", "D", "E", "P", "B", "S", "H"]):
    fill, _, txt = KAT[key]
    col, row = (0, k) if k < 4 else (1, k - 4)
    x, y = 40 + col * 600, H + 95 + row * 48
    legende.append(f'<circle cx="{x + 16}" cy="{y - 9}" r="16" fill="{fill}" stroke="#fff" stroke-width="3"/>')
    legende.append(f'<text x="{x + 44}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="24" '
                   f'fill="#2c3a10">{txt}</text>')
legende.append(f'<text x="40" y="{H + LH - 26}" font-family="Arial,Helvetica,sans-serif" font-size="22" '
               f'fill="#3d5a12">Weg: Start → D1 → D2 → E → V → W → P1 → P2 → P3 → P4 → P5 → B1 → B2 → B3 → B4 → B5 → '
               f'eine oder mehrere S-Aufgaben → Ziel</text>')

with open(os.path.join(BILDER, "karte-orientierung.svg"), "w", encoding="utf-8") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H + LH}" viewBox="0 0 {W} {H + LH}">'
            f'{innen}\n' + "\n".join(wege) + "\n" + "\n".join(punkte) + f"\n{schilder}\n" +
            "\n".join(legende) + "\n</svg>\n")
print("geschrieben: karte-beschriftet.svg, karte-orientierung.svg")
