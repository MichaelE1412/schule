#!/usr/bin/env python3
"""Baut „Der schiefe Wurf – Herleitung“ (Physik Klasse 11) als H5P Game Map.

Aufruf:  python3 build.py <entpackte Trapez-Referenz> <Ausgabe.h5p>

Inhalte: Grundlagen der Mechanik S. 10–11 (Vektoren, Wiederholung) und S. 26–29
(Der schiefe Wurf, ohne Exkurse), Herleitungspuzzle zum schiefen Wurf, Aufgabe 1.
"""
import json
import os
import sys
import zipfile

from bausteine import alt, dragtext, image, mc, route, text, blanks

HERE = os.path.dirname(os.path.abspath(__file__))
REF, OUT = sys.argv[1], sys.argv[2]

IMG = {
    "bahnkurven": ("images/bahnkurven.png", 1260, 500, "Drei Bahnkurven im x-y-Koordinatensystem: 1 parallel zur Rechtsachse, 2 geradlinig unter dem Winkel α, 3 gekrümmt"),
    "schwimmer": ("images/schwimmer.png", 1000, 470, "Schwimmer im Fluss von oben: Eigengeschwindigkeit quer zum Fluss, Strömung, resultierende Geschwindigkeit"),
    "vektor": ("images/vektor.png", 1140, 420, "Geschwindigkeitsvektor mit Winkel α und den Komponenten v_x = v·cos(α) und v_y = v·sin(α)"),
    "dreieck": ("images/dreieck.png", 1040, 400, "Rechtwinkliges Dreieck mit Hypotenuse, Ankathete und Gegenkathete von α"),
    "bahn": ("images/bahn.png", 1000, 440, "Bahn beim schiefen Wurf mit Geschwindigkeitsvektor und Komponenten an vier Stellen"),
    "boule": ("images/boule.png", 1240, 650, "Versuch V1: Messwerte und Regressionskurven x(t) und y(t) der Boule-Kugel"),
    "kugelstoss": ("images/kugelstoss.png", 1140, 420, "Wurfbahnen beim Kugelstoß für 20°, 40° und 60° bei 2 m Starthöhe und 8,5 m/s"),
}

# Mittelpunkt (Pixel auf 1600 × 1000) und Lage des Schildes relativ zum Punkt
UNTEN, OBEN = (0, 56), (0, -56)
POS = {
    "Start": ((90, 880), UNTEN), "V1": ((320, 880), UNTEN), "V2": ((550, 880), UNTEN), "HV": ((665, 760), OBEN),
    "V3": ((780, 880), UNTEN), "V4": ((1010, 880), UNTEN), "HS": ((1290, 880), UNTEN),
    "T1": ((1420, 640), UNTEN), "T2": ((1160, 600), UNTEN), "T3": ((900, 600), UNTEN), "T4": ((640, 600), UNTEN),
    "P1": ((230, 420), UNTEN), "P2": ((470, 330), UNTEN), "HP": ((605, 190), OBEN), "P3": ((740, 330), UNTEN),
    "P4": ((1010, 330), UNTEN), "A1": ((1250, 330), UNTEN), "HA": ((1365, 460), UNTEN), "A2": ((1480, 330), UNTEN),
    "Ziel": ((1480, 120), (-84, 0)),
}

S = []


def stage(key, label, neighbors, contents, start=False, special=None):
    S.append(dict(key=key, label=label, nb=neighbors, contents=contents, start=start, special=special))


def weiter(ziel):
    return f"Richtig. Weiter zu {ziel}."


MS = "\\(\\frac{\\text{m}}{\\text{s}}\\)"
M = "\\(\\text{m}\\)"
SEK = "\\(\\text{s}\\)"
GRAD = "\\(^\\circ\\)"

# ================================================================ Start
stage("Start", "Start", ["V1"], [text("Start", """
<h2>Der schiefe Wurf – Herleitung und Anwendung</h2>
<p><strong>Leitfrage:</strong> Wie weit fliegt ein schräg geworfener Ball – und unter welchem Winkel fliegt er am weitesten?</p>
<p><strong>Ihr Weg durch die Karte</strong></p>
<ol>
<li><strong>A · Vektoren</strong> (V1–V4): Wiederholung zu Koordinaten, Vektoren und Geschwindigkeitskomponenten (Buch S. 10–11). Wer Vektoren noch nicht kennt, nimmt sich hier Zeit.</li>
<li><strong>B · Fragen zum Text</strong> (T1–T4): Lesen Sie Buch S. 26–28 abschnittsweise und beantworten Sie die Fragen. Die Exkurse lassen Sie aus.</li>
<li><strong>C · Herleitungspuzzle</strong> (P1–P4): Legen Sie das Puzzle auf dem Arbeitsblatt. Die Etappen prüfen Ihre Lösung Schritt für Schritt.</li>
<li><strong>D · Aufgabe 1</strong> (A1, A2): Basketballwurf von S. 29.</li>
</ol>
<p>Etappen, die mit <strong>H</strong> beginnen (HV, HS, HP, HA), sind <strong>Hilfen</strong>. Gehen Sie dorthin, wenn eine Rückmeldung Sie hinschickt oder wenn Sie nicht weiterkommen.</p>
<p><strong>Hinweise zur Eingabe</strong></p>
<ul>
<li>Verwenden Sie das Dezimalkomma, z. B. <code>4,63</code>. Runden Sie auf zwei Nachkommastellen, wenn nichts anderes angegeben ist.</li>
<li>Die Einheit steht immer schon hinter dem Eingabefeld. Tippen Sie nur die Zahl ein.</li>
<li>Das Symbol <strong>ⓘ</strong> im Eingabefeld zeigt einen Tipp.</li>
<li>Rechnen Sie mit \\(g=9{,}81\\,\\frac{\\text{m}}{\\text{s}^2}\\). Stellen Sie den Taschenrechner auf Gradmaß (DEG).</li>
</ul>
""")], start=True)

# ================================================================ A · Vektoren
stage("V1", "V1 Koordinaten", ["Start", "V2"], [
    text("V1", """
<h3>V1 – Koordinaten und Bahnkurven (Buch S. 10)</h3>
<p>Lesen Sie den Abschnitt <em>Richtungen und Koordinatensysteme</em>.</p>
"""),
    image("V1-Bild", IMG["bahnkurven"]),
    dragtext("V1-Begriffe", "<p>a) Ziehen Sie die passenden Begriffe in die Lücken.</p>\n",
             "Die horizontale Achse heißt Rechtsachse oder *Abszisse*, die vertikale Achse heißt Hochachse oder *Ordinate*.\n\n"
             "Trägt man die horizontale gegen die vertikale Bewegung auf, erhält man die *Bahnkurve*.\n\n"
             "Die Bahnkurve zeigt, wo sich ein Körper befand – aber nicht, *wann* er dort war.",
             route("Die Begriffe stehen im ersten Absatz auf S. 10.", "Richtig."),
             distractors="*Zeitachse* *wie schnell*"),
    blanks("V1-Weg", "<p>b) Bewegung 1 verläuft von \\(x=-7{,}5\\,\\text{m}\\) bis \\(x=15\\,\\text{m}\\). Berechnen Sie den zurückgelegten Weg.</p>",
           ["<p>\\(\\Delta s\\) = *%s:Δs = Endkoordinate minus Anfangskoordinate. Achten Sie auf das Minuszeichen.* %s</p>" % (alt("22,5"), M)],
           route("Δs = 15 m − (−7,5 m). Minus mal minus ergibt plus.", "Richtig.")),
    mc("V1-Winkel", "<p>c) Bei welcher Bewegung ändert sich der Richtungswinkel \\(\\alpha\\) zwischen Rechtsachse und Bewegungsrichtung ständig?</p>",
       [("Bewegung 3", True, ""),
        ("Bewegung 2", False, "Bewegung 2 ist geradlinig. Ihr Winkel α bleibt gleich."),
        ("Bewegung 1", False, "Bewegung 1 verläuft immer parallel zur Rechtsachse.")],
       route("Bei welcher Bahn zeigt die Bewegung an jeder Stelle in eine andere Richtung?", weiter("V2")), single=True)])

