#!/usr/bin/env python3
"""Baut den Lernpfad „Der schiefe Wurf“ (Physik EF) als H5P Game Map.

Aufruf:  python3 build.py <entpackte Trapez-Referenz> <Ausgabe.h5p>

Inhalte: Grundlagen der Mechanik, Kap. 1.6 „Der schiefe Wurf“ (S. 26–29), ohne Exkurse.
Aufgaben 1–3 als Beispielaufgaben mit Hilfe-Abzweigen; 4 und 6 als Vertiefung.
"""
import json
import math
import os
import sys
import zipfile

from bausteine import alt, dragtext, image, mc, route, text, blanks

HERE = os.path.dirname(os.path.abspath(__file__))
REF, OUT = sys.argv[1], sys.argv[2]

IMG = {
    "dreieck": ("images/dreieck.png", 1040, 400, "Rechtwinkliges Dreieck mit Hypotenuse, Ankathete und Gegenkathete von α"),
    "vektor": ("images/vektor.png", 1140, 420, "Geschwindigkeitsvektor v mit Winkel α und den Komponenten v_x und v_y"),
    "bahn": ("images/bahn.png", 1000, 440, "Bahn beim schiefen Wurf mit Geschwindigkeitsvektor und Komponenten an vier Stellen"),
    "boule": ("images/boule.png", 1240, 650, "Messwerte und Regressionskurven x(t) und y(t) der Boule-Kugel"),
    "kugelstoss": ("images/kugelstoss.png", 1140, 420, "Wurfbahnen beim Kugelstoß für 20°, 40° und 60° bei 2 m Starthöhe und 8,5 m/s"),
    "weitsprung": ("images/weitsprung.png", 1060, 420, "Skizze Weitsprung: Schwerpunkt startet in 0,9 m, landet in 0,5 m Höhe; d1 = 0,6 m, d2 = 0,75 m"),
    "blasrohr": ("images/blasrohr.png", 960, 460, "Blasrohr zielt auf eine Dose, die beim Abschuss losgelassen wird"),
}

# ---------------------------------------------------------------- Lage der Etappen: auf einer Wurfparabel
X0, X1, YTOP, YBOT = 110, 1490, 130, 890
XS = (X0 + X1) / 2
HALB = (X1 - X0) / 2


def parabel(x):
    return YTOP + (YBOT - YTOP) * ((x - XS) / HALB) ** 2


def normale(x):
    """Einheitsnormale nach außen (über der Kurve) im Bildschirm-Koordinatensystem."""
    m = 2 * (YBOT - YTOP) * (x - XS) / HALB ** 2
    n = math.hypot(m, 1)
    return m / n, -1 / n


HAUPT = ["Start", "D1", "M1", "M2", "E1", "E2", "E3", "E4", "A1", "A2", "A3", "Ziel"]
POS, LAB = {}, {}
for i, k in enumerate(HAUPT):
    x = X0 + i * (X1 - X0) / (len(HAUPT) - 1)
    POS[k] = (round(x), round(parabel(x)))
    nx, ny = normale(x)
    LAB[k] = (round(-nx * 60), round(-ny * 60))      # Schild innen (unter der Kurve)
for k, (a, b) in {"H1": ("D1", "M1"), "H2": ("M1", "M2"), "H3": ("M2", "E1"),
                  "T1": ("A1", "A2"), "T2": ("A2", "A3"), "T3": ("A3", "Ziel")}.items():
    xm = (POS[a][0] + POS[b][0]) / 2
    nx, ny = normale(xm)
    POS[k] = (round(xm + nx * 130), round(parabel(xm) + ny * 130))
    LAB[k] = (round(nx * 60), round(ny * 60))        # Schild außen
POS.update({"X1": (1175, 650), "X2": (1175, 765), "X3": (1175, 880)})
LAB.update({"X1": (-68, 0), "X2": (-68, 0), "X3": (-68, 0), "Start": (0, 58), "Ziel": (0, 58), "T3": (0, -55)})

S = []


def stage(key, label, neighbors, contents, start=False, special=None):
    S.append(dict(key=key, label=label, nb=neighbors, contents=contents, start=start, special=special))


def weiter(ziel):
    return f"Richtig. Weiter zu {ziel}."


# ================================================================ Start und Vorwissen
stage("Start", "Start", ["D1"], [text("Start", """
<h2>Der schiefe Wurf</h2>
<p><strong>Leitfrage:</strong> Unter welchem Winkel sollte eine Kugelstoßerin stoßen, um möglichst weit zu kommen – und warum sind das nicht 45°?</p>
<p><strong>Ablauf (ca. 2 Stunden)</strong></p>
<ol>
<li><strong>D</strong> – Vorwissen: waagerechter und senkrechter Wurf</li>
<li><strong>M</strong> – Mathematische Werkzeuge: Sinus und Kosinus, Vektoren</li>
<li><strong>E</strong> – Erarbeitung: Bewegungsgleichungen, Versuch, Wurfweite, Starthöhe</li>
<li><strong>A</strong> – Beispielaufgaben 1–3 aus dem Buch</li>
<li><strong>X</strong> – Vertiefung (optional)</li>
</ol>
<p><strong>H</strong> und <strong>T</strong> sind Hilfe-Abzweige. Gehen Sie nur dorthin, wenn eine Rückmeldung Sie hinschickt.</p>
<p><strong>Konventionen:</strong> \\(g=9{,}81\\,\\frac{\\text{m}}{\\text{s}^2}\\), Luftwiderstand wird vernachlässigt, Taschenrechner im Gradmaß (DEG). Runden Sie auf zwei Nachkommastellen und verwenden Sie das Dezimalkomma. Einheiten stehen hinter den Eingabefeldern.</p>
""")], start=True)

stage("D1", "D1 Vorwissen Würfe", ["Start", "H1", "M1"], [
    blanks("D1-waagerecht", """
<h3>D1 – Vorwissen</h3>
<p><strong>a) Waagerechter Wurf:</strong> Eine Kugel rollt mit \\(4\\,\\frac{\\text{m}}{\\text{s}}\\) über die Kante eines \\(1{,}25\\,\\text{m}\\) hohen Tisches.</p>
""", ["<p>Fallzeit t ≈ *%s:Die Fallzeit hängt nur von der Höhe ab.* s</p>" % alt("0,5", "0,50", "0,505", "0,51"),
      "<p>Wurfweite x ≈ *%s* m</p>" % alt("2,02", "2,0", "2,01", "2,04")],
        route("Gehen Sie zuerst zum Abzweig H1.", "Richtig.")),
    blanks("D1-senkrecht", "<p><strong>b) Senkrechter Wurf nach oben:</strong> Ein Ball wird mit \\(12\\,\\frac{\\text{m}}{\\text{s}}\\) senkrecht nach oben geworfen.</p>",
           ["<p>Steigzeit t<sub>S</sub> ≈ *%s:Am höchsten Punkt ist v = 0.* s</p>" % alt("1,22", "1,2", "1,223"),
            "<p>Steighöhe h ≈ *%s* m</p>" % alt("7,34", "7,3", "7,339", "7,32", "7,35")],
           route("Gehen Sie zuerst zum Abzweig H1.", "Richtig.")),
    mc("D1-Prinzip", "<p><strong>c)</strong> Warum fällt die Kugel aus a) genauso lange wie eine Kugel, die man an der Tischkante einfach fallen lässt?</p>",
       [("Die vertikale Bewegung ist ein freier Fall, der unabhängig von der horizontalen Bewegung abläuft.", True, ""),
        ("Das stimmt nicht: Die rollende Kugel fällt länger, weil sie schneller ist.", False,
         "Die horizontale Geschwindigkeit ändert nichts an der vertikalen Bewegung."),
        ("Weil beide Kugeln die gleiche Masse haben.", False, "Die Fallzeit hängt beim freien Fall gar nicht von der Masse ab.")],
       route("Gehen Sie zuerst zum Abzweig H1.", weiter("M1")), single=True)])

