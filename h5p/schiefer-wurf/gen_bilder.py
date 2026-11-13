#!/usr/bin/env python3
"""Erzeugt die SVG-Grafiken für den Lernpfad „Der schiefe Wurf“ (EF).

Aufruf: python3 gen_bilder.py   (schreibt nach bilder/)
"""
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bilder")
os.makedirs(OUT, exist_ok=True)
FONT = 'font-family="Helvetica,Arial,sans-serif"'
NAVY, BLAU, ROT, GRUEN, ORANGE, GRAU = "#1d3557", "#2f6fa7", "#d62839", "#1f8a70", "#e07a1f", "#8a94a6"
G = 9.81


def svg(name, w, h, body, bg="#ffffff"):
    defs = ('<defs>'
            + "".join(f'<marker id="p{n}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                      f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
                      for n, c in (("n", NAVY), ("b", BLAU), ("r", ROT), ("g", GRUEN), ("o", ORANGE), ("k", "#333")))
            + '</defs>')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" {FONT}>\n'
                f'{defs}<rect width="{w}" height="{h}" fill="{bg}"/>\n{body}\n</svg>\n')


def pfeil(x1, y1, x2, y2, farbe, m, breite=4, extra=""):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{farbe}" stroke-width="{breite}" '
            f'marker-end="url(#p{m})" {extra}/>')


def formel(s, size):
    """Ersetzt v⃗, v_x, v_y, v_0 durch SVG-tspans (Pfeil, Index)."""
    up, dn = 0.32 * size, 0.62 * size
    sub = lambda c: (f'<tspan dy="{up:.1f}" font-size="{0.68 * size:.1f}">{c}</tspan><tspan dy="{-up:.1f}">\u200b</tspan>')
    for tok, c in (("v_x", "x"), ("v_y", "y"), ("vₓ", "x")):
        s = s.replace(tok, "v" + sub(c))
    s = s.replace("v⃗", f'v<tspan dx="{-0.55 * size:.1f}" dy="{-dn:.1f}" font-size="{0.62 * size:.1f}">→</tspan>'
                         f'<tspan dy="{dn:.1f}" dx="{0.04 * size:.1f}">\u200b</tspan>')
    return s


def txt(x, y, s, size=22, farbe="#222", anchor="start", weight="normal", style=""):
    s = formel(s, size)
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{farbe}" text-anchor="{anchor}" '
            f'font-weight="{weight}" {style}>{s}</text>')


class Achsen:
    """Koordinatensystem: Datenbereich -> Pixel."""

    def __init__(self, x0, y0, w, h, xmin, xmax, ymin, ymax):
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax

    def px(self, x, y):
        return (self.x0 + (x - self.xmin) / (self.xmax - self.xmin) * self.w,
                self.y0 + self.h - (y - self.ymin) / (self.ymax - self.ymin) * self.h)

    def raster(self, dx, dy, xlab, ylab, fmt=lambda v: f"{v:g}".replace(".", ",")):
        b = [f'<rect x="{self.x0}" y="{self.y0}" width="{self.w}" height="{self.h}" fill="#f4f7fb"/>']
        v = self.xmin
        while v <= self.xmax + 1e-9:
            x, _ = self.px(v, 0)
            b.append(f'<line x1="{x:.1f}" y1="{self.y0}" x2="{x:.1f}" y2="{self.y0 + self.h}" stroke="#d5dde8" stroke-width="1"/>')
            b.append(txt(x, self.y0 + self.h + 24, fmt(v), 17, "#444", "middle"))
            v += dx
        v = self.ymin
        while v <= self.ymax + 1e-9:
            _, y = self.px(0, v)
            b.append(f'<line x1="{self.x0}" y1="{y:.1f}" x2="{self.x0 + self.w}" y2="{y:.1f}" stroke="#d5dde8" stroke-width="1"/>')
            b.append(txt(self.x0 - 10, y + 6, fmt(v), 17, "#444", "end"))
            v += dy
        ax, ay = self.px(self.xmin, self.ymin)
        b.append(pfeil(ax, ay, self.x0 + self.w + 18, ay, "#333", "k", 2))
        b.append(pfeil(ax, ay, ax, self.y0 - 18, "#333", "k", 2))
        b.append(txt(self.x0 + self.w + 10, ay + 44, xlab, 18, "#333", "end", style='font-style="italic"'))
        b.append(txt(ax + 10, self.y0 - 8, ylab, 18, "#333", style='font-style="italic"'))
        return b

    def kurve(self, f, t0, t1, farbe, breite=3, n=200, extra=""):
        pts = []
        for i in range(n + 1):
            t = t0 + (t1 - t0) * i / n
            x, y = f(t)
            pts.append("%.1f,%.1f" % self.px(x, y))
        return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{farbe}" stroke-width="{breite}" {extra}/>'