stage("V2", "V2 Vektoren", ["V1", "HV", "V3"], [
    text("V2", """
<h3>V2 – Geschwindigkeiten sind Vektoren (Buch S. 10)</h3>
<p>Lesen Sie den Abschnitt <em>Geschwindigkeiten und Bezugssysteme</em> mit den beiden Gedankenexperimenten.</p>
<p><strong>Kurz erklärt:</strong> Eine Geschwindigkeit hat einen <strong>Betrag</strong> (wie schnell) und eine <strong>Richtung</strong> (wohin). Solche Größen heißen <strong>Vektoren</strong>. Man zeichnet sie als Pfeil und schreibt einen Pfeil über das Formelzeichen: \\(\\vec v\\). Der Betrag ist die Länge des Pfeils: \\(|\\vec v|=v\\). Größen ohne Richtung, z. B. Masse oder Zeit, heißen <strong>Skalare</strong>.</p>
"""),
    image("V2-Bild", IMG["schwimmer"]),
    mc("V2-Beobachter", "<p>a) Gedankenexperiment 1: Welche Geschwindigkeit misst Beobachter 3, der die Szene von oben betrachtet?</p>",
       [("die Summe \\(\\vec v=\\vec v_x+\\vec v_y\\)", True, ""),
        ("nur \\(\\vec v_x\\)", False, "Das misst Beobachter 1 am Ufer."),
        ("nur \\(\\vec v_y\\)", False, "Das misst Beobachter 2."),
        ("die Differenz \\(\\vec v_x-\\vec v_y\\)", False, "Die Strömung schiebt den Schwimmer zusätzlich – die Geschwindigkeiten addieren sich.")],
       route("Beobachter 3 sieht beide Bewegungen gleichzeitig.", "Richtig."), single=True),
    mc("V2-Pythagoras", "<p>b) Wann darf man den Betrag mit \\(v=\\sqrt{v_x^2+v_y^2}\\) berechnen?</p>",
       [("nur wenn \\(\\vec v_x\\) und \\(\\vec v_y\\) senkrecht aufeinander stehen", True, ""),
        ("immer, wenn man zwei Geschwindigkeiten addiert", False, "Der Satz des Pythagoras gilt nur im rechtwinkligen Dreieck."),
        ("nur wenn beide Geschwindigkeiten gleich groß sind", False, "Die Beträge dürfen verschieden sein.")],
       route("Lesen Sie den Satz, der mit „Achtung“ beginnt.", "Richtig."), single=True),
    mc("V2-Skalar", "<p>c) Welche Größen sind Vektoren? (mehrere richtig)</p>",
       [("Geschwindigkeit", True, ""), ("Beschleunigung", True, ""), ("Kraft", True, ""),
        ("Masse", False, "Eine Masse zeigt in keine Richtung."), ("Zeit", False, "Zeit hat keine Richtung im Raum.")],
       route("Fragen Sie sich: Kann man sinnvoll sagen, in welche Richtung die Größe zeigt?", "Richtig.")),
    dragtext("V2-Bezugssystem", "<p>d) Gedankenexperiment 2: Ziehen Sie die passenden Begriffe in die Lücken.</p>\n",
             "Ein vierter Beobachter läuft am Ufer mit derselben Geschwindigkeit in die gleiche Richtung wie der Schwimmer. Für ihn bewegt sich der Schwimmer *nicht*.\n\n"
             "Jeder Beobachter befindet sich in seinem eigenen *Bezugssystem*. Welche Geschwindigkeit man misst, hängt vom *Standort* des Beobachters ab.",
             route("Die Begriffe stehen am Ende von S. 10.", "Richtig. Weiter zu V3."),
             distractors="*schneller* *Koordinatenursprung*")])

stage("HV", "HV Hilfe Vektoren", ["V2", "V3"], [
    text("HV", """
<h3>HV – Hilfe: Vektoren addieren</h3>
<ul>
<li>Ein <strong>Vektor</strong> ist ein Pfeil mit Betrag (Länge) und Richtung.</li>
<li><strong>Addition:</strong> Man hängt die Pfeile aneinander (Fuß an Spitze). Der Summenvektor zeigt vom Anfang des ersten zur Spitze des letzten Pfeils.</li>
<li>Zeigen beide Pfeile in die <strong>gleiche</strong> Richtung, addiert man einfach die Beträge: \\(3\\,\\frac{\\text{m}}{\\text{s}}+4\\,\\frac{\\text{m}}{\\text{s}}=7\\,\\frac{\\text{m}}{\\text{s}}\\).</li>
<li>Stehen beide Pfeile <strong>senkrecht</strong> aufeinander, bilden sie mit dem Summenpfeil ein rechtwinkliges Dreieck: \\(v=\\sqrt{v_x^2+v_y^2}=\\sqrt{3^2+4^2}\\,\\frac{\\text{m}}{\\text{s}}=5\\,\\frac{\\text{m}}{\\text{s}}\\).</li>
</ul>
"""),
    image("HV-Bild", IMG["schwimmer"]),
    blanks("HV-Aufgabe", "<p><strong>Übung:</strong> Ein Schwimmer schwimmt mit \\(0{,}8\\,\\frac{\\text{m}}{\\text{s}}\\) quer über einen Fluss. Die Strömung hat \\(0{,}6\\,\\frac{\\text{m}}{\\text{s}}\\).</p>",
           ["<p>Betrag der Gesamtgeschwindigkeit: \\(v\\) = *%s:v = √(0,8² + 0,6²)* %s</p>" % (alt("1", "1,0", "1,00"), MS)],
           route("Quadrieren, addieren, Wurzel ziehen. Fragen Sie nach, wenn es nicht klappt.", "Richtig. Weiter zu V3."))])