stage("H1", "H1 Hilfe Würfe", ["D1", "M1"], [
    text("H1", """
<h3>H1 – Abzweig: Würfe und freier Fall</h3>
<table border="1" cellpadding="5" style="border-collapse:collapse">
<tr><th>Bewegung</th><th>Ort</th><th>Geschwindigkeit</th></tr>
<tr><td>freier Fall</td><td>\\(y(t)=-\\frac{g}{2}t^2\\)</td><td>\\(v(t)=-g\\cdot t\\)</td></tr>
<tr><td>senkrechter Wurf nach oben</td><td>\\(y(t)=v_0\\cdot t-\\frac{g}{2}t^2\\)</td><td>\\(v(t)=v_0-g\\cdot t\\)</td></tr>
<tr><td>waagerechter Wurf aus Höhe \\(h\\)</td><td>\\(x(t)=v_0\\cdot t,\\; y(t)=h-\\frac{g}{2}t^2\\)</td><td>\\(v_x=v_0,\\; v_y=-g\\cdot t\\)</td></tr>
</table>
<p>Steigzeit beim senkrechten Wurf: \\(v(t_S)=0 \\Rightarrow t_S=\\frac{v_0}{g}\\). Steighöhe: \\(h=\\frac{v_0^2}{2g}\\).</p>
<p><strong>Superpositionsprinzip:</strong> Horizontale und vertikale Bewegung laufen unabhängig voneinander ab und überlagern sich.</p>
"""),
    blanks("H1-Aufgabe", "<p><strong>Parallelaufgaben:</strong> a) Waagerechter Wurf aus \\(1{,}8\\,\\text{m}\\) Höhe mit \\(3\\,\\frac{\\text{m}}{\\text{s}}\\). b) Senkrechter Wurf mit \\(15\\,\\frac{\\text{m}}{\\text{s}}\\).</p>",
           ["<p>a) t ≈ *%s* s, x ≈ *%s* m</p>" % (alt("0,61", "0,6", "0,606"), alt("1,82", "1,8", "1,817", "1,83")),
            "<p>b) t<sub>S</sub> ≈ *%s* s, h ≈ *%s* m</p>" % (alt("1,53", "1,5", "1,529"), alt("11,47", "11,5", "11,468", "11,46"))],
           route("Notieren Sie, wo Sie hängen, und gehen Sie weiter zu M1. Fragen Sie bei Bedarf nach.",
                 "Richtig. Weiter zu M1."))])

# ================================================================ Mathematische Werkzeuge
stage("M1", "M1 Sinus und Kosinus", ["D1", "H1", "H2", "M2"], [
    image("M1-Bild", IMG["dreieck"]),
    blanks("M1", """
<h3>M1 – Wiederholung: Sinus und Kosinus</h3>
<p>Beim schiefen Wurf zerlegt man die Abwurfgeschwindigkeit mit Sinus und Kosinus. Frischen Sie die Begriffe auf.</p>
<p>a) Ein rechtwinkliges Dreieck hat die Hypotenuse \\(10\\,\\text{m}\\) und den Winkel \\(\\alpha=30^\\circ\\).</p>
""", ["<p>Gegenkathete von α = *%s:Gegenkathete = Hypotenuse · sin(α)* m</p>" % alt("5", "5,0", "5,00"),
      "<p>Ankathete von α ≈ *%s:Ankathete = Hypotenuse · cos(α)* m</p>" % alt("8,66", "8,7", "8,660"),
      "<p>b) Ankathete 3 cm, Gegenkathete 4 cm: α ≈ *%s:tan(α) = Gegenkathete : Ankathete, dann tan⁻¹* °</p>" % alt("53,13", "53,1", "53", "53,13")],
        route("Gehen Sie zuerst zum Abzweig H2.", "Richtig. Weiter zu M2."))])

stage("H2", "H2 Hilfe Trigonometrie", ["M1", "M2"], [
    text("H2", """
<h3>H2 – Abzweig: Trigonometrie im rechtwinkligen Dreieck</h3>
<ul>
<li><strong>Hypotenuse:</strong> liegt dem rechten Winkel gegenüber, längste Seite.</li>
<li><strong>Gegenkathete von α:</strong> liegt dem Winkel α gegenüber.</li>
<li><strong>Ankathete von α:</strong> liegt am Winkel α an (und ist nicht die Hypotenuse).</li>
</ul>
<p>\\[ \\sin(\\alpha)=\\frac{\\text{Gegenkathete}}{\\text{Hypotenuse}} \\qquad \\cos(\\alpha)=\\frac{\\text{Ankathete}}{\\text{Hypotenuse}} \\qquad \\tan(\\alpha)=\\frac{\\text{Gegenkathete}}{\\text{Ankathete}} \\]</p>
<p>Umgestellt: Gegenkathete \\(=\\) Hypotenuse \\(\\cdot\\sin(\\alpha)\\), Ankathete \\(=\\) Hypotenuse \\(\\cdot\\cos(\\alpha)\\). Winkel aus Seiten: \\(\\sin^{-1}\\), \\(\\cos^{-1}\\), \\(\\tan^{-1}\\).</p>
<p><strong>Taschenrechner-Test:</strong> \\(\\sin(30)\\) muss \\(0{,}5\\) ergeben. Erscheint \\(-0{,}988\\), steht der Rechner im Bogenmaß (RAD).</p>
"""),
    image("H2-Bild", IMG["dreieck"]),
    blanks("H2-Aufgabe", "<p><strong>Parallelaufgabe:</strong> Hypotenuse \\(8\\,\\text{cm}\\), \\(\\alpha=40^\\circ\\).</p>",
           ["<p>Gegenkathete ≈ *%s* cm</p>" % alt("5,14", "5,1", "5,142"),
            "<p>Ankathete ≈ *%s* cm</p>" % alt("6,13", "6,1", "6,128")],
           route("Notieren Sie, wo Sie hängen, und gehen Sie weiter zu M2.", "Richtig. Weiter zu M2."))])