# ------------------------------------------------------------ Rechtwinkliges Dreieck (Trigonometrie)
def dreieck():
    A, B, C = (90, 330), (470, 330), (470, 110)
    b = [f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="#eef3f9" stroke="{NAVY}" stroke-width="3"/>',
         f'<polyline points="{B[0] - 26},{B[1]} {B[0] - 26},{B[1] - 26} {B[0]},{B[1] - 26}" fill="none" stroke="{NAVY}" stroke-width="2"/>',
         f'<path d="M{A[0] + 70},{A[1]} A70,70 0 0 0 {A[0] + 70 * math.cos(math.atan2(220, 380)):.1f},{A[1] - 70 * math.sin(math.atan2(220, 380)):.1f}" fill="none" stroke="{ROT}" stroke-width="2.5"/>',
         txt(A[0] + 80, A[1] - 12, "α", 26, ROT, weight="bold"),
         f'<line x1="{A[0]}" y1="{A[1]}" x2="{C[0]}" y2="{C[1]}" stroke="{ROT}" stroke-width="5"/>',
         f'<line x1="{A[0]}" y1="{A[1]}" x2="{B[0]}" y2="{B[1]}" stroke="{BLAU}" stroke-width="5"/>',
         f'<line x1="{B[0]}" y1="{B[1]}" x2="{C[0]}" y2="{C[1]}" stroke="{GRUEN}" stroke-width="5"/>',
         txt(250, 200, "Hypotenuse", 22, ROT, "middle", "bold", 'transform="rotate(-30 250 200)"'),
         txt(280, 365, "Ankathete von α", 22, BLAU, "middle", "bold"),
         txt(490, 225, "Gegenkathete", 22, GRUEN, weight="bold"),
         txt(490, 252, "von α", 22, GRUEN, weight="bold"),
         txt(660, 150, "sin(α) = Gegenkathete : Hypotenuse", 21, NAVY),
         txt(660, 195, "cos(α) = Ankathete : Hypotenuse", 21, NAVY),
         txt(660, 240, "tan(α) = Gegenkathete : Ankathete", 21, NAVY),
         txt(660, 300, "Taschenrechner auf DEG (Grad) stellen!", 19, ORANGE, weight="bold")]
    svg("dreieck.svg", 1040, 400, "\n".join(b))