stage("V3", "V3 Komponenten", ["V2", "HV", "V4"], [
    text("V3", """
<h3>V3 – Geschwindigkeitskomponenten (Buch S. 11)</h3>
<p>Lesen Sie den Abschnitt <em>Geschwindigkeitskomponenten</em> und die <em>Beispielaufgabe: Flussüberquerung</em>.</p>
<p>Ein Vektor \\(\\vec v_1\\) lässt sich in eine \\(x\\)-Komponente \\(\\vec v_{1,x}\\) und eine \\(y\\)-Komponente \\(\\vec v_{1,y}\\) zerlegen. Die vektorielle Addition der Komponenten ergibt wieder \\(\\vec v_1\\).</p>
"""),
    image("V3-Bild", IMG["vektor"]),
    mc("V3-negativ", "<p>a) Was meint man mit einer „negativen Geschwindigkeit in \\(x\\)-Richtung“?</p>",
       [("Der Körper bewegt sich entgegen der Richtung der Rechtsachse, seine \\(x\\)-Koordinate wird kleiner.", True, ""),
        ("Der Körper wird langsamer.", False, "Das wäre eine Abbremsung. Gemeint ist hier eine Richtungsangabe."),
        ("Der Betrag der Geschwindigkeit ist kleiner als null.", False, "Ein Betrag ist nie negativ.")],
       route("Lesen Sie den letzten Absatz links auf S. 11.", "Richtig."), single=True),
    blanks("V3-Beispiel", """<p>b) Beispielaufgabe: Ein Schwimmer schwimmt mit \\(v_1=2\\,\\frac{\\text{m}}{\\text{s}}\\) senkrecht über einen \\(10\\,\\text{m}\\) breiten Fluss. Die Strömung hat \\(v_2=1\\,\\frac{\\text{m}}{\\text{s}}\\).</p>""",
           ["<p>Betrag der Gesamtgeschwindigkeit: \\(v\\) ≈ *%s:v1 und v2 stehen senkrecht aufeinander.* %s</p>" % (alt("2,24", "2,2", "2,236"), MS),
            "<p>Zeit bis zum anderen Ufer: \\(t\\) = *%s:Nur v1 bringt den Schwimmer über den Fluss: t = Breite : v1* %s</p>" % (alt("5", "5,0"), SEK),
            "<p>Abdrift flussabwärts in dieser Zeit: *%s:Abdrift = v2 · t* %s</p>" % (alt("5", "5,0"), M)],
           route("Gehen Sie zum Abzweig HV.", weiter("V4")))])

stage("V4", "V4 Übung Fluss", ["V3", "HS", "T1"], [blanks("V4", """
<h3>V4 – Übung: Arbeitsauftrag 1 (Buch S. 11)</h3>
<p>Ein Schwimmer möchte einen \\(30\\,\\text{m}\\) breiten Fluss überqueren. Er schwimmt mit \\(0{,}6\\,\\frac{\\text{m}}{\\text{s}}\\) senkrecht zur Strömungsrichtung. Die Strömung hat den Betrag \\(1{,}2\\,\\frac{\\text{m}}{\\text{s}}\\).</p>
""", ["<p>a) Zeit für die Überquerung: \\(t\\) = *%s:Nur die Komponente quer zum Fluss zählt.* %s</p>" % (alt("50", "50,0"), SEK),
      "<p>b) Betrag der Gesamtgeschwindigkeit: \\(v\\) ≈ *%s* %s</p>" % (alt("1,34", "1,3", "1,342"), MS),
      "<p>c) Länge der Gesamtstrecke: \\(s\\) ≈ *%s:s = v · t oder Pythagoras mit 30 m und der Abdrift* %s</p>" % (alt("67,08", "67,1", "67", "67,05", "67,1"), M)],
    route("Gehen Sie zum Abzweig HV oder fragen Sie nach.", "Richtig.")),
    mc("V4-d", "<p>d) Er möchte das Ufer genau gegenüber erreichen. Was gilt?</p>",
       [("Mit \\(0{,}6\\,\\frac{\\text{m}}{\\text{s}}\\) ist das unmöglich. Er müsste schräg gegen die Strömung und mit mehr als \\(1{,}2\\,\\frac{\\text{m}}{\\text{s}}\\) schwimmen.", True, ""),
        ("Er muss nur schräg gegen die Strömung schwimmen, die Geschwindigkeit reicht.", False,
         "Seine Komponente gegen die Strömung muss 1,2 m/s ausgleichen. Mit 0,6 m/s insgesamt geht das nicht."),
        ("Er muss genau senkrecht schwimmen, dann kommt er gegenüber an.", False, "Dann treibt ihn die Strömung ab, wie in c).")],
       route("Zeichnen Sie: Die Komponente seiner Geschwindigkeit gegen die Strömung muss 1,2 m/s betragen.",
             "Richtig. Weiter zu Teil B (T1). Wer sin und cos auffrischen möchte, geht vorher zu HS."), single=True)])

stage("HS", "HS Hilfe sin/cos", ["V4", "T1"], [
    text("HS", """
<h3>HS – Hilfe: Vektoren mit Sinus und Kosinus zerlegen</h3>
<p>Beim schiefen Wurf kennt man den Betrag \\(v_0\\) und den Abwurfwinkel \\(\\alpha\\). Die Komponenten bekommt man über das rechtwinklige Dreieck: Der Vektor ist die <strong>Hypotenuse</strong>, \\(v_x\\) die <strong>Ankathete</strong>, \\(v_y\\) die <strong>Gegenkathete</strong> von \\(\\alpha\\).</p>
<p>\\[ \\cos(\\alpha)=\\frac{\\text{Ankathete}}{\\text{Hypotenuse}}=\\frac{v_x}{v} \\;\\Rightarrow\\; v_x=v\\cdot\\cos(\\alpha) \\]</p>
<p>\\[ \\sin(\\alpha)=\\frac{\\text{Gegenkathete}}{\\text{Hypotenuse}}=\\frac{v_y}{v} \\;\\Rightarrow\\; v_y=v\\cdot\\sin(\\alpha) \\]</p>
<p><strong>Taschenrechner-Test:</strong> \\(\\sin(30)\\) muss \\(0{,}5\\) ergeben. Erscheint \\(-0{,}988\\), steht der Rechner im Bogenmaß (RAD).</p>
"""),
    image("HS-Bild", IMG["dreieck"]),
    blanks("HS-Aufgabe", "<p><strong>Übung:</strong> \\(v=10\\,\\frac{\\text{m}}{\\text{s}}\\), \\(\\alpha=30^\\circ\\).</p>",
           ["<p>\\(v_x\\) ≈ *%s* %s</p>" % (alt("8,66", "8,7", "8,660"), MS),
            "<p>\\(v_y\\) = *%s* %s</p>" % (alt("5", "5,0", "5,00"), MS)],
           route("Fragen Sie nach und gehen Sie dann weiter zu T1.", weiter("T1")))])