stage("M2", "M2 Vektoren", ["M1", "H2", "H3", "E1"], [
    text("M2", """
<h3>M2 – Neu: Vektoren</h3>
<p>Manche physikalischen Größen sind schon durch Zahlenwert und Einheit vollständig beschrieben, z. B. Masse \\(m=2\\,\\text{kg}\\) oder Zeit \\(t=3\\,\\text{s}\\). Solche Größen heißen <strong>Skalare</strong>.</p>
<p>Bei anderen Größen kommt es zusätzlich auf die <strong>Richtung</strong> an: Ein Ball, der mit \\(10\\,\\frac{\\text{m}}{\\text{s}}\\) nach oben fliegt, bewegt sich anders als einer, der mit \\(10\\,\\frac{\\text{m}}{\\text{s}}\\) nach rechts fliegt. Solche Größen heißen <strong>Vektoren</strong>. Man stellt sie als Pfeil dar und kennzeichnet sie mit einem Pfeil über dem Formelzeichen: \\(\\vec v\\).</p>
<ul>
<li>Die <strong>Länge</strong> des Pfeils gibt den <strong>Betrag</strong> an: \\(|\\vec v|=v\\).</li>
<li>Die <strong>Richtung</strong> des Pfeils gibt die Bewegungsrichtung an, z. B. durch den Winkel \\(\\alpha\\) zur Horizontalen.</li>
<li>Ein Vektor lässt sich in <strong>Komponenten</strong> entlang der Achsen zerlegen: \\(\\vec v=\\begin{pmatrix} v_x \\\\ v_y \\end{pmatrix}\\) mit \\(v_x=v\\cdot\\cos(\\alpha)\\) und \\(v_y=v\\cdot\\sin(\\alpha)\\).</li>
<li>Umgekehrt gilt \\(v=\\sqrt{v_x^2+v_y^2}\\) (Pythagoras) und \\(\\tan(\\alpha)=\\frac{v_y}{v_x}\\).</li>
</ul>
"""),
    image("M2-Bild", IMG["vektor"]),
    mc("M2-Vektor", "<p>a) Welche Größen sind Vektoren? (mehrere richtig)</p>",
       [("Geschwindigkeit", True, ""), ("Kraft", True, ""), ("Beschleunigung", True, ""),
        ("Masse", False, "Eine Masse hat keine Richtung."), ("Zeit", False, "Zeit hat keine Richtung im Raum."),
        ("Temperatur", False, "Temperatur ist ein Skalar.")],
       route("Fragen Sie sich jeweils: Ist es sinnvoll zu sagen, in welche Richtung die Größe zeigt?", "Richtig.")),
    blanks("M2-Zerlegen", "<p>b) Zerlegen Sie: \\(v=20\\,\\frac{\\text{m}}{\\text{s}}\\) unter \\(\\alpha=35^\\circ\\) zur Horizontalen. c) Setzen Sie zusammen: \\(v_x=6\\,\\frac{\\text{m}}{\\text{s}}\\), \\(v_y=8\\,\\frac{\\text{m}}{\\text{s}}\\).</p>",
           ["<p>b) v<sub>x</sub> ≈ *%s* m/s, v<sub>y</sub> ≈ *%s* m/s</p>" % (alt("16,38", "16,4", "16,383"), alt("11,47", "11,5", "11,472")),
            "<p>c) v = *%s:v = √(vx² + vy²)* m/s, α ≈ *%s:tan(α) = vy : vx* °</p>" % (alt("10", "10,0"), alt("53,13", "53,1", "53"))],
           route("Gehen Sie zuerst zum Abzweig H3.", "Richtig.")),
    mc("M2-Addition", "<p>d) Ein Boot fährt mit \\(4\\,\\frac{\\text{m}}{\\text{s}}\\) quer über einen Fluss, die Strömung treibt es mit \\(3\\,\\frac{\\text{m}}{\\text{s}}\\) flussabwärts. Wie schnell bewegt es sich gegenüber dem Ufer?</p>",
       [("\\(5\\,\\frac{\\text{m}}{\\text{s}}\\)", True, ""),
        ("\\(7\\,\\frac{\\text{m}}{\\text{s}}\\)", False, "Beträge darf man nur addieren, wenn die Vektoren in die gleiche Richtung zeigen."),
        ("\\(1\\,\\frac{\\text{m}}{\\text{s}}\\)", False, "Das wäre nur bei entgegengesetzter Richtung richtig.")],
       route("Zeichnen Sie die beiden Pfeile aneinander. Sie stehen senkrecht aufeinander.",
             "Richtig: Vektoren werden addiert, indem man die Pfeile aneinanderhängt. Weiter zu E1."), single=True)])

stage("H3", "H3 Hilfe Komponenten", ["M2", "E1"], [
    text("H3", """
<h3>H3 – Abzweig: Vektor zerlegen</h3>
<p>Der Vektorpfeil \\(\\vec v\\) ist die <strong>Hypotenuse</strong> eines rechtwinkligen Dreiecks. Die Komponente \\(v_x\\) ist die <strong>Ankathete</strong>, \\(v_y\\) die <strong>Gegenkathete</strong> von \\(\\alpha\\).</p>
<p>\\[ v_x=v\\cdot\\cos(\\alpha) \\qquad v_y=v\\cdot\\sin(\\alpha) \\qquad v=\\sqrt{v_x^2+v_y^2} \\qquad \\tan(\\alpha)=\\frac{v_y}{v_x} \\]</p>
<p><strong>Muster:</strong> \\(v=10\\,\\frac{\\text{m}}{\\text{s}}\\), \\(\\alpha=30^\\circ\\): \\(v_x=10\\cdot\\cos(30^\\circ)\\approx 8{,}66\\,\\frac{\\text{m}}{\\text{s}}\\), \\(v_y=10\\cdot\\sin(30^\\circ)=5\\,\\frac{\\text{m}}{\\text{s}}\\).</p>
"""),
    image("H3-Bild", IMG["vektor"]),
    blanks("H3-Aufgabe", "<p><strong>Parallelaufgabe:</strong> a) \\(v=10\\,\\frac{\\text{m}}{\\text{s}}\\), \\(\\alpha=60^\\circ\\). b) \\(v_x=5\\,\\frac{\\text{m}}{\\text{s}}\\), \\(v_y=12\\,\\frac{\\text{m}}{\\text{s}}\\).</p>",
           ["<p>a) v<sub>x</sub> = *%s* m/s, v<sub>y</sub> ≈ *%s* m/s</p>" % (alt("5", "5,0", "5,00"), alt("8,66", "8,7")),
            "<p>b) v = *%s* m/s</p>" % alt("13", "13,0")],
           route("Notieren Sie, wo Sie hängen, und gehen Sie weiter zu E1.", "Richtig. Weiter zu E1."))])

