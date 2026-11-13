#!/usr/bin/env python3
"""Erzeugt die SVG-Bilder für den Lernpfad „Oberflächeninhalt des Kegels“.

Aufruf: python3 gen_bilder.py   (schreibt nach bilder/)
Danach mit render.js zu PNG/JPG rendern (siehe make.sh).
"""
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bilder")
os.makedirs(OUT, exist_ok=True)
FONT = 'font-family="Arial,Helvetica,sans-serif"'


def svg(name, w, h, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" {FONT}>\n'
                f'<rect width="{w}" height="{h}" fill="#fff"/>\n{body}\n</svg>\n')


def cone(cx, by, R, H, fill, stroke="#333", ry_f=0.28):
    """Kegel mit Spitze oben; by = y der Grundkreismitte."""
    ry = R * ry_f
    ax, ay = cx, by - H
    return (f'<path d="M{cx - R},{by} L{ax},{ay} L{cx + R},{by} A{R},{ry} 0 0 1 {cx - R},{by} Z" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>'
            f'<path d="M{cx - R},{by} A{R},{ry} 0 0 1 {cx + R},{by}" fill="none" stroke="{stroke}" stroke-width="2" stroke-dasharray="7 5"/>'
            f'<circle cx="{cx}" cy="{by}" r="3.5" fill="{stroke}"/>')