# ================================================================ B · Fragen zum Text
stage("T1", "T1 Beschreibung", ["V4", "HS", "T2"], [
    text("T1", """
<h3>T1 – Beschreibung des schiefen Wurfs (Buch S. 26)</h3>
<p>Lesen Sie <em>Würfe im sportlichen Kontext</em> und <em>Beschreibung des schiefen Wurfs</em> bis einschließlich Gleichung (2).</p>
"""),
    image("T1-Bild", IMG["bahn"]),
    mc("T1-Modell", "<p>a) Welche Aussagen gelten im Modell des schiefen Wurfs? (mehrere richtig)</p>",
       [("Der Luftwiderstand wird vernachlässigt.", True, ""),
        ("In horizontaler Richtung ist die Bewegung gleichförmig.", True, ""),
        ("In vertikaler Richtung ist die Bewegung ein freier Fall mit der Anfangsgeschwindigkeit \\(v_{y,0}\\).", True, ""),
        ("Der waagerechte Wurf ist ein Spezialfall des schiefen Wurfs.", True, ""),
        ("In horizontaler Richtung wird der Körper gleichmäßig beschleunigt.", False, "Horizontal wirkt keine Kraft – die Geschwindigkeit bleibt gleich.")],
       route("Vier Aussagen sind richtig. Lesen Sie die ersten beiden Absätze noch einmal.", "Richtig.")),
    mc("T1-Zerlegung", "<p>b) Mit welchen Gleichungen wird die Startgeschwindigkeit \\(\\vec v_0\\) zerlegt? (mehrere richtig)</p>",
       [("\\(v_{x,0}=v_0\\cdot\\cos(\\alpha)\\)", True, ""),
        ("\\(v_{y,0}=v_0\\cdot\\sin(\\alpha)\\)", True, ""),
        ("\\(v_{x,0}=v_0\\cdot\\sin(\\alpha)\\)", False, "Die horizontale Komponente ist die Ankathete von α – dazu gehört der Kosinus."),
        ("\\(v_{y,0}=v_0\\cdot\\tan(\\alpha)\\)", False, "Der Tangens verbindet die beiden Katheten, nicht Kathete und Hypotenuse.")],
       route("Gehen Sie zum Abzweig HS.", "Richtig.")),
    blanks("T1-Rechnen", "<p>c) Ein Ball wird mit \\(v_0=10\\,\\frac{\\text{m}}{\\text{s}}\\) unter \\(\\alpha=40^\\circ\\) geworfen.</p>",
           ["<p>\\(v_{x,0}\\) ≈ *%s:v0 · cos(40°)* %s</p>" % (alt("7,66", "7,7", "7,660"), MS),
            "<p>\\(v_{y,0}\\) ≈ *%s:v0 · sin(40°)* %s</p>" % (alt("6,43", "6,4", "6,428"), MS)],
           route("Gehen Sie zum Abzweig HS. Taschenrechner im DEG-Modus?", "Richtig.")),
    mc("T1-Gleichung", "<p>d) Welche Gleichung beschreibt die Bewegung in \\(y\\)-Richtung (Start im Ursprung)?</p>",
       [("\\(y(t)=-\\frac{g}{2}\\cdot t^2+v_0\\cdot\\sin(\\alpha)\\cdot t\\)", True, ""),
        ("\\(y(t)=v_0\\cdot\\sin(\\alpha)\\cdot t\\)", False, "Ohne den Term mit g gäbe es keine Fallbewegung."),
        ("\\(y(t)=-\\frac{g}{2}\\cdot t^2+v_0\\cdot\\cos(\\alpha)\\cdot t\\)", False, "Für die y-Richtung brauchen Sie die vertikale Komponente v0·sin(α)."),
        ("\\(y(t)=-g\\cdot t^2+v_0\\cdot\\sin(\\alpha)\\cdot t\\)", False, "Beim freien Fall steht g/2 vor t².")],
       route("Vergleichen Sie mit Gleichung (2) im Buch.", weiter("T2")), single=True)])

stage("T2", "T2 Versuch V1", ["T1", "T3"], [
    text("T2", """
<h3>T2 – Versuch V1 und Merksatz (Buch S. 26–27)</h3>
<p>Lesen Sie den Versuch <em>V1 Bewegungsgleichung einer Kugel beim Boulespiel</em>, den Merksatz und den Absatz danach. Die Regression liefert</p>
<p>\\[ x(t)=3{,}71\\cdot t \\qquad y(t)=-4{,}97\\,t^2+2{,}43\\,t+0{,}44 \\]</p>
"""),
    image("T2-Bild", IMG["boule"]),
    blanks("T2-Ablesen", "<p>a) Vergleichen Sie mit den Gleichungen (1) und (2) und lesen Sie ab:</p>",
           ["<p>\\(v_{x,0}\\) = *%s:Faktor vor t in x(t)* %s</p>" % (alt("3,71", "3,7"), MS),
            "<p>\\(v_{y,0}\\) = *%s:Faktor vor t in y(t)* %s</p>" % (alt("2,43", "2,4"), MS),
            "<p>Starthöhe \\(y_0\\) = *%s:Der Summand ohne t* %s</p>" % (alt("0,44"), M),
            "<p>Fallbeschleunigung im Versuch: \\(g\\) ≈ *%s:−4,97 entspricht −g/2.* \\(\\frac{\\text{m}}{\\text{s}^2}\\)</p>" % alt("9,94", "9,9")],
           route("Ordnen Sie jeden Faktor dem passenden Term in Gleichung (2) zu.", "Richtig.")),
    mc("T2-Bahn", "<p>b) Welche Aussagen aus dem Text stimmen? (mehrere richtig)</p>",
       [("Die Bahnkurve ist eine nach unten geöffnete Parabel (Wurfparabel).", True, ""),
        ("Am Scheitelpunkt ist der Betrag der Geschwindigkeit am kleinsten.", True, ""),
        ("Am Scheitelpunkt ist die Geschwindigkeit null.", False, "Nur die vertikale Komponente ist null. Horizontal fliegt der Körper weiter."),
        ("Der Wert 4,97 sollte genau der Fallbeschleunigung entsprechen.", False, "4,97 sollte die Hälfte der Fallbeschleunigung sein.")],
       route("Lesen Sie den Merksatz und den Absatz unter dem Merksatz.", weiter("T3")))])

stage("T3", "T3 Wurfweite, Höhe", ["T2", "T4"], [
    text("T3", """
<h3>T3 – Wurfweite und maximale Wurfhöhe (Buch S. 27)</h3>
<p>Lesen Sie <em>Wurfweite und maximale Wurfhöhe</em> und den zweiten Merksatz. Abwurf und Landung liegen hier auf gleicher Höhe.</p>
"""),
    mc("T3-Ende", "<p>a) Woran erkennt man rechnerisch den Zeitpunkt \\(t_E\\), an dem der Wurf endet?</p>",
       [("\\(y(t_E)=0\\)", True, ""),
        ("\\(x(t_E)=0\\)", False, "x = 0 gilt am Anfang des Wurfs."),
        ("\\(v_y(t_E)=0\\)", False, "Das gilt am höchsten Punkt, nicht am Ende.")],
       route("Am Ende trifft die Kugel auf den Boden. Welche Koordinate ist dann null?", "Richtig."), single=True),
    mc("T3-Formeln", "<p>b) Welche Gleichungen stehen im Text? (mehrere richtig)</p>",
       [("\\(t_E=2\\,v_0\\cdot\\frac{\\sin(\\alpha)}{g}\\)", True, ""),
        ("\\(w=2\\,v_0^2\\cdot\\frac{\\cos(\\alpha)\\cdot\\sin(\\alpha)}{g}\\)", True, ""),
        ("\\(h=\\frac{1}{2}\\cdot\\frac{(v_0\\cdot\\sin(\\alpha))^2}{g}\\)", True, ""),
        ("\\(w=v_0\\cdot\\frac{\\sin(\\alpha)}{g}\\)", False, "Für die Weite brauchen Sie x(tE) = v0·cos(α)·tE.")],
       route("Drei Gleichungen sind richtig. Vergleichen Sie mit dem Text.", "Richtig.")),
    mc("T3-Winkel", "<p>c) Warum ist \\(\\alpha=45^\\circ\\) der beste Abwurfwinkel (bei gleicher Abwurf- und Landehöhe)?</p>",
       [("Weil das Produkt \\(\\cos(\\alpha)\\cdot\\sin(\\alpha)\\) bei \\(45^\\circ\\) am größten ist.", True, ""),
        ("Weil der Ball bei \\(45^\\circ\\) am höchsten fliegt.", False, "Am höchsten fliegt er bei 90°."),
        ("Weil die Flugzeit bei \\(45^\\circ\\) am längsten ist.", False, "Die Flugzeit wächst mit sin(α) und ist bei 90° am längsten.")],
       route("Lesen Sie den Satz oben rechts auf S. 27.", "Richtig."), single=True),
    blanks("T3-Rechnen", "<p>d) Berechnen Sie mit den Formeln aus dem Merksatz für \\(v_0=10\\,\\frac{\\text{m}}{\\text{s}}\\) und \\(\\alpha=45^\\circ\\):</p>",
           ["<p>Wurfweite \\(w\\) ≈ *%s* %s</p>" % (alt("10,19", "10,2", "10,194"), M),
            "<p>maximale Wurfhöhe \\(h\\) ≈ *%s* %s</p>" % (alt("2,55", "2,5", "2,548", "2,6"), M)],
           route("Setzen Sie ein und achten Sie auf die Klammern bei h.", weiter("T4")))])