# ================================================================ Erarbeitung
stage("E1", "E1 Bewegungsgleichungen", ["M2", "H3", "E2"], [
    text("E1", """
<h3>E1 – Beschreibung des schiefen Wurfs</h3>
<p>Beim Kugelstoßen, beim Boule oder beim Basketball werden Gegenstände unter einem Abwurfwinkel \\(\\alpha\\) – also „schief“ – geworfen. Wir betrachten zunächst den vereinfachten Fall: Der Wurf beginnt und endet auf dem Boden, der Luftwiderstand wird vernachlässigt.</p>
<p>Der Wurf beginnt zum Zeitpunkt \\(t=0\\) im Ursprung mit der Geschwindigkeit \\(\\vec v_0\\) unter dem Winkel \\(\\alpha\\).</p>
"""),
    image("E1-Bild", IMG["bahn"]),
    dragtext("E1-Superposition", "<p>Ziehen Sie die passenden Begriffe in die Lücken.</p>\n",
             "Die Startgeschwindigkeit wird in eine *horizontale* und eine *vertikale* Komponente zerlegt: vx,0 = v0 · *cos(α)* und vy,0 = v0 · *sin(α)*.\n\n"
             "In x-Richtung ist die Bewegung *gleichförmig*, weil keine Kraft horizontal wirkt.\n\n"
             "In y-Richtung ist die Bewegung ein *senkrechter Wurf* nach oben mit der Anfangsgeschwindigkeit vy,0.\n\n"
             "Beide Bewegungen überlagern sich *unabhängig* voneinander (Superpositionsprinzip).\n\n"
             "Am Scheitelpunkt ist vy = *0*. Dort ist der Betrag der Geschwindigkeit am *kleinsten*.",
             route("Schauen Sie sich die Pfeile in der Grafik an: Welcher bleibt gleich, welcher ändert sich?", "Richtig."),
             distractors="*tan(α)* *gleichmäßig beschleunigt* *größten*"),
    text("E1-Merksatz", """
<p><strong>Merksatz:</strong> Die Bewegungsgleichungen für den schiefen Wurf ohne Reibung mit Abwurfwinkel \\(\\alpha\\) und Abwurfgeschwindigkeit \\(v_0\\) lauten</p>
<p>\\[ x(t)=v_0\\cdot\\cos(\\alpha)\\cdot t \\qquad (1) \\]</p>
<p>\\[ y(t)=-\\frac{1}{2}\\,g\\cdot t^2+v_0\\cdot\\sin(\\alpha)\\cdot t \\qquad (2) \\]</p>
<p>Die Bahnkurve ist eine nach unten geöffnete Parabel (Wurfparabel). Übertragen Sie den Merksatz in Ihr Heft.</p>
"""),
    mc("E1-Check", "<p>Welche Aussagen über die Geschwindigkeit während des Fluges stimmen? (mehrere richtig)</p>",
       [("\\(v_x\\) bleibt während des ganzen Fluges gleich.", True, ""),
        ("Am Scheitelpunkt ist \\(v_y=0\\).", True, ""),
        ("Am Scheitelpunkt ist die Geschwindigkeit \\(\\vec v=\\vec 0\\).", False, "Die Kugel bewegt sich dort weiter horizontal mit v_x."),
        ("Am Scheitelpunkt wirkt keine Fallbeschleunigung.", False, "Die Fallbeschleunigung g wirkt während des ganzen Fluges.")],
       route("Unterscheiden Sie zwischen den Komponenten und dem ganzen Vektor.", weiter("E2")))])

stage("E2", "E2 Versuch Boule", ["E1", "E3"], [
    text("E2", """
<h3>E2 – Versuch V1: Boule-Kugel</h3>
<p>Beim Boulespiel wird eine Metallkugel geworfen und von der Seite gefilmt. Mit einer Videoanalysesoftware wird die Position der Kugel in jedem Einzelbild bestimmt. Eine Regression der Daten bis \\(t=0{,}6\\,\\text{s}\\) liefert</p>
<p>\\[ x(t)=3{,}71\\cdot t \\qquad y(t)=-4{,}97\\,t^2+2{,}43\\,t+0{,}44 \\]</p>
<p>(alle Größen in m und s). Vergleichen Sie mit den Gleichungen (1) und (2). Beachten Sie: Die Kugel startet hier nicht auf dem Boden.</p>
"""),
    image("E2-Bild", IMG["boule"]),
    blanks("E2-Koeffizienten", "<p>Lesen Sie aus den Regressionsfunktionen ab bzw. berechnen Sie:</p>",
           ["<p>v<sub>x,0</sub> = *%s:Koeffizient von t in x(t)* m/s</p>" % alt("3,71", "3,7"),
            "<p>v<sub>y,0</sub> = *%s:Koeffizient von t in y(t)* m/s</p>" % alt("2,43", "2,4"),
            "<p>Abwurfhöhe y<sub>0</sub> = *%s* m</p>" % alt("0,44"),
            "<p>Fallbeschleunigung aus dem Versuch: g ≈ *%s:−4,97 entspricht −g : 2* m/s²</p>" % alt("9,94", "9,9"),
            "<p>Abwurfgeschwindigkeit v<sub>0</sub> ≈ *%s:Vektor aus den Komponenten zusammensetzen* m/s</p>" % alt("4,43", "4,44", "4,4", "4,435"),
            "<p>Abwurfwinkel α ≈ *%s:tan(α) = vy,0 : vx,0* °</p>" % alt("33,22", "33,2", "33,1", "33,3", "33")],
           route("Nutzen Sie die Tipps. Für v0 und α brauchen Sie M2.", "Richtig.")),
    mc("E2-Abweichung", "<p>Der Versuch liefert \\(g\\approx 9{,}94\\,\\frac{\\text{m}}{\\text{s}^2}\\) statt \\(9{,}81\\,\\frac{\\text{m}}{\\text{s}^2}\\). Welche Erklärungen sind plausibel? (mehrere richtig)</p>",
       [("Ungenauigkeiten beim Markieren der Kugel in den Videobildern", True, ""),
        ("Die Regression stützt sich nur auf wenige Messpunkte.", True, ""),
        ("Schwere Metallkugeln fallen schneller als leichte.", False, "Ohne Luftwiderstand fallen alle Körper gleich schnell."),
        ("Die Fallbeschleunigung ist beim Boule-Spielen größer.", False, "g hängt nicht von der Sportart ab.")],
       route("Denken Sie an Messfehler, nicht an neue Physik.", weiter("E3")))])