# ------------------------------------------------------------ Vektor und Komponenten
def vektor():
    O = (260, 360)
    L, a = 330, math.radians(35)
    E = (O[0] + L * math.cos(a), O[1] - L * math.sin(a))
    b = [pfeil(O[0] - 20, O[1], 700, O[1], "#333", "k", 2), pfeil(O[0], O[1] + 20, O[0], 50, "#333", "k", 2),
         txt(705, O[1] + 26, "x", 20, "#333", style='font-style="italic"'), txt(O[0] - 26, 60, "y", 20, "#333", style='font-style="italic"'),
         pfeil(O[0], O[1], E[0], O[1], BLAU, "b", 5),
         f'<line x1="{E[0]:.1f}" y1="{O[1]}" x2="{E[0]:.1f}" y2="{E[1]:.1f}" stroke="{GRUEN}" stroke-width="2" stroke-dasharray="7 6"/>',
         pfeil(O[0], O[1], O[0], E[1], GRUEN, "g", 5),
         f'<line x1="{O[0]}" y1="{E[1]:.1f}" x2="{E[0]:.1f}" y2="{E[1]:.1f}" stroke="{BLAU}" stroke-width="2" stroke-dasharray="7 6"/>',
         pfeil(O[0], O[1], E[0], E[1], ROT, "r", 6),
         f'<path d="M{O[0] + 70},{O[1]} A70,70 0 0 0 {O[0] + 70 * math.cos(a):.1f},{O[1] - 70 * math.sin(a):.1f}" fill="none" stroke="{ROT}" stroke-width="2.5"/>',
         txt(O[0] + 78, O[1] - 14, "α", 24, ROT, weight="bold"),
         txt(E[0] - 150, E[1] - 30, "v⃗ (Betrag v, Richtung α)", 22, ROT, weight="bold"),
         txt((O[0] + E[0]) / 2, O[1] + 34, "vₓ = v · cos(α)", 21, BLAU, "middle", "bold"),
         txt(O[0] - 14, (O[1] + E[1]) / 2, "v_y = v · sin(α)", 21, GRUEN, "end", "bold"),
         txt(760, 120, "Ein Vektor ist ein Pfeil mit", 21, NAVY),
         txt(760, 152, "• Betrag (Länge) und", 21, NAVY),
         txt(760, 184, "• Richtung.", 21, NAVY),
         txt(760, 240, "Er lässt sich in Komponenten", 21, NAVY),
         txt(760, 272, "zerlegen: v⃗ = vₓ-Pfeil + v_y-Pfeil", 21, NAVY),
         txt(760, 320, "Betrag: v = √(vₓ² + v_y²)", 21, NAVY, weight="bold")]
    svg("vektor.svg", 1140, 420, "\n".join(b))


# ------------------------------------------------------------ Bahn mit Geschwindigkeitskomponenten
def bahn():
    ax = Achsen(70, 40, 860, 330, 0, 10.4, 0, 3.3)
    v0, a = 10, math.radians(40)
    vx, vy = v0 * math.cos(a), v0 * math.sin(a)
    tE = 2 * vy / G
    b = [f'<rect x="0" y="0" width="1000" height="440" fill="#fff"/>']
    x0, y0 = ax.px(0, 0)
    b.append(pfeil(x0 - 10, y0, 960, y0, "#333", "k", 2))
    b.append(pfeil(x0, y0 + 10, x0, 25, "#333", "k", 2))
    b.append(txt(962, y0 + 26, "x", 20, "#333", style='font-style="italic"'))
    b.append(txt(x0 - 26, 38, "y", 20, "#333", style='font-style="italic"'))
    b.append(ax.kurve(lambda t: (vx * t, vy * t - G / 2 * t * t), 0, tE, NAVY, 3, extra='stroke-dasharray="9 7"'))
    k = 11  # Pixel pro m/s
    for t in (0, 0.33, tE / 2, 0.98):
        x, y = vx * t, vy * t - G / 2 * t * t
        px, py = ax.px(x, y)
        vyt = vy - G * t
        b.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="9" fill="{GRAU}" stroke="#333" stroke-width="2"/>')
        b.append(pfeil(px, py, px + vx * k, py, BLAU, "b", 4))
        if abs(vyt) > 0.3:
            b.append(pfeil(px, py, px, py - vyt * k, GRUEN, "g", 4))
        b.append(pfeil(px, py, px + vx * k, py - vyt * k, ROT, "r", 4))
    px, py = ax.px(vx * tE / 2, vy * tE / 2 - G / 8 * tE * tE)
    b.append(txt(px, py - 26, "Scheitelpunkt: v_y = 0", 19, NAVY, "middle", "bold"))
    b.append(txt(x0 + 62, y0 - 12, "α", 22, ROT, weight="bold"))
    b.append(txt(70, 420, "rot: Geschwindigkeit v⃗   ·   blau: vₓ (bleibt gleich)   ·   grün: v_y (nimmt ab, wird null, dann negativ)", 18, "#333"))
    svg("bahn.svg", 1000, 440, "\n".join(b))