stage("T4", "T4 Starthöhe", ["T3", "P1"], [
    text("T4", """
<h3>T4 – Wurf mit Starthöhe, Kugelstoßen, versteckte Würfe (Buch S. 27–28)</h3>
<p>Lesen Sie <em>Der Wurf mit Starthöhe</em>, <em>Gewinnen beim Kugelstoßen</em> und <em>Versteckte Würfe</em>. Die beiden Exkurse lassen Sie aus.</p>
"""),
    image("T4-Bild", IMG["kugelstoss"]),
    mc("T4-Gleichungen", "<p>a) Was ändert sich an den Bewegungsgleichungen, wenn der Wurf in der Höhe \\(y_0\\) beginnt? (mehrere richtig)</p>",
       [("Gleichung (1) für \\(x(t)\\) bleibt unverändert.", True, ""),
        ("In Gleichung (2) kommt der Summand \\(+\\,y_0\\) hinzu.", True, ""),
        ("In Gleichung (1) kommt der Summand \\(+\\,y_0\\) hinzu.", False, "Die Starthöhe ändert nur die vertikale Lage."),
        ("Die Formel \\(w=2\\,v_0^2\\cdot\\frac{\\cos(\\alpha)\\cdot\\sin(\\alpha)}{g}\\) gilt weiterhin.", False,
         "Diese Formel gilt nur bei gleicher Abwurf- und Landehöhe.")],
       route("Vergleichen Sie die Gleichung oben rechts auf S. 27 mit Gleichung (2).", "Richtig.")),
    mc("T4-Kugel", "<p>b) Welcher Abstoßwinkel liefert beim Kugelstoß mit \\(v_0=8{,}5\\,\\frac{\\text{m}}{\\text{s}}\\) aus \\(2\\,\\text{m}\\) Höhe die größte Weite?</p>",
       [("etwa \\(40^\\circ\\)", True, ""),
        ("genau \\(45^\\circ\\)", False, "45° ist nur bei gleicher Abwurf- und Landehöhe optimal."),
        ("etwa \\(60^\\circ\\)", False, "Schauen Sie in Bild B1 auf S. 28: Die 60°-Bahn landet früher.")],
       route("Lesen Sie den Abschnitt „Gewinnen beim Kugelstoßen“.", "Richtig."), single=True),
    mc("T4-Zusammenhang", "<p>c) Welche Aussagen stehen im Text? (mehrere richtig)</p>",
       [("In der Umgebung des optimalen Winkels ändert sich die Weite nur wenig.", True, ""),
        ("Mit steigender Anfangsgeschwindigkeit steigt die Stoßweite, aber nicht proportional.", True, ""),
        ("Beim Weitsprung folgt der Körperschwerpunkt einer Wurfparabel.", True, ""),
        ("Doppelte Anfangsgeschwindigkeit bedeutet doppelte Stoßweite.", False, "Der Zusammenhang ist nicht proportional (Bild B3)."),
        ("Beim Weitsprung beginnt und endet die Wurfparabel auf dem Boden.", False, "Sie beginnt etwa 1 m und endet etwa 0,5 m über dem Boden.")],
       route("Drei Aussagen sind richtig.", "Richtig. Weiter zum Herleitungspuzzle (P1)."))])

# ================================================================ C · Herleitungspuzzle
NOTATION = "<p>\\[ \\begin{array}{|l|l|l|} \\hline \\textbf{Puzzle} & \\textbf{Buch} & \\textbf{Bedeutung} \\\\ \\hline s_x,\\ s_y & x(t),\\ y(t) & \\text{Ort in } x\\text{- bzw. } y\\text{-Richtung} \\\\ \\hline v_{0x},\\ v_{0y} & v_{x,0},\\ v_{y,0} & \\text{Komponenten der Startgeschwindigkeit} \\\\ \\hline h_0 & y_0 & \\text{Starthöhe} \\\\ \\hline t_{ges} & t_E & \\text{gesamte Flugzeit} \\\\ \\hline s_{max} & w & \\text{Wurfweite} \\\\ \\hline \\end{array} \\]</p>"

stage("P1", "P1 Puzzle: x und y", ["T4", "P2"], [
    text("P1", f"""
<h3>P1 – Herleitungspuzzle, Teil 1: Superposition</h3>
<p><strong>Auftrag:</strong> Schneiden Sie die Karten des Arbeitsblatts aus und legen Sie die Herleitung der Wurfweite in eine sinnvolle Reihenfolge. Die Etappen P1–P4 prüfen Ihre Lösung Schritt für Schritt.</p>
<ul>
<li>Die <span style="background-color:#7CFC00">grün</span> markierte Karte ist der Anfang.</li>
<li>Die <span style="background-color:#ffff00">gelb</span> markierten Karten sind die Ergebnisse. Die Lücke \\(\\alpha=\\ldots\\) füllen Sie in P4.</li>
<li>Die Karte mit der Wurfbahn (Abbildung) gehört neben den Anfang.</li>
</ul>
<p>Das Puzzle verwendet eine etwas andere Schreibweise als das Buch:</p>
{NOTATION}
"""),
    mc("P1-Start", "<p>a) Mit welcher Karte beginnt die Herleitung?</p>",
       [("Beim schiefen Wurf gilt das Superpositionsprinzip.", True, ""),
        ("\\(s_{max}=v_x\\cdot t_{ges}\\)", False, "Das ist ein späterer Schritt: Erst müssen Sie die Bewegungen in x und y beschreiben."),
        ("\\(v_0=\\sqrt{v_{0x}^2+v_{0y}^2}\\)", False, "Diese Karte verbindet die Komponenten – sie kommt nach der Zerlegung.")],
       route("Die grüne Karte steht am Anfang.", "Richtig: Weil sich die Bewegungen überlagern, kann man x- und y-Richtung getrennt betrachten."), single=True),
    mc("P1-x", "<p>b) Welche Karten gehören in die Spalte für die \\(x\\)-Richtung? (mehrere richtig)</p>",
       [("Die Bewegung in \\(x\\)-Richtung ist gleichförmig.", True, ""),
        ("\\(a_x=0\\)", True, ""),
        ("\\(v_x=v_{0x}=\\text{konstant}\\)", True, ""),
        ("\\(s_x=v_{0x}\\cdot t\\)", True, ""),
        ("\\(v_{0x}=v_0\\cdot\\cos(\\alpha)\\)", True, ""),
        ("\\(a_y=-g\\)", False, "Diese Karte beschreibt die y-Richtung."),
        ("\\(v_{0y}=v_0\\cdot\\sin(\\alpha)\\)", False, "Das ist die Startgeschwindigkeit in y-Richtung.")],
       route("Fünf Karten sind richtig. In x-Richtung wirkt keine Kraft. Gehen Sie bei Bedarf zu HP.", "Richtig.")),
    mc("P1-y", "<p>c) Welche Karten gehören in die Spalte für die \\(y\\)-Richtung? (mehrere richtig)</p>",
       [("Die Bewegung in \\(y\\)-Richtung ist gleichmäßig beschleunigt.", True, ""),
        ("\\(a_y=-g\\)", True, ""),
        ("\\(v_y=-g\\cdot t+v_{0y}\\)", True, ""),
        ("\\(s_y=-\\frac{1}{2}\\,g\\,t^2+v_{0y}\\cdot t+h_0\\)", True, ""),
        ("\\(v_{0y}=v_0\\cdot\\sin(\\alpha)\\)", True, ""),
        ("\\(s_x=v_{0x}\\cdot t\\)", False, "Das ist die Ortsgleichung in x-Richtung."),
        ("\\(a_x=0\\)", False, "Das gilt in x-Richtung.")],
       route("Fünf Karten sind richtig. In y-Richtung wirkt die Fallbeschleunigung. Gehen Sie bei Bedarf zu HP.", "Richtig.")),
    mc("P1-Reihenfolge", "<p>d) In welcher Reihenfolge legt man die Karten einer Spalte sinnvoll von oben nach unten?</p>",
       [("Bewegungsart → Beschleunigung → Geschwindigkeit → Ort", True, ""),
        ("Ort → Geschwindigkeit → Beschleunigung → Bewegungsart", False, "Das geht auch, ist aber umgekehrt: Man beginnt meist mit der Ursache, der Beschleunigung."),
        ("Geschwindigkeit → Bewegungsart → Ort → Beschleunigung", False, "Die Beschleunigung bestimmt die Geschwindigkeit, die Geschwindigkeit den Ort.")],
       route("Was bestimmt was? Die Beschleunigung ändert die Geschwindigkeit, die Geschwindigkeit ändert den Ort.",
             "Richtig. Die Karten \\(v_{0x}=v_0\\cdot\\cos(\\alpha)\\), \\(v_{0y}=v_0\\cdot\\sin(\\alpha)\\) und \\(v_0=\\sqrt{v_{0x}^2+v_{0y}^2}\\) zur Zerlegung legen Sie neben die Spalten. Weiter zu P2."), single=True)])