stage("E3", "E3 Wurfweite und Höhe", ["E2", "E4"], [
    dragtext("E3-Herleitung", """<h3>E3 – Wurfweite und maximale Wurfhöhe</h3>
<p>Abwurf und Landung liegen auf gleicher Höhe. Ergänzen Sie die Herleitung, indem Sie die passenden Bausteine in die Lücken ziehen.</p>
""", "Der Wurf endet zum Zeitpunkt tE, wenn die Kugel auf dem Boden auftrifft, also wenn *y(tE) = 0* gilt.\n\n"
         "Ausklammern liefert tE · (v0 · sin(α) − g/2 · tE) = 0. Die Lösung mit tE > 0 ist tE = *2 · v0 · sin(α) / g*.\n\n"
         "Setzt man tE in die Gleichung für *x(t)* ein, erhält man die Wurfweite w = 2 · v0² · cos(α) · sin(α) / g.\n\n"
         "Aus Symmetriegründen wird die maximale Höhe zur Zeit *tE / 2* erreicht.\n\n"
         "Wegen 2 · sin(α) · cos(α) = sin(2α) wird w am größten, wenn 2α = 90° ist, also für α = *45°*.",
         route("Gehen Sie die Schritte einzeln durch: Was bedeutet „Landung“ für y?", "Richtig."),
         distractors="*x(tE) = 0* *v0 · sin(α) / g* *90°*"),
    text("E3-Merksatz", """
<p><strong>Merksatz:</strong> Bei gleicher Abwurf- und Landehöhe gilt für die Wurfweite und die maximale Wurfhöhe</p>
<p>\\[ w=2\\,v_0^2\\cdot\\frac{\\cos(\\alpha)\\cdot\\sin(\\alpha)}{g} \\qquad h=\\frac{1}{2}\\cdot\\frac{(v_0\\cdot\\sin(\\alpha))^2}{g} \\]</p>
<p>Im Modell ist \\(\\alpha=45^\\circ\\) der beste Abwurfwinkel für die größte Wurfweite.</p>
"""),
    blanks("E3-Rechnen", "<p>Berechnen Sie für \\(v_0=10\\,\\frac{\\text{m}}{\\text{s}}\\) Wurfweite und maximale Wurfhöhe.</p>",
           ["<p>α = 45°: w ≈ *%s* m, h ≈ *%s* m</p>" % (alt("10,19", "10,2", "10,194"), alt("2,55", "2,5", "2,548", "2,6")),
            "<p>α = 30°: w ≈ *%s* m, h ≈ *%s* m</p>" % (alt("8,83", "8,8", "8,828"), alt("1,27", "1,3", "1,274")),
            "<p>α = 60°: w ≈ *%s* m, h ≈ *%s* m</p>" % (alt("8,83", "8,8", "8,828"), alt("3,82", "3,8", "3,823"))],
           route("Setzen Sie in die Formeln aus dem Merksatz ein. Taschenrechner im DEG-Modus?", "Richtig.")),
    mc("E3-Auffaellig", "<p>Was fällt beim Vergleich von 30° und 60° auf?</p>",
       [("Die Wurfweiten sind gleich, die Wurfhöhen verschieden.", True, ""),
        ("Bei 60° fliegt die Kugel doppelt so weit.", False, "Vergleichen Sie Ihre Ergebnisse."),
        ("Bei 60° ist die Wurfhöhe doppelt so groß wie bei 30°.", False, "Rechnen Sie nach: 3,82 m ist das Dreifache von 1,27 m.")],
       route("Vergleichen Sie Ihre Ergebnisse.",
             "Richtig: Winkel, die sich zu 90° ergänzen, liefern dieselbe Weite, weil sin(60°) = sin(120°). Weiter zu E4."), single=True)])

stage("E4", "E4 Starthöhe, Kugelstoß", ["E3", "A1"], [
    text("E4", """
<h3>E4 – Wurf mit Starthöhe: Kugelstoßen</h3>
<p>Würfe im Sport beginnen selten auf Bodenhöhe. Liegt der Startort bei \\((0\\,\\text{m}\\,|\\,y_0)\\), bleibt Gleichung (1) unverändert. Gleichung (2) wird zu</p>
<p>\\[ y(t)=-\\frac{g}{2}\\,t^2+v_0\\cdot\\sin(\\alpha)\\cdot t+y_0 \\]</p>
<p>Beim Kugelstoß ist \\(y_0\\approx 2\\,\\text{m}\\). Die Landung ist bei \\(y(t_E)=0\\). Dafür lösen Sie eine quadratische Gleichung (abc- oder pq-Formel) und nehmen die positive Lösung.</p>
"""),
    image("E4-Bild", IMG["kugelstoss"]),
    blanks("E4-Rechnen", "<p>Eine Kugel wird aus \\(2\\,\\text{m}\\) Höhe mit \\(v_0=8{,}5\\,\\frac{\\text{m}}{\\text{s}}\\) gestoßen.</p>",
           ["<p>α = 40°: v<sub>x,0</sub> ≈ *%s* m/s, v<sub>y,0</sub> ≈ *%s* m/s</p>" % (alt("6,51", "6,5", "6,511"), alt("5,46", "5,5", "5,464")),
            "<p>Flugzeit t<sub>E</sub> ≈ *%s:0 = −4,905 t² + 5,46 t + 2 lösen* s</p>" % alt("1,4", "1,40", "1,404", "1,41"),
            "<p>Stoßweite w ≈ *%s:w = vx,0 · tE* m</p>" % alt("9,14", "9,1", "9,143", "9,15", "9,13", "9,12", "9,18"),
            "<p>α = 45°: w ≈ *%s* m</p>" % alt("9", "9,0", "9,00", "9,01", "8,99", "9,02")],
           route("Gehen Sie schrittweise vor: Komponenten → Flugzeit aus y(tE) = 0 → Weite.", "Richtig.")),
    mc("E4-Fazit", "<p>Welche Schlussfolgerungen sind richtig? (mehrere richtig)</p>",
       [("Bei einer Starthöhe über dem Landeniveau liegt der optimale Winkel unter 45°.", True, ""),
        ("In der Nähe des optimalen Winkels ändert sich die Weite nur wenig.", True, ""),
        ("Der optimale Winkel ist immer 45°, egal wie hoch man abwirft.", False, "Das gilt nur bei gleicher Abwurf- und Landehöhe."),
        ("Verdoppelt man v0 (bei gleicher Höhe), verdoppelt sich die Wurfweite.", False, "w hängt von v0² ab: Die Weite vervierfacht sich.")],
       route("Vergleichen Sie Ihre Werte für 40° und 45° und schauen Sie in die Formel für w.",
             "Richtig. Das beantwortet die Leitfrage. Weiter zu den Beispielaufgaben (A1)."))])

# ================================================================ Beispielaufgaben mit Hilfen
stage("A1", "A1 Aufg. 1 Basketball", ["E4", "T1", "A2"], [blanks("A1", """
<h3>A1 – Aufgabe 1: Basketball</h3>
<p>Ein Basketball wird mit einer Anfangsgeschwindigkeit \\(v_0=7\\,\\frac{\\text{m}}{\\text{s}}\\) unter einem Winkel \\(\\alpha=56^\\circ\\) geworfen. Berechnen Sie die Wurfweite, wenn</p>
""", ["<p>a) der Ball vom Boden aus geworfen wird: w ≈ *%s:Gleiche Abwurf- und Landehöhe: Formel aus E3* m</p>" % alt("4,63", "4,6", "4,631", "4,64"),
      "<p>b) der Ball aus einer Höhe von 2 m über dem Boden geworfen wird: w ≈ *%s:Wie beim Kugelstoß in E4: y0 = 2 m, y(tE) = 0* m</p>" % alt("5,72", "5,7", "5,723", "5,73", "5,71")],
    route("Nutzen Sie den Abzweig T1 mit den Zwischenschritten.", weiter("A2")))])

stage("T1", "T1 Schritte Aufg. 1", ["A1", "A2"], [blanks("T1", """
<h3>T1 – Abzweig: Aufgabe 1 Schritt für Schritt</h3>
<p>\\(v_0=7\\,\\frac{\\text{m}}{\\text{s}}\\), \\(\\alpha=56^\\circ\\)</p>
""", ["<p>1. Komponenten: v<sub>x,0</sub> ≈ *%s:7 · cos(56°)* m/s, v<sub>y,0</sub> ≈ *%s:7 · sin(56°)* m/s</p>" % (alt("3,91", "3,9", "3,914"), alt("5,8", "5,80", "5,803")),
      "<p><strong>a)</strong> 2. Flugzeit t<sub>E</sub> = 2 · v<sub>y,0</sub> : g ≈ *%s* s</p>" % alt("1,18", "1,2", "1,183"),
      "<p>3. Wurfweite w = v<sub>x,0</sub> · t<sub>E</sub> ≈ *%s* m</p>" % alt("4,63", "4,6", "4,631", "4,62", "4,64"),
      "<p><strong>b)</strong> 2. Ansatz: 0 = −4,905 · t² + 5,80 · t + 2. Positive Lösung: t<sub>E</sub> ≈ *%s:abc-Formel mit a = −4,905; b = 5,80; c = 2* s</p>" % alt("1,46", "1,5", "1,462"),
      "<p>3. Wurfweite w = v<sub>x,0</sub> · t<sub>E</sub> ≈ *%s* m</p>" % alt("5,72", "5,7", "5,723", "5,71", "5,73")],
    route("Notieren Sie, bei welchem Schritt Sie hängen, und fragen Sie nach. Weiter zu A2.",
          "Richtig. Rechnen Sie Aufgabe 1 in A1 noch einmal ein, dann weiter zu A2."))])