# ------------------------------------------------------------ Versuch V1: Boule-Kugel
def boule():
    b = []
    ax1 = Achsen(80, 40, 760, 230, 0, 0.7, 0, 2.5)
    b += ax1.raster(0.1, 0.5, "t in s", "x in m")
    b.append(ax1.kurve(lambda t: (t, 3.71 * t), 0, 0.6, BLAU, 2.5))
    for i in range(16):
        t = i * 0.04
        b.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s"/>' % (*ax1.px(t, 3.71 * t), NAVY))
    ax2 = Achsen(80, 370, 760, 230, 0, 0.7, 0, 0.8)
    b += ax2.raster(0.1, 0.2, "t in s", "y in m")
    b.append(ax2.kurve(lambda t: (t, -4.97 * t * t + 2.43 * t + 0.44), 0, 0.6, ROT, 2.5))
    for i in range(16):
        t = i * 0.04
        b.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s"/>' % (*ax2.px(t, -4.97 * t * t + 2.43 * t + 0.44), NAVY))
    b.append(txt(880, 140, "x(t) = 3,71 · t", 22, BLAU, weight="bold"))
    b.append(txt(880, 470, "y(t) = −4,97 t² + 2,43 t + 0,44", 22, ROT, weight="bold"))
    b.append(txt(880, 175, "(Regression bis t = 0,6 s)", 18, "#555"))
    svg("boule.svg", 1240, 650, "\n".join(b))


# ------------------------------------------------------------ Kugelstoß: Bahnen für verschiedene Winkel
def kugelstoss():
    ax = Achsen(80, 40, 800, 330, 0, 10, 0, 5)
    b = ax.raster(1, 1, "x in m", "y in m")
    v0 = 8.5
    for wnk, farbe in ((20, BLAU), (40, ROT), (60, GRUEN)):
        a = math.radians(wnk)
        vx, vy = v0 * math.cos(a), v0 * math.sin(a)
        tE = (vy + math.sqrt(vy * vy + 2 * G * 2)) / G
        b.append(ax.kurve(lambda t: (vx * t, 2 + vy * t - G / 2 * t * t), 0, tE, farbe, 3.5))
        xs = vx * tE
        px, py = ax.px(xs, 0)
        b.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{farbe}"/>')
        tx, ty = ax.px(vx * tE * 0.45, 2 + vy * tE * 0.45 - G / 2 * (tE * 0.45) ** 2)
        b.append(txt(tx, ty - 12, f"α = {wnk}°", 20, farbe, "middle", "bold"))
    b.append('<circle cx="%.1f" cy="%.1f" r="7" fill="#333"/>' % ax.px(0, 2))
    b.append(txt(940, 120, "v₀ = 8,5 m/s", 21, NAVY, weight="bold"))
    b.append(txt(940, 152, "Starthöhe 2 m", 21, NAVY, weight="bold"))
    svg("kugelstoss.svg", 1140, 420, "\n".join(b))