stage("HP", "HP Hilfe Puzzle", ["P2", "P3"], [text("HP", """
<h3>HP – Hilfe zum Herleitungspuzzle</h3>
<p><strong>Gerüst der Herleitung:</strong></p>
<ol>
<li><strong>Superpositionsprinzip</strong> (grüne Karte): Die Bewegung wird in zwei unabhängige Teilbewegungen zerlegt.</li>
<li><strong>Zerlegung von \\(\\vec v_0\\):</strong> \\(v_{0x}=v_0\\cdot\\cos(\\alpha)\\), \\(v_{0y}=v_0\\cdot\\sin(\\alpha)\\), umgekehrt \\(v_0=\\sqrt{v_{0x}^2+v_{0y}^2}\\).</li>
<li><strong>Spalte x:</strong> gleichförmig → \\(a_x=0\\) → \\(v_x=v_{0x}=\\text{konstant}\\) → \\(s_x=v_{0x}\\cdot t\\).</li>
<li><strong>Spalte y:</strong> gleichmäßig beschleunigt → \\(a_y=-g\\) → \\(v_y=-g\\cdot t+v_{0y}\\) → \\(s_y=-\\frac{1}{2}g t^2+v_{0y}\\cdot t+h_0\\).</li>
<li><strong>Steigzeit:</strong> Am höchsten Punkt ist \\(v_y=0\\). Einsetzen in \\(v_y\\) liefert \\(t_{steig}\\).</li>
<li><strong>Flugzeit:</strong> Bei gleicher Abwurf- und Landehöhe ist \\(t_{ges}=2\\cdot t_{steig}\\).</li>
<li><strong>Wurfweite:</strong> \\(s_{max}=v_x\\cdot t_{ges}\\), dann einsetzen und vereinfachen.</li>
<li><strong>Umformen</strong> mit \\(\\cos(\\alpha)\\cdot\\sin(\\alpha)=\\frac{1}{2}\\sin(2\\alpha)\\) und den <strong>besten Winkel</strong> bestimmen.</li>
</ol>
<p><strong>Tipp:</strong> Karten mit Pfeilen \\(\\rightarrow\\) enthalten mehrere Umformungsschritte. Lesen Sie sie von oben nach unten.</p>
""" + NOTATION)])

stage("P2", "P2 Puzzle: Flugzeit", ["P1", "HP", "P3"], [
    mc("P2-Scheitel", "<h3>P2 – Herleitungspuzzle, Teil 2: Steigzeit und Flugzeit</h3><p>a) Welche Bedingung gilt im höchsten Punkt der Bahnkurve?</p>",
       [("\\(v_y=0\\)", True, ""),
        ("\\(v_x=0\\)", False, "Die horizontale Geschwindigkeit bleibt konstant."),
        ("\\(a_y=0\\)", False, "Die Fallbeschleunigung wirkt immer."),
        ("\\(s_y=0\\)", False, "s_y = 0 gilt am Boden.")],
       route("Am höchsten Punkt steigt der Ball nicht mehr und fällt noch nicht.", "Richtig."), single=True),
    mc("P2-Steigzeit", "<p>b) Setzen Sie \\(v_y=0\\) in \\(v_y=-g\\cdot t+v_{0y}\\) ein. Welche Steigzeit erhalten Sie?</p>",
       [("\\(t_{steig}=\\displaystyle\\frac{v_0\\cdot\\sin(\\alpha)}{g}\\)", True, ""),
        ("\\(t_{steig}=\\displaystyle\\frac{v_0\\cdot\\cos(\\alpha)}{g}\\)", False, "In y-Richtung steht v0y = v0·sin(α)."),
        ("\\(t_{steig}=\\displaystyle\\frac{g}{v_0\\cdot\\sin(\\alpha)}\\)", False, "Prüfen Sie die Einheit: Das Ergebnis muss eine Zeit sein."),
        ("\\(t_{steig}=\\displaystyle\\frac{2\\cdot v_0\\cdot\\sin(\\alpha)}{g}\\)", False, "Das ist schon die gesamte Flugzeit.")],
       route("0 = −g·t + v0·sin(α). Bringen Sie g·t auf die andere Seite und teilen Sie durch g.", "Richtig.")),
    mc("P2-Flugzeit", "<p>c) Warum gilt \\(t_{ges}=2\\cdot t_{steig}\\)?</p>",
       [("Weil Abwurf- und Landehöhe gleich sind: Steigzeit und Sinkzeit sind dann gleich lang.", True, ""),
        ("Weil der Ball immer doppelt so lange fällt, wie er steigt.", False, "Die Zeiten sind gleich, nicht doppelt so lang."),
        ("Das gilt bei jedem schiefen Wurf, auch mit Starthöhe.", False,
         "Mit Starthöhe ist die Sinkzeit länger als die Steigzeit. Das ist wichtig für Aufgabe 1b!")],
       route("Lesen Sie die Karte zur Flugzeit genau.", "Richtig."), single=True),
    blanks("P2-Zahl", "<p>d) Zahlenbeispiel: \\(v_0=10\\,\\frac{\\text{m}}{\\text{s}}\\), \\(\\alpha=30^\\circ\\).</p>",
           ["<p>\\(t_{steig}\\) ≈ *%s* %s</p>" % (alt("0,51", "0,5", "0,510"), SEK),
            "<p>\\(t_{ges}\\) ≈ *%s* %s</p>" % (alt("1,02", "1,0", "1,019", "1,01"), SEK)],
           route("Setzen Sie in t_steig = v0·sin(α) : g ein und verdoppeln Sie.", weiter("P3")))])