TABELLE = """<table border="1" cellpadding="5" style="border-collapse:collapse;text-align:center">
<tr><th>x in m</th><td>0,00</td><td>0,30</td><td>0,71</td><td>1,18</td><td>1,72</td><td>2,28</td><td>2,88</td></tr>
<tr><th>y in m</th><td>2,02</td><td>2,53</td><td>2,92</td><td>3,26</td><td>3,48</td><td>3,50</td><td>3,34</td></tr></table>"""

stage("A2", "A2 Aufg. 2 Messwerte", ["A1", "T1", "T2", "A3"], [
    text("A2", f"""
<h3>A2 – Aufgabe 2: Ist das ein schiefer Wurf?</h3>
<p>Die Tabelle zeigt Positionen eines Basketballs.</p>
{TABELLE}
<p>Zeichnen Sie ein \\(y(x)\\)-Diagramm (im Heft oder mit GeoGebra) und prüfen Sie, ob es sich um einen schiefen Wurf ohne Luftreibung handeln könnte.</p>
<p><strong>Idee:</strong> Ohne Reibung ist die Bahnkurve eine Parabel \\(y=a\\,x^2+b\\,x+c\\) mit \\(a&lt;0\\). Führen Sie eine quadratische Regression durch und prüfen Sie, wie gut die Punkte passen.</p>
"""),
    blanks("A2-Regression", "<p>Ergebnis der quadratischen Regression (auf zwei Nachkommastellen):</p>",
           ["<p>a ≈ *%s:GeoGebra: TrendPoly(Liste der Punkte, 2)* m⁻¹</p>" % alt("-0,34", "−0,34", "-0,339"),
            "<p>b ≈ *%s*</p>" % alt("1,41", "1,4", "1,409"),
            "<p>c ≈ *%s* m</p>" % alt("2,07", "2,08", "2,075", "2,1")],
           route("Gehen Sie zum Abzweig T2.", "Richtig.")),
    mc("A2-Urteil", "<p>Könnte es sich um einen schiefen Wurf ohne Luftreibung handeln?</p>",
       [("Ja: Die Messpunkte liegen sehr gut auf einer nach unten geöffneten Parabel (Abweichungen höchstens etwa 6 cm).", True, ""),
        ("Nein, weil der Ball nicht auf dem Boden startet.", False, "Auch ein Wurf mit Starthöhe ist ein schiefer Wurf."),
        ("Nein, weil die Punkte nicht symmetrisch zum Scheitelpunkt liegen.", False,
         "Die Messung endet kurz nach dem Scheitelpunkt. Symmetrie können Sie daran nicht prüfen.")],
       route("Gehen Sie zum Abzweig T2.", "Richtig.")),
    blanks("A2-Zusatz", "<p><strong>Für Schnelle:</strong> Bestimmen Sie aus der Regression Abwurfwinkel und Abwurfgeschwindigkeit. (Tipp: Bahngleichung in T2.)</p>",
           ["<p>α ≈ *%s:b = tan(α)* °</p>" % alt("54,64", "54,6", "54,7", "55", "54,5"),
            "<p>v<sub>0</sub> ≈ *%s:a = −g : (2 · v0² · cos²(α))* m/s</p>" % alt("6,57", "6,6", "6,56", "6,58", "6,55", "6,5")],
           route("Nutzen Sie die Bahngleichung aus dem Abzweig T2.", weiter("A3")))])

stage("T2", "T2 Hilfe Bahnkurve", ["A2", "A3"], [
    text("T2", """
<h3>T2 – Abzweig: Die Bahnkurve y(x)</h3>
<p>Aus Gleichung (1) folgt \\(t=\\dfrac{x}{v_0\\cdot\\cos(\\alpha)}\\). Eingesetzt in \\(y(t)=-\\frac{g}{2}t^2+v_0\\sin(\\alpha)\\,t+y_0\\) ergibt sich die <strong>Bahngleichung</strong></p>
<p>\\[ y(x)=-\\frac{g}{2\\,v_0^2\\cos^2(\\alpha)}\\,x^2+\\tan(\\alpha)\\cdot x+y_0 \\]</p>
<p>Das ist eine quadratische Funktion \\(y=a\\,x^2+b\\,x+c\\) mit \\(a=-\\frac{g}{2v_0^2\\cos^2(\\alpha)}\\), \\(b=\\tan(\\alpha)\\), \\(c=y_0\\). Die Bahn ist also eine nach unten geöffnete Parabel.</p>
<p><strong>Regression mit GeoGebra:</strong> Geben Sie in die Eingabezeile ein:</p>
<p><code>TrendPoly({(0, 2.02), (0.3, 2.53), (0.71, 2.92), (1.18, 3.26), (1.72, 3.48), (2.28, 3.5), (2.88, 3.34)}, 2)</code></p>
<p>Mit dem Taschenrechner: Statistik-Modus, Regression „quadratisch“ (QuadReg).</p>
<p><strong>Prüfen:</strong> Zeichnen Sie Punkte und Parabel gemeinsam. Liegen alle Punkte nahe an der Kurve, ist das Modell „schiefer Wurf ohne Reibung“ plausibel.</p>
"""),
    blanks("T2-Aufgabe", "<p>Die Regression liefert \\(y=-0{,}34\\,x^2+1{,}41\\,x+2{,}07\\). Lesen Sie ab bzw. berechnen Sie:</p>",
           ["<p>Abwurfhöhe y<sub>0</sub> ≈ *%s* m</p>" % alt("2,07", "2,1"),
            "<p>α ≈ *%s:tan⁻¹(1,41)* °</p>" % alt("54,64", "54,6", "54,7", "55")],
           route("Fragen Sie nach und gehen Sie weiter zu A3.", "Richtig. Lösen Sie jetzt A2 fertig, dann weiter zu A3."))])