# ------------------------------------------------------------ Weitsprung (Aufgabe 3)
def weitsprung():
    ax = Achsen(80, 60, 900, 260, -0.8, 10.4, 0, 2.6)
    b = []
    gx0, gy0 = ax.px(-0.8, 0)
    gx1, _ = ax.px(10.4, 0)
    b.append(f'<line x1="{gx0}" y1="{gy0}" x2="{gx1}" y2="{gy0}" stroke="#333" stroke-width="3"/>')
    bx, by = ax.px(-0.6, 0)
    b.append(f'<rect x="{bx - 14:.1f}" y="{by - 6:.1f}" width="28" height="12" fill="{ORANGE}"/>')
    b.append(txt(bx, by + 30, "Absprung", 17, "#333", "middle"))
    vx, vy = 10 * math.cos(math.radians(25)), 10 * math.sin(math.radians(25))
    tE = (vy + math.sqrt(vy * vy + 2 * G * 0.4)) / G
    xw = vx * tE
    b.append(ax.kurve(lambda t: (vx * t, 0.9 + vy * t - G / 2 * t * t), 0, tE, ROT, 3.5))
    sx, sy = ax.px(0, 0.9)
    ex, ey = ax.px(xw, 0.5)
    b.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="8" fill="{NAVY}"/>')
    b.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="8" fill="{NAVY}"/>')
    b.append(pfeil(sx, sy, sx + 140 * math.cos(math.radians(25)), sy - 140 * math.sin(math.radians(25)) * (260 / 2.6) / (900 / 11.2), ROT, "r", 3))
    b.append(txt(sx + 60, sy + 2, "25°", 19, ROT, weight="bold"))
    b.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{sx + 120:.1f}" y2="{sy:.1f}" stroke="{GRAU}" stroke-width="2" stroke-dasharray="6 5"/>')
    # Höhen
    b.append(f'<line x1="{sx - 30:.1f}" y1="{sy:.1f}" x2="{sx - 30:.1f}" y2="{gy0}" stroke="{NAVY}" stroke-width="1.6" marker-start="url(#pn)" marker-end="url(#pn)"/>')
    b.append(txt(sx - 38, (sy + gy0) / 2 + 6, "0,9 m", 18, NAVY, "end"))
    b.append(f'<line x1="{ex + 30:.1f}" y1="{ey:.1f}" x2="{ex + 30:.1f}" y2="{gy0}" stroke="{NAVY}" stroke-width="1.6" marker-start="url(#pn)" marker-end="url(#pn)"/>')
    b.append(txt(ex + 38, (ey + gy0) / 2 + 6, "0,5 m", 18, NAVY))
    # d1, d2
    lx, _ = ax.px(xw + 0.75, 0)
    b.append(f'<line x1="{bx:.1f}" y1="{gy0 + 46}" x2="{sx:.1f}" y2="{gy0 + 46}" stroke="#333" stroke-width="1.6" marker-start="url(#pk)" marker-end="url(#pk)"/>')
    b.append(txt((bx + sx) / 2, gy0 + 72, "d₁ ≈ 0,6 m", 17, "#333", "middle"))
    b.append(f'<line x1="{ex:.1f}" y1="{gy0 + 46}" x2="{lx:.1f}" y2="{gy0 + 46}" stroke="#333" stroke-width="1.6" marker-start="url(#pk)" marker-end="url(#pk)"/>')
    b.append(txt((ex + lx) / 2, gy0 + 72, "d₂ ≈ 0,75 m", 17, "#333", "middle"))
    b.append(f'<rect x="{lx - 6:.1f}" y="{gy0 - 6}" width="12" height="12" fill="{GRAU}"/>')
    b.append(txt(lx, gy0 + 30, "Landung (Ferse)", 17, "#333", "middle"))
    b.append(txt((sx + ex) / 2, sy - 150, "Flugbahn des Körperschwerpunkts (Wurfparabel)", 19, ROT, "middle", "bold"))
    b.append(txt(80, 30, "Weitsprung: v₀ = 10 m/s, α = 25°   (Skizze nicht maßstäblich)", 19, "#333"))
    svg("weitsprung.svg", 1060, 420, "\n".join(b))