stage("P3", "P3 Puzzle: Wurfweite", ["P2", "HP", "P4"], [
    mc("P3-Ansatz", "<h3>P3 – Herleitungspuzzle, Teil 3: Wurfweite</h3><p>a) Mit welchem Ansatz berechnet man die Wurfweite?</p>",
       [("\\(s_{max}=v_x\\cdot t_{ges}\\)", True, ""),
        ("\\(s_{max}=v_y\\cdot t_{ges}\\)", False, "Die Weite ist eine horizontale Strecke."),
        ("\\(s_{max}=v_0\\cdot t_{ges}\\)", False, "v0 zeigt schräg nach oben. Für die Weite zählt nur die x-Komponente.")],
       route("Die Wurfweite ist die Strecke in x-Richtung.", "Richtig."), single=True),
    mc("P3-Einsetzen", "<p>b) Setzen Sie \\(v_x=v_0\\cdot\\cos(\\alpha)\\) und \\(t_{ges}=2\\cdot t_{steig}\\) ein. Welches Ergebnis steht auf der Karte?</p>",
       [("\\(s_{max}=\\displaystyle\\frac{2\\cdot v_0^2}{g}\\cdot\\cos(\\alpha)\\cdot\\sin(\\alpha)\\)", True, ""),
        ("\\(s_{max}=\\displaystyle\\frac{v_0^2}{g}\\cdot\\cos(\\alpha)\\cdot\\sin(\\alpha)\\)", False, "Der Faktor 2 aus t_ges = 2·t_steig fehlt."),
        ("\\(s_{max}=\\displaystyle\\frac{2\\cdot v_0}{g}\\cdot\\cos(\\alpha)\\cdot\\sin(\\alpha)\\)", False, "v0 kommt zweimal vor: in v_x und in t_steig. Also v0²."),
        ("\\(s_{max}=\\displaystyle\\frac{2\\cdot v_0^2}{g}\\cdot\\sin^2(\\alpha)\\)", False, "v_x enthält den Kosinus.")],
       route("Schreiben Sie s_max = v0·cos(α) · 2 · v0·sin(α) : g und fassen Sie zusammen.", "Richtig.")),
    mc("P3-Umformen", "<p>c) Mit der Karte \\(\\cos(\\alpha)\\cdot\\sin(\\alpha)=\\frac{1}{2}\\sin(2\\alpha)\\) lässt sich das Ergebnis vereinfachen. Welche gelbe Ergebniskarte entsteht?</p>",
       [("\\(s_{max}=\\displaystyle\\frac{v_0^2}{g}\\cdot\\sin(2\\alpha)\\)", True, ""),
        ("\\(s_{max}=\\displaystyle\\frac{2\\cdot v_0^2}{g}\\cdot\\sin(2\\alpha)\\)", False, "2 · ½ = 1. Der Faktor 2 kürzt sich weg."),
        ("\\(s_{max}=\\displaystyle\\frac{v_0^2}{2g}\\cdot\\sin(2\\alpha)\\)", False, "Multiplizieren Sie 2 mit ½.")],
       route("Ersetzen Sie cos(α)·sin(α) durch ½·sin(2α) und kürzen Sie.", "Richtig.")),
    blanks("P3-Zahl", "<p>d) Zahlenbeispiel: \\(v_0=10\\,\\frac{\\text{m}}{\\text{s}}\\), \\(\\alpha=30^\\circ\\).</p>",
           ["<p>\\(s_{max}\\) ≈ *%s:v0² : g · sin(60°)* %s</p>" % (alt("8,83", "8,8", "8,828"), M)],
           route("2α = 60°. Rechnen Sie 100 : 9,81 · sin(60°).", weiter("P4")))])

stage("P4", "P4 Puzzle: bester Winkel", ["P3", "A1"], [
    blanks("P4", """<h3>P4 – Herleitungspuzzle, Teil 4: Der beste Winkel</h3>
<p>In \\(s_{max}=\\displaystyle\\frac{v_0^2}{g}\\cdot\\sin(2\\alpha)\\) hängt nur \\(\\sin(2\\alpha)\\) vom Winkel ab. Der Sinus ist höchstens 1.</p>""",
           ["<p>\\(\\sin(2\\alpha)\\) ist maximal für \\(2\\alpha\\) = *90:Bei welchem Winkel hat die Sinusfunktion ihr Maximum?* %s</p>" % GRAD,
            "<p>Daraus ergibt sich eine maximale Weite bei einem Wurfwinkel von \\(\\alpha\\) = *45* %s</p>" % GRAD],
           route("sin(90°) = 1 ist der größte Wert des Sinus.",
                 "Richtig. Tragen Sie α = 45° in die gelbe Lücke auf dem Arbeitsblatt ein.")),
    mc("P4-Gleich", "<p>Für welche Winkelpaare ergibt sich dieselbe Wurfweite?</p>",
       [("\\(30^\\circ\\) und \\(60^\\circ\\)", True, ""),
        ("\\(20^\\circ\\) und \\(70^\\circ\\)", True, ""),
        ("\\(30^\\circ\\) und \\(45^\\circ\\)", False, "sin(60°) ≠ sin(90°)."),
        ("\\(40^\\circ\\) und \\(60^\\circ\\)", False, "sin(80°) ≠ sin(120°).")],
       route("Berechnen Sie jeweils sin(2α). Gleiche Werte bedeuten gleiche Weite.",
             "Richtig: Winkel, die sich zu 90° ergänzen, liefern dieselbe Weite. Übertragen Sie das gelegte Puzzle in Ihr Heft. Weiter zu Aufgabe 1 (A1).")),
    text("P4-Grenzen", "<p><strong>Achtung, Gültigkeit:</strong> \\(s_{max}=\\frac{v_0^2}{g}\\cdot\\sin(2\\alpha)\\) und \\(\\alpha=45^\\circ\\) gelten nur, wenn Abwurf- und Landehöhe <strong>gleich</strong> sind. Mit Starthöhe \\(h_0&gt;0\\) müssen Sie mit \\(s_y=0\\) rechnen (siehe Aufgabe 1b).</p>")])

# ================================================================ D · Aufgabe 1
AUFG1 = """<p><strong>Aufgabe 1 (Buch S. 29):</strong> Ein Basketball wird mit einer Anfangsgeschwindigkeit \\(v_0=7\\,\\frac{\\text{m}}{\\text{s}}\\) unter einem Winkel \\(\\alpha=56^\\circ\\) geworfen. Berechnen Sie die Wurfweite, wenn</p>"""