stage("A3", "A3 Aufg. 3 Weitsprung", ["A2", "T2", "T3", "X1", "Ziel"], [
    text("A3", """
<h3>A3 – Aufgabe 3: Versteckte Würfe – Weitsprung</h3>
<p>Beim Weitsprung folgt der Körperschwerpunkt einer Wurfparabel. Sie beginnt etwa \\(0{,}9\\,\\text{m}\\) über dem Boden, wenn sich der hintere Fuß löst, und endet etwa \\(0{,}5\\,\\text{m}\\) über dem Boden, wenn die Füße den Boden berühren.</p>
<p>Schätzen Sie die Sprungweite grob ab. Nehmen Sie an, dass der Springer unter \\(25^\\circ\\) mit \\(10\\,\\frac{\\text{m}}{\\text{s}}\\) abspringt. Die Abstände \\(d_1\\) und \\(d_2\\) vor und nach dem „Wurf“ betragen etwa \\(0{,}6\\,\\text{m}\\) und \\(0{,}75\\,\\text{m}\\).</p>
"""),
    image("A3-Bild", IMG["weitsprung"]),
    blanks("A3-Rechnen", "<p>Rechnen Sie:</p>",
           ["<p>v<sub>x,0</sub> ≈ *%s* m/s, v<sub>y,0</sub> ≈ *%s* m/s</p>" % (alt("9,06", "9,1", "9,063"), alt("4,23", "4,2", "4,226")),
            "<p>Flugzeit t<sub>E</sub> ≈ *%s:Landung bei y = 0,5 m, Start bei y0 = 0,9 m* s</p>" % alt("0,95", "0,9", "0,948", "0,947"),
            "<p>horizontale Flugstrecke ≈ *%s* m</p>" % alt("8,59", "8,6", "8,589", "8,61", "8,58"),
            "<p>Sprungweite d<sub>1</sub> + Flugstrecke + d<sub>2</sub> ≈ *%s* m</p>" % alt("9,94", "9,9", "9,939", "9,96", "9,93", "10")],
           route("Gehen Sie zum Abzweig T3.", "Richtig.")),
    mc("A3-Bewerten", "<p>Der Weltrekord im Weitsprung liegt bei \\(8{,}95\\,\\text{m}\\). Wie bewerten Sie Ihr Ergebnis?</p>",
       [("Die Schätzung ist zu groß. Die angenommene Absprunggeschwindigkeit von 10 m/s ist für einen Springer sehr hoch, das Modell ist grob.", True, ""),
        ("Die Rechnung muss falsch sein, weil das Modell des schiefen Wurfs hier nicht gilt.", False,
         "Das Modell gilt für den Schwerpunkt gut. Prüfen Sie die Annahmen."),
        ("Das Ergebnis ist realistisch für Hobbysportler.", False, "Hobbysportler springen meist 4–6 m weit.")],
       route("Vergleichen Sie Ihr Ergebnis mit dem Weltrekord.",
             "Richtig. Gehen Sie zum Ziel oder wählen Sie eine Vertiefung X1–X3."), single=True)])

stage("T3", "T3 Schritte Aufg. 3", ["A3", "Ziel"], [blanks("T3", """
<h3>T3 – Abzweig: Aufgabe 3 Schritt für Schritt</h3>
<p>Koordinatensystem: Der Schwerpunkt startet bei \\((0\\,|\\,0{,}9\\,\\text{m})\\). Die Landung ist erreicht, wenn \\(y(t_E)=0{,}5\\,\\text{m}\\).</p>
<p>\\[ 0{,}5=-4{,}905\\,t_E^2+4{,}23\\,t_E+0{,}9 \\;\\Longleftrightarrow\\; 0=-4{,}905\\,t_E^2+4{,}23\\,t_E+0{,}4 \\]</p>
""", ["<p>1. v<sub>x,0</sub> = 10 · cos(25°) ≈ *%s* m/s, v<sub>y,0</sub> = 10 · sin(25°) ≈ *%s* m/s</p>" % (alt("9,06", "9,1"), alt("4,23", "4,2")),
      "<p>2. positive Lösung der quadratischen Gleichung: t<sub>E</sub> ≈ *%s* s</p>" % alt("0,95", "0,948", "0,947"),
      "<p>3. Flugstrecke x = v<sub>x,0</sub> · t<sub>E</sub> ≈ *%s* m</p>" % alt("8,59", "8,6", "8,61", "8,58"),
      "<p>4. Sprungweite = 0,6 m + Flugstrecke + 0,75 m ≈ *%s* m</p>" % alt("9,94", "9,9", "9,96", "9,93", "10")],
    route("Fragen Sie nach. Danach geht es zum Ziel.", "Richtig. Lösen Sie A3 fertig, dann zum Ziel oder zu X1–X3."))])

# ================================================================ Vertiefung (optional)
stage("X1", "X1 Blasrohr", ["A3", "X2"], [
    text("X1", """
<h3>X1 – Vertiefung: Aufgabe 4 (Blasrohr und Dose)</h3>
<p>Mit einem Blasrohr wird genau auf eine Dose gezielt, die von einer Hand gehalten wird. Die Abschussgeschwindigkeit kann bei jedem Schuss variieren.</p>
<p>a) Beschreiben Sie im Heft die Bewegungen des Kügelchens und der Dose.</p>
"""),
    image("X1-Bild", IMG["blasrohr"]),
    mc("X1-b", "<p>b) Wann muss die Dose losgelassen werden, damit sie getroffen wird?</p>",
       [("Genau im Moment des Abschusses", True, ""),
        ("Etwas vor dem Abschuss, damit sie schon fällt", False, "Dann ist die Dose immer tiefer als das Kügelchen."),
        ("Je nach Abschussgeschwindigkeit etwas später", False, "Die Regel hängt nicht von der Geschwindigkeit ab.")],
       route("Vergleichen Sie, um wie viel beide in der Zeit t unter die Ziellinie fallen.",
             "Richtig: Ohne Schwerkraft flöge das Kügelchen geradlinig zur Dose. Mit Schwerkraft fallen Kügelchen und Dose in derselben Zeit um dieselbe Strecke g/2 · t² unter diese Linie – unabhängig von v0."), single=True),
    text("X1-c", "<p>c) Formulieren Sie die Begründung zu b) im Heft mit den Bewegungsgleichungen. Wenn möglich: Probieren Sie es in einer Kleingruppe aus.</p>")])

stage("X2", "X2 Waagerechter Wurf", ["X1", "X3"], [
    mc("X2", """<h3>X2 – Vertiefung: Aufgabe 6</h3>
<p>Untersuchen Sie, ob die Bahnkurve eines waagerechten Wurfs ebenfalls eine Wurfparabel ist. Setzen Sie dazu \\(\\alpha=0^\\circ\\) und die Abwurfhöhe \\(h\\) in die Bahngleichung des schiefen Wurfs ein.</p>
<p>Welche Bahngleichung erhalten Sie?</p>""",
       [("\\(y(x)=h-\\dfrac{g}{2\\,v_0^2}\\,x^2\\)", True, ""),
        ("\\(y(x)=h-\\dfrac{g}{2}\\,x^2\\)", False, "Beim Einsetzen von t = x : v0 bleibt v0² im Nenner."),
        ("\\(y(x)=h-\\dfrac{g}{v_0}\\,x\\)", False, "Das wäre eine Gerade.")],
       route("Mit α = 0° gilt cos(α) = 1 und tan(α) = 0.",
             "Richtig: Auch der waagerechte Wurf ist eine Wurfparabel – ein Spezialfall des schiefen Wurfs."), single=True),
    blanks("X2-Zahl", "<p>Prüfen Sie mit D1a): \\(h=1{,}25\\,\\text{m}\\), \\(v_0=4\\,\\frac{\\text{m}}{\\text{s}}\\). In welcher Höhe ist die Kugel nach \\(x=1\\,\\text{m}\\)?</p>",
           ["<p>y(1 m) ≈ *%s* m</p>" % alt("0,94", "0,943", "0,9")],
           route("Setzen Sie in die Bahngleichung ein.", "Richtig."))])