def sector(cx, cy, rad, a0, a1, fill, stroke="#333", extra=""):
    """Kreisausschnitt, Winkel in Grad (0 = rechts, gegen den Uhrzeigersinn, SVG-y nach unten)."""
    p = lambda a: (cx + rad * math.cos(math.radians(a)), cy - rad * math.sin(math.radians(a)))
    x0, y0 = p(a0)
    x1, y1 = p(a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{rad},{rad} 0 {large} 0 {x1:.1f},{y1:.1f} Z" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2.5" {extra}/>')


# ------------------------------------------------------------ Kegel und Netz (Wissen)
def kegel_netz():
    b = [cone(170, 380, 95, 260, "#cfe8f7")]
    b.append('<line x1="170" y1="120" x2="170" y2="380" stroke="#2e8b57" stroke-width="3" stroke-dasharray="9 6"/>')
    b.append('<line x1="170" y1="380" x2="265" y2="380" stroke="#c0392b" stroke-width="3.5"/>')
    b.append('<line x1="170" y1="120" x2="265" y2="380" stroke="#1f6fb2" stroke-width="4"/>')
    b.append('<polyline points="170,362 188,362 188,380" fill="none" stroke="#333" stroke-width="2"/>')
    b.append('<text x="146" y="270" font-size="26" fill="#2e8b57" font-weight="bold">h</text>')
    b.append('<text x="205" y="408" font-size="26" fill="#c0392b" font-weight="bold">r</text>')
    b.append('<text x="232" y="240" font-size="26" fill="#1f6fb2" font-weight="bold">s</text>')
    b.append('<text x="60" y="455" font-size="20" fill="#333">Kegel</text>')
    # Netz: r = 3, s = 7,6 -> alpha ≈ 142°
    s_px, r_px = 190, 190 * 3 / 7.6158
    alpha = 360 * 3 / 7.6158
    cx, cy = 560, 50
    a0, a1 = 270 - alpha / 2, 270 + alpha / 2
    b.append(sector(cx, cy, s_px, a0, a1, "#cfe8f7"))
    p = lambda a, rad: (cx + rad * math.cos(math.radians(a)), cy - rad * math.sin(math.radians(a)))
    # Mantelbogen hervorheben
    x0, y0 = p(a0, s_px)
    x1, y1 = p(a1, s_px)
    b.append(f'<path d="M{x0:.1f},{y0:.1f} A{s_px},{s_px} 0 0 0 {x1:.1f},{y1:.1f}" fill="none" stroke="#e0407b" stroke-width="6"/>')
    # Grundkreis tangential unten
    gy = cy + s_px + r_px
    b.append(f'<circle cx="{cx}" cy="{gy:.1f}" r="{r_px:.1f}" fill="#f7d0d6" stroke="#333" stroke-width="2.5"/>')
    b.append(f'<line x1="{cx}" y1="{gy:.1f}" x2="{cx + r_px:.1f}" y2="{gy:.1f}" stroke="#c0392b" stroke-width="3.5"/>')
    b.append(f'<text x="{cx + r_px / 2 - 6:.1f}" y="{gy - 8:.1f}" font-size="24" fill="#c0392b" font-weight="bold">r</text>')
    xs, ys = p(a1, s_px)
    b.append(f'<line x1="{cx}" y1="{cy}" x2="{xs:.1f}" y2="{ys:.1f}" stroke="#1f6fb2" stroke-width="4"/>')
    b.append(f'<text x="{(cx + xs) / 2 + 12:.1f}" y="{(cy + ys) / 2:.1f}" font-size="26" fill="#1f6fb2" font-weight="bold">s</text>')
    b.append(f'<text x="{cx - 14}" y="{cy + 58}" font-size="22" fill="#333">α</text>')
    b.append(f'<path d="M{p(a0, 40)[0]:.1f},{p(a0, 40)[1]:.1f} A40,40 0 0 0 {p(a1, 40)[0]:.1f},{p(a1, 40)[1]:.1f}" fill="none" stroke="#333" stroke-width="2"/>')
    b.append(f'<text x="{cx + 150}" y="{cy + 205}" font-size="21" fill="#e0407b" font-weight="bold">Mantelbogen = 2·π·r</text>')
    b.append(f'<text x="{cx + 200}" y="{cy + 95}" font-size="21" fill="#1f6fb2">Mantelfläche M</text>')
    b.append(f'<text x="{cx + r_px + 14:.1f}" y="{gy + 30:.1f}" font-size="21" fill="#a0303a">Grundfläche G</text>')
    b.append(f'<text x="{cx - 250}" y="455" font-size="20" fill="#333">Netz des Kegels</text>')
    svg("kegel-netz.svg", 960, 480, "\n".join(b))


# ------------------------------------------------------------ Aufgabe 1: drei Kegel
def aufgabe1():
    b = []
    data = [("a)", 140, 70, 230, "#cde7f8", "12 cm", "5,1 cm", "r"),
            ("b)", 430, 80, 170, "#f8d0cd", "10 mm", "8 mm", "d"),
            ("c)", 720, 70, 240, "#dcefc6", "12,2 cm", "11,4 cm", "d")]
    for lab, cx, R, H, fill, s_txt, m_txt, kind in data:
        by = 330
        b.append(cone(cx, by, R, H, fill))
        b.append(f'<text x="{cx - 120}" y="60" font-size="24" fill="#333" font-weight="bold">{lab}</text>')
        # Mantellinie links bemaßen
        ax, ay = cx, by - H
        dx, dy = -(H), -R  # Normale nach links außen (unnormiert)
        n = math.hypot(dx, dy)
        ox, oy = dx / n * 22, dy / n * 22
        b.append(f'<line x1="{cx - R + ox:.1f}" y1="{by + oy:.1f}" x2="{ax + ox:.1f}" y2="{ay + oy:.1f}" stroke="#333" stroke-width="1.6" marker-start="url(#pf)" marker-end="url(#pf)"/>')
        ang = math.degrees(math.atan2(ay - by, ax - (cx - R)))
        mx, my = (cx - R + ax) / 2 + ox * 1.9, (by + ay) / 2 + oy * 1.9
        b.append(f'<text x="{mx:.1f}" y="{my:.1f}" font-size="21" fill="#333" text-anchor="middle" transform="rotate({ang:.1f} {mx:.1f} {my:.1f})">{s_txt}</text>')
        if kind == "r":
            b.append(f'<line x1="{cx}" y1="{by}" x2="{cx + R}" y2="{by}" stroke="#c0392b" stroke-width="2.5"/>')
            b.append(f'<line x1="{cx}" y1="{by + 38}" x2="{cx + R}" y2="{by + 38}" stroke="#333" stroke-width="1.6" marker-start="url(#pf)" marker-end="url(#pf)"/>')
            b.append(f'<text x="{cx + R / 2}" y="{by + 64}" font-size="21" text-anchor="middle" fill="#333">{m_txt}</text>')
        else:
            b.append(f'<line x1="{cx - R}" y1="{by + 38}" x2="{cx + R}" y2="{by + 38}" stroke="#333" stroke-width="1.6" marker-start="url(#pf)" marker-end="url(#pf)"/>')
            b.append(f'<text x="{cx}" y="{by + 64}" font-size="21" text-anchor="middle" fill="#333">{m_txt}</text>')
    defs = ('<defs><marker id="pf" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>')
    svg("aufgabe1-kegel.svg", 860, 420, defs + "\n".join(b))


# ------------------------------------------------------------ Aufgabe 10: Netze prüfen
def aufgabe10():
    b = []
    k = 32  # Pixel pro cm (1 Kästchen = 0,5 cm)
    nets = [("a)", 90, 90, 0, 90, 1), ("b)", 410, 90, 0, 180, 1), ("c)", 730, 90, 0, 180, 2)]
    for lab, ox, oy, a0, a1, r in nets:
        w, h = 280, 330
        for i in range(0, w + 1, k // 2):
            b.append(f'<line x1="{ox + i}" y1="{oy}" x2="{ox + i}" y2="{oy + h}" stroke="#d6d6d6" stroke-width="1"/>')
        for j in range(0, h + 1, k // 2):
            b.append(f'<line x1="{ox}" y1="{oy + j}" x2="{ox + w}" y2="{oy + j}" stroke="#d6d6d6" stroke-width="1"/>')
        b.append(f'<text x="{ox - 6}" y="{oy - 20}" font-size="24" font-weight="bold" fill="#333">{lab}</text>')
        s = 4
        if a1 == 90:   # Viertelkreis, Mittelpunkt unten links
            cx, cy = ox + 16, oy + 16 + s * k
            b.append(sector(cx, cy, s * k, 0, 90, "#cfe8f7"))
            ccx, ccy = cx + s * k + r * k, cy - r * k - 8
        else:          # Halbkreis, Mittelpunkt links in der Mitte, Bogen nach rechts
            cx, cy = ox + 16, oy + 16 + s * k
            b.append(sector(cx, cy, s * k, -90, 90, "#cfe8f7"))
            ccx, ccy = cx + s * k + r * k, cy
        b.append(f'<circle cx="{ccx}" cy="{ccy}" r="{r * k}" fill="none" stroke="#333" stroke-width="2.5"/>')
        b.append(f'<line x1="{ccx}" y1="{ccy}" x2="{ccx}" y2="{ccy - r * k}" stroke="#c0392b" stroke-width="2.5"/>')
        b.append(f'<text x="{ccx + 6}" y="{ccy - r * k / 2 + 6}" font-size="18" fill="#c0392b">r = {r} cm</text>')
        b.append(f'<text x="{cx + 4}" y="{cy + (24 if a1 == 90 else -s * k / 2)}" font-size="18" fill="#1f6fb2">s = 4 cm</text>')
    b.append('<text x="90" y="470" font-size="18" fill="#555">1 Kästchen = 0,5 cm</text>')
    svg("aufgabe10-netze.svg", 1060, 490, "\n".join(b))


# ------------------------------------------------------------ Aufgabe 15: Lampenschirm
def aufgabe15():
    b = []
    cx, cy = 70, 230
    k = 4.6  # Pixel pro cm
    R_in, R_out = 70 * k, 140 * k
    ang = math.degrees(100 / 140) / 2  # halber Mittelpunktswinkel
    p = lambda a, rad: (cx + rad * math.cos(math.radians(a)), cy - rad * math.sin(math.radians(a)))
    xi0, yi0 = p(ang, R_in)
    xi1, yi1 = p(-ang, R_in)
    xo0, yo0 = p(ang, R_out)
    xo1, yo1 = p(-ang, R_out)
    b.append(f'<path d="M{xi0:.1f},{yi0:.1f} L{xo0:.1f},{yo0:.1f} A{R_out},{R_out} 0 0 1 {xo1:.1f},{yo1:.1f} '
             f'L{xi1:.1f},{yi1:.1f} A{R_in},{R_in} 0 0 0 {xi0:.1f},{yi0:.1f} Z" fill="#cfe8f7" stroke="#333" stroke-width="2.5"/>')
    b.append(f'<path d="M{xi0:.1f},{yi0:.1f} L{cx},{cy} L{xi1:.1f},{yi1:.1f}" fill="none" stroke="#333" stroke-width="2" stroke-dasharray="7 6"/>')
    b.append(f'<path d="M{xo0:.1f},{yo0:.1f} A{R_out},{R_out} 0 0 1 {xo1:.1f},{yo1:.1f}" fill="none" stroke="#2e8b57" stroke-width="5"/>')
    b.append(f'<path d="M{xi0:.1f},{yi0:.1f} A{R_in},{R_in} 0 0 1 {xi1:.1f},{yi1:.1f}" fill="none" stroke="#c0392b" stroke-width="5"/>')
    b.append(f'<text x="{(cx + xi0) / 2 - 8:.1f}" y="{(cy + yi0) / 2 - 12:.1f}" font-size="24" fill="#333">x</text>')
    b.append(f'<text x="{(xi0 + xo0) / 2 - 10:.1f}" y="{(yi0 + yo0) / 2 - 14:.1f}" font-size="24" fill="#333">70</text>')
    b.append(f'<text x="{xi0 - 50:.1f}" y="{cy + 8}" font-size="24" fill="#c0392b">50</text>')
    b.append(f'<text x="{cx + R_out + 12:.1f}" y="{cy + 8}" font-size="24" fill="#2e8b57">100</text>')
    b.append('<text x="20" y="440" font-size="18" fill="#555">Angaben in cm · roter Bogen 50 cm · grüner Bogen 100 cm</text>')
    svg("aufgabe15-lampenschirm.svg", 800, 460, "\n".join(b))


# ------------------------------------------------------------ Einstieg: Hut und Schnittmuster
def hut():
    b = [cone(150, 360, 85, 280, "#f2b6b0")]
    b.append('<path d="M65,360 A85,24 0 0 0 235,360" fill="none" stroke="#7a3b35" stroke-width="5"/>')
    b.append('<text x="60" y="425" font-size="20" fill="#333">Hut aus Filz</text>')
    b.append('<text x="40" y="452" font-size="18" fill="#7a3b35">Kopfumfang 55 cm</text>')
    cx, cy, s = 520, 70, 300
    alpha = 110
    b.append(sector(cx, cy, s, 270 - alpha / 2, 270 + alpha / 2, "#f2b6b0", extra='stroke-dasharray="0"'))
    p = lambda a, rad: (cx + rad * math.cos(math.radians(a)), cy - rad * math.sin(math.radians(a)))
    x0, y0 = p(270 - alpha / 2, s)
    x1, y1 = p(270 + alpha / 2, s)
    b.append(f'<path d="M{x0:.1f},{y0:.1f} A{s},{s} 0 0 0 {x1:.1f},{y1:.1f}" fill="none" stroke="#7a3b35" stroke-width="6"/>')
    b.append(f'<text x="{cx - 20}" y="{cy + s + 40}" font-size="34" fill="#7a3b35" font-weight="bold">?</text>')
    b.append(f'<text x="{cx - 120}" y="452" font-size="20" fill="#333">Schnittmuster (Mantel)</text>')
    svg("hut.svg", 820, 470, "\n".join(b))


# ------------------------------------------------------------ Karte (Hintergrund)
def karte():
    b = ['<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe6fa"/>'
         '<stop offset="1" stop-color="#e9f6ff"/></linearGradient>'
         '<linearGradient id="gras" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe3a0"/>'
         '<stop offset="1" stop-color="#9fd27f"/></linearGradient></defs>',
         '<rect width="1600" height="1000" fill="url(#gras)"/>']
    # Wege-Hügel / Wiesenmuster
    for y in (300, 560, 790):
        b.append(f'<path d="M0 {y} Q400 {y - 40} 800 {y} T1600 {y}" fill="none" stroke="#8cc46c" stroke-width="3" opacity="0.6"/>')
    for (x, y) in [(470, 600), (1180, 330), (60, 980), (980, 990), (700, 330), (1560, 590)]:
        b.append(f'<g fill="#7dbb5c" opacity="0.8"><ellipse cx="{x}" cy="{y}" rx="18" ry="6"/><ellipse cx="{x + 22}" cy="{y + 4}" rx="12" ry="4"/></g>')
    # Zirkuszelt oben rechts (Kegeldach)
    tx, ty = 1470, 250
    b.append(f'<rect x="{tx - 95}" y="{ty}" width="190" height="95" fill="#fff4e0" stroke="#7a4b20" stroke-width="3"/>')
    for i in range(5):
        b.append(f'<rect x="{tx - 95 + i * 38}" y="{ty}" width="19" height="95" fill="#e74c3c" opacity="0.85"/>')
    b.append(f'<path d="M{tx - 50},{ty + 95} Q{tx},{ty + 40} {tx + 50},{ty + 95} Z" fill="#7a4b20"/>')
    b.append(f'<polygon points="{tx},{ty - 190} {tx - 115},{ty + 4} {tx + 115},{ty + 4}" fill="#e74c3c" stroke="#7a4b20" stroke-width="3"/>')
    for i in (-1, 0, 1):
        b.append(f'<line x1="{tx}" y1="{ty - 190}" x2="{tx + i * 55}" y2="{ty + 4}" stroke="#fff4e0" stroke-width="10" opacity="0.9"/>')
    b.append(f'<line x1="{tx}" y1="{ty - 190}" x2="{tx}" y2="{ty - 225}" stroke="#7a4b20" stroke-width="3"/>')
    b.append(f'<polygon points="{tx},{ty - 225} {tx + 34},{ty - 214} {tx},{ty - 203}" fill="#f1c40f"/>')
    # Nadelbäume (Kegel) links Mitte
    for (x, y, s) in [(70, 690, 1.0), (165, 640, 0.8), (120, 760, 0.7), (1110, 640, 0.6)]:
        b.append(f'<g transform="translate({x},{y}) scale({s})"><rect x="-8" y="0" width="16" height="30" fill="#7a5328"/>'
                 '<polygon points="0,-130 -55,5 55,5" fill="#3f8f3a"/><polygon points="0,-130 0,5 55,5" fill="#2f7a2c"/></g>')
    # Eistüte unten Mitte zwischen den Reihen
    b.append('<g transform="translate(560,640)"><polygon points="-26,0 26,0 0,80" fill="#e0a85a" stroke="#9b6a2a" stroke-width="2"/>'
             '<circle cx="-12" cy="-8" r="20" fill="#f7b6c8"/><circle cx="12" cy="-8" r="20" fill="#fff1c2"/><circle cx="0" cy="-26" r="20" fill="#8b5a3c"/></g>')
    # Partyhüte
    b.append('<g transform="translate(1180,330)"><polygon points="0,-60 -28,10 28,10" fill="#9b59b6"/><circle cx="0" cy="-62" r="8" fill="#f1c40f"/>'
             '<line x1="-18" y1="-14" x2="18" y2="-14" stroke="#fff" stroke-width="4"/></g>')
    # Titel
    b.append('<g transform="translate(965,695)"><rect width="420" height="66" rx="12" fill="#fffbea" stroke="#5a7a2a" stroke-width="3"/>'
             '<text x="210" y="44" text-anchor="middle" font-family="Georgia,serif" font-size="31" fill="#3d5a12">Oberfläche des Kegels</text></g>')
    with open(os.path.join(OUT, "karte.svg"), "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000">\n'
                + "\n".join(b) + "\n</svg>\n")


kegel_netz()
aufgabe1()
aufgabe10()
aufgabe15()
hut()
karte()
print("SVGs geschrieben nach", OUT)
