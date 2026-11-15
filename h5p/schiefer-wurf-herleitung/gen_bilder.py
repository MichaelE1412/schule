#!/usr/bin/env python3
"""Grafiken für „Der schiefe Wurf – Herleitung“ (Klasse 11).

Nutzt die Zeichenfunktionen aus ../schiefer-wurf/gen_bilder.py und ergänzt
Bahnkurven (Buch S. 10), den Schwimmer im Fluss (S. 10–11) und die Karte.
Aufruf: python3 gen_bilder.py   (schreibt nach bilder/)
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wb", os.path.join(HERE, "..", "schiefer-wurf", "gen_bilder.py"))
wb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wb)
wb.OUT = os.path.join(HERE, "bilder")
os.makedirs(wb.OUT, exist_ok=True)

NAVY, BLAU, ROT, GRUEN, ORANGE, GRAU = wb.NAVY, wb.BLAU, wb.ROT, wb.GRUEN, wb.ORANGE, wb.GRAU
txt, pfeil, svg, Achsen = wb.txt, wb.pfeil, wb.svg, wb.Achsen


def kasten(x, y, n):
    return (f'<rect x="{x - 14:.1f}" y="{y - 16:.1f}" width="28" height="28" fill="#fff" stroke="#333" stroke-width="2"/>'
            + txt(x, y + 6, str(n), 19, "#333", "middle", "bold"))


def bahnkurven():
    ax = Achsen(90, 40, 820, 400, -15, 20, 0, 20)
    b = ax.raster(5, 5, "x in m", "y in m")
    # Bewegung 1: parallel zur Rechtsachse
    x0, y0 = ax.px(-7.5, 1)
    x1, y1 = ax.px(15, 1)
    b.append(pfeil(x0, y0, x1, y1, BLAU, "b", 4))
    for xx in (-7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10, 12.5):
        b.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (*ax.px(xx, 1), BLAU))
    b.append(kasten(*ax.px(-10.5, 2.6), 1))
    # Bewegung 2: Gerade unter dem Winkel alpha
    x0, y0 = ax.px(0, 1)
    x1, y1 = ax.px(16, 13)
    b.append(pfeil(x0, y0, x1, y1, ROT, "r", 4))
    b.append(kasten(*ax.px(17.6, 15), 2))
    b.append(f'<path d="M{x0 + 60:.1f},{y0:.1f} A60,60 0 0 0 {x0 + 60 * 0.8:.1f},{y0 - 60 * 0.6:.1f}" fill="none" stroke="{ROT}" stroke-width="2"/>')
    b.append(txt(x0 + 68, y0 - 10, "α", 20, ROT, weight="bold"))
    # Bewegung 3: gekrümmte Bahn
    b.append(ax.kurve(lambda t: (t, 12 - 0.03 * t * t), -12, 12, GRUEN, 4))
    b.append(kasten(*ax.px(4, 15.5), 3))
    b.append(txt(940, 120, "1: parallel zur Rechtsachse", 19, BLAU, weight="bold"))
    b.append(txt(940, 155, "2: geradlinig unter dem Winkel α", 19, ROT, weight="bold"))
    b.append(txt(940, 190, "3: gekrümmt – die Richtung", 19, GRUEN, weight="bold"))
    b.append(txt(958, 218, "ändert sich ständig", 19, GRUEN, weight="bold"))
    svg("bahnkurven.svg", 1260, 500, "\n".join(b))


def schwimmer():
    b = ['<rect x="0" y="0" width="1000" height="460" fill="#fff"/>',
         '<rect x="170" y="20" width="560" height="400" fill="#d7ecf8"/>',
         '<rect x="120" y="20" width="50" height="400" fill="#cfe3a8"/>',
         '<rect x="730" y="20" width="50" height="400" fill="#cfe3a8"/>']
    for y in (80, 180, 280, 380):
        b.append(pfeil(820, y + 40, 820, y - 10, "#5aa0c8", "b", 2))
    b.append(txt(840, 240, "Strömung", 19, "#2f6fa7"))
    O = (200, 380)
    vx, vy = 380, 190
    b.append(f'<circle cx="{O[0]}" cy="{O[1]}" r="10" fill="{ORANGE}"/>')
    b.append(pfeil(O[0], O[1], O[0] + vx, O[1], BLAU, "b", 5))
    b.append(pfeil(O[0], O[1], O[0], O[1] - vy, GRUEN, "g", 5))
    b.append(f'<line x1="{O[0] + vx}" y1="{O[1]}" x2="{O[0] + vx}" y2="{O[1] - vy}" stroke="{GRUEN}" stroke-width="2" stroke-dasharray="7 6"/>')
    b.append(f'<line x1="{O[0]}" y1="{O[1] - vy}" x2="{O[0] + vx}" y2="{O[1] - vy}" stroke="{BLAU}" stroke-width="2" stroke-dasharray="7 6"/>')
    b.append(pfeil(O[0], O[1], O[0] + vx, O[1] - vy, ROT, "r", 6))
    b.append(txt(O[0] + vx / 2, O[1] + 34, "v⃗_x: Schwimmer (quer zum Fluss)", 20, BLAU, "middle", "bold"))
    b.append(txt(O[0] + 14, O[1] - vy - 14, "v⃗_y: Strömung", 20, GRUEN, weight="bold"))
    b.append(txt(O[0] + vx / 2 + 90, O[1] - vy / 2 + 60, "v⃗ = v⃗_x + v⃗_y", 22, ROT, "middle", "bold"))
    b.append(txt(40, 452, "Ansicht von oben. Stehen v⃗_x und v⃗_y senkrecht aufeinander, gilt v = √(v_x² + v_y²).", 18, "#333"))
    svg("schwimmer.svg", 1000, 470, "\n".join(b))


def karte():
    W, H = 1600, 1000
    b = [f'<rect width="{W}" height="{H}" fill="#14273d"/>']
    for x in range(0, W + 1, 25):
        b.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#1d3654" stroke-width="{1.6 if x % 100 == 0 else 0.7}"/>')
    for y in range(0, H + 1, 25):
        b.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#1d3654" stroke-width="{1.6 if y % 100 == 0 else 0.7}"/>')
    # dezente Wurfparabel im Hintergrund
    para = []
    for i in range(101):
        x = 80 + i * 14.4
        y = 950 - 880 * (1 - ((x - 800) / 720) ** 2)
        para.append(f"{x:.1f},{y:.1f}")
    b.append(f'<polyline points="{" ".join(para)}" fill="none" stroke="#1f3c5e" stroke-width="4" stroke-dasharray="14 12"/>')
    kopf = [(40, 812, "A · Vektoren (Wiederholung)"), (650, 548, "B · Fragen zum Text"),
            (40, 258, "C · Herleitungspuzzle"), (1100, 252, "D · Aufgabe 1")]
    for x, y, s in kopf:
        b.append(txt(x, y, s, 27, "#9fc0e2", weight="bold", style='letter-spacing="0.5"'))
    b.append(txt(40, 70, "Der schiefe Wurf", 44, "#d6e4f2", weight="bold", style='font-family="Georgia,serif"'))
    b.append(txt(42, 104, "Physik · Klasse 11 · Herleitung und Anwendung", 20, "#7f9fc2"))
    with open(os.path.join(wb.OUT, "karte.svg"), "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
                'font-family="Helvetica,Arial,sans-serif">\n' + "\n".join(b) + "\n</svg>\n")


if __name__ == "__main__":
    wb.dreieck()
    wb.vektor()
    wb.bahn()
    wb.boule()
    wb.kugelstoss()
    bahnkurven()
    schwimmer()
    karte()
    print("SVGs geschrieben nach", wb.OUT)