# ------------------------------------------------------------ Blasrohr und Dose (Aufgabe 4)
def blasrohr():
    b = []
    S, Z = (110, 380), (760, 90)
    b.append(f'<line x1="{S[0]}" y1="{S[1]}" x2="{Z[0]}" y2="{Z[1]}" stroke="{GRAU}" stroke-width="2.5" stroke-dasharray="9 7"/>')
    b.append(f'<line x1="{S[0] - 40}" y1="{S[1] + 18}" x2="{S[0] + 30}" y2="{S[1] - 13}" stroke="#555" stroke-width="12" stroke-linecap="round"/>')
    # Dose oben (Start) und Treffpunkt
    b.append(f'<rect x="{Z[0] - 18}" y="{Z[1] - 34}" width="36" height="56" rx="5" fill="none" stroke="{ROT}" stroke-width="2.5" stroke-dasharray="6 5"/>')
    T = (760, 250)
    b.append(f'<rect x="{T[0] - 18}" y="{T[1] - 34}" width="36" height="56" rx="5" fill="{ROT}"/>')
    b.append(pfeil(Z[0] + 40, Z[1], Z[0] + 40, T[1] - 20, ROT, "r", 3))
    b.append(txt(Z[0] + 50, (Z[1] + T[1]) / 2, "Dose fällt frei", 19, ROT))
    # gekrümmte Bahn der Kugel
    pts = []
    for i in range(61):
        u = i / 60
        x = S[0] + (T[0] - S[0]) * u
        y_lin = S[1] + (Z[1] - S[1]) * u
        y = y_lin + (T[1] - Z[1]) * u * u
        pts.append(f"{x:.1f},{y:.1f}")
    b.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{NAVY}" stroke-width="3"/>')
    b.append(txt(330, 330, "Bahn des Kügelchens", 19, NAVY, weight="bold"))
    b.append(txt(260, 210, "Zielrichtung (ohne Schwerkraft)", 18, GRAU, style='transform="rotate(-24 260 210)"'))
    b.append(txt(40, 440, "Das Blasrohr zielt direkt auf die Dose. Sie wird losgelassen, wenn das Kügelchen abgeschossen wird.", 18, "#333"))
    svg("blasrohr.svg", 960, 460, "\n".join(b))


# ------------------------------------------------------------ Karte (Hintergrund, sachlich)
def karte():
    W, H = 1600, 1000
    b = [f'<rect width="{W}" height="{H}" fill="#14273d"/>']
    for x in range(0, W + 1, 25):
        b.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#1d3654" stroke-width="{1.6 if x % 100 == 0 else 0.7}"/>')
    for y in range(0, H + 1, 25):
        b.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#1d3654" stroke-width="{1.6 if y % 100 == 0 else 0.7}"/>')
    # Achsen
    b.append(pfeil(40, 960, 1575, 960, "#5d7fa3", "k", 2.5, 'opacity="0.9"').replace('url(#pk)', 'url(#pa)'))
    b.append(pfeil(40, 960, 40, 25, "#5d7fa3", "k", 2.5, 'opacity="0.9"').replace('url(#pk)', 'url(#pa)'))
    b.append(txt(1560, 990, "x", 22, "#8fb1d6", style='font-style="italic"'))
    b.append(txt(14, 40, "y", 22, "#8fb1d6", style='font-style="italic"'))
    # Formeln dezent
    for x, y, s in ((560, 600, "x(t) = v₀ · cos(α) · t"), (560, 645, "y(t) = −½ g t² + v₀ · sin(α) · t + y₀"),
                    (560, 690, "w = 2 v₀² · cos(α) · sin(α) / g")):
        b.append(txt(x, y, s, 26, "#4f7196", style='font-family="Georgia,serif" font-style="italic"'))
    # Titel
    b.append(txt(560, 520, "Der schiefe Wurf", 54, "#c9d9ea", weight="bold", style='font-family="Georgia,serif" letter-spacing="1"'))
    b.append(txt(562, 556, "Physik · Einführungsphase · Grundlagen der Mechanik", 21, "#7f9fc2"))
    with open(os.path.join(OUT, "karte.svg"), "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" {FONT}>'
                '<defs><marker id="pa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                '<path d="M0,0 L10,5 L0,10 z" fill="#5d7fa3"/></marker></defs>\n' + "\n".join(b) + "\n</svg>\n")


dreieck()
vektor()
bahn()
boule()
kugelstoss()
weitsprung()
blasrohr()
karte()
print("SVGs geschrieben nach", OUT)