stage("X3", "X3 Knobelaufgabe", ["X2", "Ziel"], [blanks("X3", """
<h3>X3 – Vertiefung: Knobelaufgaben</h3>
<p>Abwurf- und Landehöhe sind gleich.</p>
<p>a) Bei welchem Abwurfwinkel sind Wurfweite \\(w\\) und maximale Wurfhöhe \\(h\\) gleich groß? Setzen Sie die Formeln gleich und vereinfachen Sie.</p>
""", ["<p>tan(α) = *4:Teilen Sie beide Seiten durch cos(α) · sin(α) · v0² : g*</p>",
      "<p>α ≈ *%s* °</p>" % alt("75,96", "76", "75,9", "76,0"),
      "<p>b) Ein Ball soll mit v<sub>0</sub> = 10 m/s genau 8 m weit fliegen. Es gibt zwei mögliche Winkel:</p>",
      "<p>flacher Wurf: α ≈ *%s:sin(2α) = w · g : v0²* °</p>" % alt("25,86", "25,9", "26"),
      "<p>steiler Wurf: α ≈ *%s:Die Winkel ergänzen sich zu 90°.* °</p>" % alt("64,14", "64,1", "64")],
    route("Nutzen Sie die Tipps.", "Richtig. Weiter zum Ziel."))])

stage("Ziel", "Ziel", ["A3", "T3", "X3"], [{}], special="finish")

# ================================================================ Zusammenbau
index = {s["key"]: i for i, s in enumerate(S)}
for s in S:
    for n in s["nb"]:
        assert s["key"] in S[index[n]]["nb"], (s["key"], n)

W_PCT, H_PCT = 3.6, 5.76
elements, paths = [], []
for i, s in enumerate(S):
    cx, cy = POS[s["key"]]
    el = {
        "id": "wurf-" + s["key"].lower(),
        "label": s["label"],
        "telemetry": {"x": str(round(cx / 16 - W_PCT / 2, 3)), "y": str(round(cy / 10 - H_PCT / 2, 3)),
                      "width": str(W_PCT), "height": str(H_PCT)},
        "neighbors": [str(index[n]) for n in s["nb"]],
        "canBeStartStage": s["start"],
        "time": {},
        "accessRestrictions": {"allOrAnyRestrictionSet": "all", "restrictionSetList": []},
        "contentsList": s["contents"],
        "specialStageExtraLives": 1,
        "specialStageExtraTime": 1,
        "specialStageLinkTarget": "_blank",
        "alwaysVisible": False,
        "overrideSymbol": False,
    }
    if s["special"]:
        el["specialStageType"] = s["special"]
    elements.append(el)
    for n in s["nb"]:
        j = index[n]
        if i < j:
            paths.append({"from": i, "to": j, "visualsType": "global",
                          "customVisuals": {"colorPath": "rgba(200, 220, 240, 0.8)", "pathWidth": "0.2",
                                            "pathStyle": "dotted"}})

with open(os.path.join(HERE, "bilder", "etappen.json"), "w", encoding="utf-8") as f:
    json.dump([{"code": s["key"], "cx": POS[s["key"]][0], "cy": POS[s["key"]][1], "ldx": LAB[s["key"]][0],
                "ldy": LAB[s["key"]][1], "nb": [index[n] for n in s["nb"]], "finish": s["special"] == "finish"}
               for s in S], f, ensure_ascii=False, indent=1)

ref = json.load(open(os.path.join(REF, "content", "content.json"), encoding="utf-8"))
END = """<p style="text-align: center;"><strong>Leitfrage:</strong> Unter welchem Winkel sollte eine Kugelstoßerin stoßen – und warum sind das nicht 45°?</p>
<p style="text-align: center;">Beantworten Sie die Leitfrage im Heft in höchstens vier Sätzen. Verwenden Sie die Begriffe Komponente, Starthöhe und Wurfweite.</p>
<p style="text-align: center;"><strong>Hausaufgabe (Aufg. 5):</strong> Filmen Sie einen eigenen Wurf mit dem Smartphone und werten Sie ihn mit einer Videoanalyse-App aus.</p>
"""
visual = json.loads(json.dumps(ref["visual"]))
visual["stages"].update({"colorStage": "rgba(214, 228, 244, 0.92)", "colorStageCleared": "rgba(46, 170, 120, 0.92)",
                         "colorStageLocked": "rgba(153, 0, 0, 0.7)"})
visual["paths"]["style"].update({"colorPath": "rgba(200, 220, 240, 0.8)", "colorPathCleared": "rgba(46, 170, 120, 0.9)"})
hintergrund = "karte-beschriftet.jpg" if os.path.exists(os.path.join(HERE, "bilder", "karte-beschriftet.jpg")) else "karte.jpg"
content = {
    "showTitleScreen": False,
    "titleScreen": {"titleScreenIntroduction": "<p style=\"text-align: center;\"></p>"},
    "headline": "Der schiefe Wurf",
    "gamemapSteps": {
        "backgroundImageSettings": {
            "backgroundColor": "rgb(20, 39, 61)",
            "backgroundImage": {"path": "images/" + hintergrund, "mime": "image/jpeg",
                                "copyright": {"license": "U"}, "width": 1600, "height": 1000}},
        "gamemap": {"elements": elements, "paths": paths},
    },
    "endScreen": {
        "noSuccess": {"endScreenTextNoSuccess": END},
        "success": {"endScreenTextSuccess": END},
        "overallFeedback": [{"from": 0, "to": 100}],
    },
    "visual": visual,
    "audio": ref["audio"],
    "behaviour": {"enableRetry": True, "enableSolutionsButton": False,
                  "map": {"showLabels": True, "roaming": "free"}},
    "l10n": ref["l10n"],
    "a11y": ref["a11y"],
}
content["l10n"]["restrictionStageProgressIs"] = "Der Fortschritt von Etappe @label ist @value."
content["l10n"]["restrictionStageProgressIsNot"] = "Der Fortschritt von Etappe @label ist nicht @value."

h5p = json.load(open(os.path.join(REF, "h5p.json"), encoding="utf-8"))
h5p["title"] = "Der schiefe Wurf – Lernpfad"
h5p["language"] = "de"
h5p["license"] = "U"

bilder = [hintergrund] + [p.split("/")[1] for p, *_ in IMG.values()]
if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("h5p.json", json.dumps(h5p, ensure_ascii=False))
    z.writestr("content/content.json", json.dumps(content, ensure_ascii=False))
    for name in bilder:
        z.write(os.path.join(HERE, "bilder", name), "content/images/" + name)
    for d in sorted(os.listdir(REF)):
        full = os.path.join(REF, d)
        if not os.path.isdir(full) or d == "content":
            continue
        for root, _, files in os.walk(full):
            for f in files:
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, REF))
print("geschrieben:", OUT, "Etappen:", len(elements), "Wege:", len(paths), "Hintergrund:", hintergrund)