stage("A1", "A1 Aufgabe 1a", ["P4", "HA", "A2"], [blanks("A1", f"""<h3>A1 – Aufgabe 1a: Wurf vom Boden</h3>
{AUFG1}
<p>a) der Ball vom Boden aus geworfen wird.</p>
<p><em>Hinweis:</em> Abwurf- und Landehöhe sind gleich – die Formel aus dem Puzzle gilt.</p>""",
    ["<p>Wurfweite \\(s_{max}\\) ≈ *%s:s_max = v0² : g · sin(2α) mit 2α = 112°* %s</p>" % (alt("4,63", "4,6", "4,631", "4,62", "4,64"), M)],
    route("Gehen Sie zum Abzweig HA mit den Zwischenschritten.", weiter("A2")))])

stage("HA", "HA Hilfe Aufgabe 1", ["A1", "A2"], [blanks("HA", """<h3>HA – Hilfe: Aufgabe 1 Schritt für Schritt</h3>
<p>\\(v_0=7\\,\\frac{\\text{m}}{\\text{s}}\\), \\(\\alpha=56^\\circ\\), \\(g=9{,}81\\,\\frac{\\text{m}}{\\text{s}^2}\\)</p>""",
    ["<p><strong>Schritt 1 – Komponenten:</strong> \\(v_{0x}=7\\cdot\\cos(56^\\circ)\\) ≈ *%s* %s und \\(v_{0y}=7\\cdot\\sin(56^\\circ)\\) ≈ *%s* %s</p>"
     % (alt("3,91", "3,9", "3,914"), MS, alt("5,8", "5,80", "5,803"), MS),
     "<p><strong>a) Schritt 2 – Steigzeit:</strong> \\(t_{steig}=\\frac{v_{0y}}{g}\\) ≈ *%s* %s</p>" % (alt("0,59", "0,6", "0,592"), SEK),
     "<p><strong>a) Schritt 3 – Flugzeit:</strong> \\(t_{ges}=2\\cdot t_{steig}\\) ≈ *%s* %s</p>" % (alt("1,18", "1,2", "1,183", "1,184"), SEK),
     "<p><strong>a) Schritt 4 – Weite:</strong> \\(s_{max}=v_{0x}\\cdot t_{ges}\\) ≈ *%s* %s</p>" % (alt("4,63", "4,6", "4,631", "4,62", "4,64"), M),
     "<p><strong>b) Schritt 2 – Gleichung aufstellen:</strong> Der Ball landet bei \\(s_y=0\\). Mit \\(h_0=2\\,\\text{m}\\) gilt \\(0=-4{,}905\\,t^2+5{,}80\\,t+2\\).</p>",
     "<p><strong>b) Schritt 3 – Flugzeit:</strong> positive Lösung \\(t_{ges}\\) ≈ *%s:abc-Formel mit a = −4,905; b = 5,80; c = 2* %s</p>" % (alt("1,46", "1,5", "1,462"), SEK),
     "<p><strong>b) Schritt 4 – Weite:</strong> \\(s_{max}=v_{0x}\\cdot t_{ges}\\) ≈ *%s* %s</p>" % (alt("5,72", "5,7", "5,723", "5,71", "5,73"), M)],
    route("Notieren Sie, bei welchem Schritt Sie hängen, und fragen Sie nach.",
          "Richtig. Lösen Sie jetzt A1 und A2 noch einmal ohne Hilfe."))])

stage("A2", "A2 Aufgabe 1b", ["A1", "HA", "Ziel"], [
    blanks("A2", f"""<h3>A2 – Aufgabe 1b: Wurf aus 2 m Höhe</h3>
{AUFG1}
<p>b) der Ball aus einer Höhe von \\(2\\,\\text{{m}}\\) über dem Boden geworfen wird.</p>
<p><em>Hinweis:</em> Jetzt sind Abwurf- und Landehöhe <strong>verschieden</strong>. Die Formel \\(s_{{max}}=\\frac{{v_0^2}}{{g}}\\sin(2\\alpha)\\) gilt nicht. Bestimmen Sie die Flugzeit aus \\(s_y=0\\) mit \\(h_0=2\\,\\text{{m}}\\).</p>""",
           ["<p>Flugzeit \\(t_{ges}\\) ≈ *%s:0 = −½·g·t² + v0·sin(α)·t + 2 mit der abc- oder pq-Formel lösen* %s</p>" % (alt("1,46", "1,5", "1,462"), SEK),
            "<p>Wurfweite \\(s_{max}\\) ≈ *%s:s_max = v0·cos(α) · t_ges* %s</p>" % (alt("5,72", "5,7", "5,723", "5,71", "5,73"), M)],
           route("Gehen Sie zum Abzweig HA mit den Zwischenschritten.", "Richtig.")),
    mc("A2-Vergleich", "<p>Vergleichen Sie a) und b): Warum fliegt der Ball in b) weiter?</p>",
       [("Er hat mehr Zeit zum Fallen, weil er 2 m tiefer landet als er startet. In dieser Zeit fliegt er horizontal weiter.", True, ""),
        ("Weil er in b) schneller abgeworfen wird.", False, "v0 ist in beiden Fällen 7 m/s."),
        ("Weil der Winkel in b) näher an 45° liegt.", False, "Der Winkel ist in beiden Fällen 56°.")],
       route("Vergleichen Sie die Flugzeiten.", "Richtig. Weiter zum Ziel."), single=True)])

stage("Ziel", "Ziel", ["A2"], [{}], special="finish")

# ================================================================ Zusammenbau
index = {s["key"]: i for i, s in enumerate(S)}
for s in S:
    for n in s["nb"]:
        assert s["key"] in S[index[n]]["nb"], (s["key"], n)

W_PCT, H_PCT = 3.6, 5.76
elements, paths = [], []
for i, s in enumerate(S):
    (cx, cy), _ = POS[s["key"]]
    el = {
        "id": "wurf11-" + s["key"].lower(),
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
    json.dump([{"code": s["key"], "cx": POS[s["key"]][0][0], "cy": POS[s["key"]][0][1],
                "ldx": POS[s["key"]][1][0], "ldy": POS[s["key"]][1][1],
                "nb": [index[n] for n in s["nb"]], "finish": s["special"] == "finish"} for s in S],
              f, ensure_ascii=False, indent=1)

ref = json.load(open(os.path.join(REF, "content", "content.json"), encoding="utf-8"))
END = """<p style="text-align: center;"><strong>Leitfrage:</strong> Wie weit fliegt ein schräg geworfener Ball – und unter welchem Winkel fliegt er am weitesten?</p>
<p style="text-align: center;">Beantworten Sie die Leitfrage im Heft in höchstens vier Sätzen. Nennen Sie auch, wann \\(\\alpha=45^\\circ\\) <em>nicht</em> der beste Winkel ist.</p>
"""
visual = json.loads(json.dumps(ref["visual"]))
visual["stages"].update({"colorStage": "rgba(214, 228, 244, 0.92)", "colorStageCleared": "rgba(46, 170, 120, 0.92)"})
visual["paths"]["style"].update({"colorPath": "rgba(200, 220, 240, 0.8)", "colorPathCleared": "rgba(46, 170, 120, 0.9)"})
hintergrund = "karte-beschriftet.jpg" if os.path.exists(os.path.join(HERE, "bilder", "karte-beschriftet.jpg")) else "karte.jpg"
content = {
    "showTitleScreen": False,
    "titleScreen": {"titleScreenIntroduction": "<p style=\"text-align: center;\"></p>"},
    "headline": "Der schiefe Wurf – Herleitung",
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
h5p["title"] = "Der schiefe Wurf – Herleitung (Klasse 11)"
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
