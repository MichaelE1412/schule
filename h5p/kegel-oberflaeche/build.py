#!/usr/bin/env python3
"""Baut den Lernpfad „Oberflächeninhalt des Kegels“ als H5P Game Map.

Aufruf:  python3 build.py <entpackte Trapez-Referenz> <Ordner H5P.Video-1.6> <Ausgabe.h5p>

Bibliotheken: aus der Referenzdatei „Umfang und Flächeninhalt – Trapez“ (Lumi),
dazu H5P.Video 1.6.66 (läuft mit H5P-Core 1.27 wie in Lumi).
Inhalte: Fundamente der Mathematik, Kap. 2.3 „Netz und Oberflächeninhalt eines Kegels“ (S. 41–43).
"""
import json
import os
import sys
import zipfile

from bausteine import alt, dragtext, image, mc, route, text, blanks, video, PARALLEL_FB

HERE = os.path.dirname(os.path.abspath(__file__))
REF, VIDEO_LIB, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

IMG_NETZ = ("images/kegel-netz.png", 960, 480, "Kegel mit r, h und s und sein Netz aus Kreisausschnitt und Kreis")
IMG_A1 = ("images/aufgabe1-kegel.png", 860, 420, "Drei Kegel: a) s = 12 cm, r = 5,1 cm; b) s = 10 mm, d = 8 mm; c) s = 12,2 cm, d = 11,4 cm")
IMG_A10 = ("images/aufgabe10-netze.png", 1060, 490, "Drei mögliche Kegelnetze: a) Viertelkreis s = 4 cm mit Kreis r = 1 cm; b) Halbkreis s = 4 cm mit Kreis r = 1 cm; c) Halbkreis s = 4 cm mit Kreis r = 2 cm")
IMG_A15 = ("images/aufgabe15-lampenschirm.png", 800, 460, "Stofffläche für einen Lampenschirm: Kreisringausschnitt mit Bögen 50 cm und 100 cm, Breite 70 cm, Abstand x zur Spitze")
IMG_HUT = ("images/hut.png", 820, 470, "Kegelförmiger Hut aus Filz und sein Schnittmuster")

VIDEO_URL = "https://www.youtube.com/watch?v=YYJ_GfOVu44"

S = []


def stage(key, label, cx, cy, neighbors, contents, start=False, special=None):
    """cx, cy: Mittelpunkt der Etappe in Pixeln auf der 1600 × 1000-Karte."""
    S.append(dict(key=key, label=label, cx=cx, cy=cy, nb=neighbors, contents=contents,
                  start=start, special=special))


F = "\\(O=\\pi\\cdot r^2+\\pi\\cdot r\\cdot s\\)"

# ================================================================ Start und Diagnose
stage("Start", "Start", 90, 870, ["D1"], [text("Start", """
<h2>Oberflächeninhalt des Kegels</h2>
<p><strong>Leitfrage:</strong> Wie viel Material braucht man für einen Kegel – und warum ist sein Mantel ein Kreisausschnitt?</p>
<p><strong>Rückblick:</strong> Bei der Pyramide gilt \\(O=G+M\\). Beim Kegel ist das genauso – nur sind Grundfläche und Mantel rund.</p>
<p><strong>Ablauf (ca. 2 Stunden):</strong> Vorwissen (D) → Einstieg, Video, Wissen (E, V, W) → Basisaufgaben (P) → weiterführende Aufgaben (B) → Profi-Aufgaben zur Wahl (S).</p>
<ul>
<li><strong>H, T, F</strong> sind Abzweige mit Hilfen. Geh nur dorthin, wenn dich eine Rückmeldung hinschickt.</li>
<li>Rechne mit \\(\\pi\\) auf dem Taschenrechner und runde Ergebnisse auf zwei Nachkommastellen. Einheiten stehen schon hinter den Feldern.</li>
<li>Lege dein Heft bereit.</li>
</ul>
""")], start=True)

stage("D1", "D1 Kreis", 260, 870, ["Start", "H1", "D2"], [blanks("D1", """
<h3>D1 – Vorwissen: Kreis</h3>
<p>Ein Kreis hat den Radius \\(r=4\\,\\text{cm}\\). Berechne Umfang und Flächeninhalt.</p>
""", ["<p>u ≈ *%s:u = 2 · π · r* cm</p>" % alt("25,13", "25,1", "25,12", "25,14"),
      "<p>A ≈ *%s:A = π · r²* cm²</p>" % alt("50,27", "50,3", "50,26", "50,24")],
    route("Geh zuerst zum Abzweig H1.", "Richtig. Weiter zu D2."))])

stage("H1", "H1 Hilfe Kreis", 390, 730, ["D1", "D2"], [
    text("H1", """
<h3>H1 – Abzweig: Kreisformeln</h3>
<p>\\(d=2\\cdot r\\) (Durchmesser) · \\(u=2\\cdot\\pi\\cdot r\\) (Umfang) · \\(A=\\pi\\cdot r^2\\) (Flächeninhalt)</p>
<p><strong>Muster:</strong> \\(r=3\\,\\text{cm}\\): \\(u=2\\cdot\\pi\\cdot 3\\approx 18{,}85\\,\\text{cm}\\) und \\(A=\\pi\\cdot 3^2\\approx 28{,}27\\,\\text{cm}^2\\).</p>
<p>Achtung: Ist der <strong>Durchmesser</strong> gegeben, halbiere ihn zuerst.</p>
"""),
    blanks("H1-Aufgabe", "<p><strong>Parallelaufgabe:</strong> Ein Kreis hat den Durchmesser \\(d=10\\,\\text{cm}\\).</p>",
           ["<p>r = *5* cm</p>",
            "<p>u ≈ *%s* cm</p>" % alt("31,42", "31,4", "31,41"),
            "<p>A ≈ *%s* cm²</p>" % alt("78,54", "78,5", "78,53")], PARALLEL_FB)])

stage("D2", "D2 Pythagoras", 520, 870, ["D1", "H1", "H2", "E"], [blanks("D2", """
<h3>D2 – Vorwissen: Satz des Pythagoras</h3>
<p>Ein Kegel hat den Radius \\(r=5\\,\\text{cm}\\) und die Höhe \\(h=12\\,\\text{cm}\\). Die <strong>Mantellinie</strong> \\(s\\) verläuft von der Spitze zum Rand der Grundfläche. Berechne \\(s\\).</p>
""", ["<p>s = *%s:Höhe, Radius und Mantellinie bilden ein rechtwinkliges Dreieck.* cm</p>" % alt("13", "13,0")],
    route("Geh zuerst zum Abzweig H2.", "Richtig. Weiter zu E."), img=IMG_NETZ)])

stage("H2", "H2 Hilfe Mantellinie", 650, 730, ["D2", "E"], [
    text("H2", """
<h3>H2 – Abzweig: Mantellinie mit Pythagoras</h3>
<p>Wie bei der Pyramide gibt es ein <strong>Stützdreieck</strong>: Höhe \\(h\\), Radius \\(r\\) und Mantellinie \\(s\\). Der rechte Winkel liegt im Mittelpunkt der Grundfläche, \\(s\\) ist die Hypotenuse:</p>
<p>\\[ s^2=r^2+h^2 \\qquad s=\\sqrt{r^2+h^2} \\]</p>
<p><strong>Muster:</strong> \\(r=3\\,\\text{cm}\\), \\(h=4\\,\\text{cm}\\): \\(s=\\sqrt{9+16}=\\sqrt{25}=5\\,\\text{cm}\\).</p>
"""),
    image("H2-Bild", IMG_NETZ),
    blanks("H2-Aufgabe", "<p><strong>Parallelaufgabe:</strong> \\(r=6\\,\\text{cm}\\), \\(h=8\\,\\text{cm}\\).</p>",
           ["<p>s = *%s* cm</p>" % alt("10", "10,0")], PARALLEL_FB)])

# ================================================================ Erarbeitung
stage("E", "E Einstieg Hut", 780, 870, ["D2", "H2", "V"], [
    text("E", """
<h3>E – Einstieg: Ein Hut aus Filz</h3>
<p>Aus Filz soll ein kegelförmiger Hut gebastelt werden. Eine Person mit einem Kopfumfang von \\(55\\,\\text{cm}\\) soll ihn tragen.</p>
<p>Skizziere in deinem Heft ein passendes Schnittmuster. Beantworte dann die Fragen.</p>
"""),
    image("E-Bild", IMG_HUT),
    mc("E-Form", "<p>Welche Form hat das Schnittmuster für den Hut (ohne Boden)?</p>",
       [("einen Kreisausschnitt", True, ""),
        ("ein Dreieck", False, "Rollst du ein Dreieck auf, ist der untere Rand nicht rund."),
        ("ein Rechteck", False, "Ein aufgerolltes Rechteck ergibt einen Zylinder, keine Spitze."),
        ("einen ganzen Kreis", False, "Einen ganzen Kreis kannst du nicht zu einer Spitze formen.")],
       route("Lies die Rückmeldung zu deiner Antwort.", "Richtig."), single=True),
    mc("E-Laenge", "<p>Welche Länge im Schnittmuster ist durch den Kopfumfang von \\(55\\,\\text{cm}\\) festgelegt?</p>",
       [("die Länge des Kreisbogens", True, ""),
        ("der Radius des Kreisausschnitts", False, "Der Radius bestimmt, wie hoch der Hut wird."),
        ("die Höhe des Hutes", False, "Die Höhe kannst du frei wählen."),
        ("der Mittelpunktswinkel", False, "Der Winkel ergibt sich erst aus Bogen und Radius.")],
       route("Der Kopf passt in den unteren Rand des Hutes. Welche Linie im Schnittmuster wird zu diesem Rand?",
             "Richtig: Der Kreisbogen wird zum Rand des Hutes. Weiter zu V."), single=True)])

stage("V", "V Video", 1000, 870, ["E", "W"], [
    text("V", """
<h3>V – Video: Netz und Oberfläche des Kegels</h3>
<p>Schau dir das Video an. Notiere in deinem Heft:</p>
<ol><li>Aus welchen Teilen besteht das Netz eines Kegels?</li>
<li>Wie lang ist der Bogen des Kreisausschnitts?</li>
<li>Wie lautet die Formel für den Oberflächeninhalt?</li></ol>
<p>Beantworte danach die Fragen unter dem Video. Du darfst das Video dafür noch einmal ansehen.</p>
"""),
    video("V", VIDEO_URL, "Video: Oberfläche des Kegels"),
    mc("V-1", "<p>1. Der Bogen des Kreisausschnitts (Mantelbogen) ist genauso lang wie …</p>",
       [("der Umfang der Grundfläche, also \\(2\\cdot\\pi\\cdot r\\)", True, ""),
        ("die Mantellinie \\(s\\)", False, "Die Mantellinie ist der Radius des Kreisausschnitts."),
        ("der Radius \\(r\\)", False, "Der Bogen wird beim Aufrollen zum ganzen Rand der Grundfläche."),
        ("die Höhe \\(h\\)", False, "Die Höhe kommt im Netz gar nicht vor.")],
       route("Denk an den Hut: Der Bogen wird zum Rand der Grundfläche.", "Richtig."), single=True),
    mc("V-2", "<p>2. Welche Formel gilt für die Mantelfläche \\(M\\)?</p>",
       [("\\(M=\\pi\\cdot r\\cdot s\\)", True, ""),
        ("\\(M=\\pi\\cdot r^2\\)", False, "Das ist die Grundfläche."),
        ("\\(M=\\pi\\cdot r\\cdot h\\)", False, "Der Radius des Kreisausschnitts ist s, nicht h."),
        ("\\(M=2\\cdot\\pi\\cdot r\\cdot s\\)", False, "Das wäre doppelt so groß. Ein Kreisausschnitt ist ähnlich wie ein Dreieck: Bogen mal Radius, dann halbieren.")],
       route("Sieh dir die Stelle im Video noch einmal an.", "Richtig."), single=True),
    mc("V-3", "<p>3. Welche Formeln für den Oberflächeninhalt \\(O\\) sind richtig? (mehrere richtig)</p>",
       [("\\(O=G+M\\)", True, ""),
        ("\\(O=\\pi\\cdot r^2+\\pi\\cdot r\\cdot s\\)", True, ""),
        ("\\(O=\\pi\\cdot r\\cdot(r+s)\\)", True, ""),
        ("\\(O=\\pi\\cdot r\\cdot s\\)", False, "Das ist nur der Mantel. Der Boden fehlt."),
        ("\\(O=\\pi\\cdot r^2+\\pi\\cdot r\\cdot h\\)", False, "Für den Mantel brauchst du s, nicht h.")],
       route("Drei Antworten sind richtig. Klammere bei der dritten \\(\\pi\\cdot r\\) aus.", "Richtig. Weiter zu W."))])

stage("W", "W Wissen", 1220, 870, ["V", "P1"], [
    image("W-Bild", IMG_NETZ),
    dragtext("W-Herleitung", "<h3>W – Wissen: Woher kommt die Formel?</h3><p>Ziehe die passenden Begriffe in die Lücken.</p>\n",
             "Das Netz eines Kegels besteht aus einem *Kreis* (Grundfläche) und einem *Kreisausschnitt* (Mantel).\n\n"
             "Der Radius des Kreisausschnitts ist die *Mantellinie* s.\n\n"
             "Der Mantelbogen ist so lang wie der *Umfang* der Grundfläche, also 2 · π · r.\n\n"
             "Ein ganzer Kreis mit dem Radius s hätte den Umfang 2 · π · s und den Flächeninhalt *π · s²*.\n\n"
             "Der Mantel ist davon nur der Anteil r geteilt durch s. Deshalb gilt M = π · s² · r geteilt durch s = *π · r · s*.",
             route("Schau dir das Bild über der Aufgabe noch einmal an.", "Richtig."),
             distractors="*Rechteck* *Höhe* *2 · π · r · s*"),
    text("W-Merke", """
<p><strong>Merke:</strong> Für den Oberflächeninhalt eines Kegels mit Grundflächenradius \\(r\\) und Mantellinie \\(s\\) gilt</p>
<p>\\[ O=G+M=\\pi\\cdot r^2+\\pi\\cdot r\\cdot s=\\pi\\cdot r\\cdot(r+s) \\]</p>
<p><strong>Beispiel:</strong> Ein \\(4\\,\\text{cm}\\) hoher Kegel hat den Radius \\(2\\,\\text{cm}\\).</p>
<ol>
<li>Mantellinie: \\(s=\\sqrt{2^2+4^2}=\\sqrt{20}\\approx 4{,}47\\,\\text{cm}\\)</li>
<li>Mantel: \\(M=\\pi\\cdot 2\\cdot 4{,}47\\approx 28{,}10\\,\\text{cm}^2\\)</li>
<li>Grundfläche: \\(G=\\pi\\cdot 2^2\\approx 12{,}57\\,\\text{cm}^2\\)</li>
<li>Oberfläche: \\(O=G+M\\approx 40{,}67\\,\\text{cm}^2\\)</li>
</ol>
<p>Übertrage den Merksatz und das Beispiel in dein Heft. Weiter zu den Basisaufgaben (P1).</p>
""")])

# ================================================================ Basisaufgaben (Pflicht)
stage("P1", "P1 Aufg. 1", 1440, 870, ["W", "P2"], [blanks("P1", """
<h3>P1 – Aufgabe 1</h3>
<p>Berechne den Oberflächeninhalt der Kegel. Achte darauf, ob der Radius oder der Durchmesser gegeben ist.</p>
""", ["<p>a) O ≈ *%s:r = 5,1 cm und s = 12 cm* cm²</p>" % alt("273,98", "274", "273,97", "274,0"),
      "<p>b) O ≈ *%s:8 mm ist der Durchmesser. Wie groß ist r?* mm²</p>" % alt("175,93", "175,9", "175,92", "176"),
      "<p>c) O ≈ *%s:11,4 cm ist der Durchmesser.* cm²</p>" % alt("320,54", "320,5", "320,53", "320,6")],
    route("Prüfe: Hast du bei b) und c) den Durchmesser halbiert? Hast du G und M addiert?",
          "Richtig. Weiter zu P2."), img=IMG_A1)])

stage("P2", "P2 Aufg. 2", 1500, 680, ["P1", "T", "P3"], [blanks("P2", """
<h3>P2 – Aufgabe 2</h3>
<p>Berechne den Oberflächeninhalt des Kegels mit den gegebenen Maßen. Berechne zuerst die Mantellinie \\(s\\).</p>
""", ["<p>a) r = 3 cm, h = 4 cm: O ≈ *%s:Erst s = √(r² + h²), dann O = π · r · (r + s)* cm²</p>" % alt("75,4", "75,40", "75,39"),
      "<p>b) r = 1,5 cm, h = 2,5 cm: O ≈ *%s* cm²</p>" % alt("20,81", "20,8", "20,83", "20,82"),
      "<p>c) r = 5 cm, h = 5 cm: O ≈ *%s* cm²</p>" % alt("189,61", "189,6", "189,60", "189,59"),
      "<p>d) r = 1 cm, h = 3 cm: O ≈ *%s* cm²</p>" % alt("13,08", "13,07", "13,1")],
    route("Nutze den Abzweig T mit den Zwischenschritten.", "Richtig. Weiter zu P3."))])

stage("T", "T Zwischenschritte", 1310, 600, ["P2", "P3"], [blanks("T", """
<h3>T – Abzweig: Zwischenschritte zu Aufgabe 2</h3>
<p>Rechne Schritt für Schritt. Runde auf zwei Nachkommastellen.</p>
""", ["<p><strong>2a)</strong> r = 3 cm, h = 4 cm</p>",
      "<p>s = *%s:s = √(3² + 4²)* cm</p>" % alt("5", "5,0"),
      "<p>M = π · r · s ≈ *%s* cm²</p>" % alt("47,12", "47,1"),
      "<p>G = π · r² ≈ *%s* cm²</p>" % alt("28,27", "28,3"),
      "<p>O = G + M ≈ *%s* cm²</p>" % alt("75,4", "75,40", "75,39"),
      "<p><strong>2b)</strong> r = 1,5 cm, h = 2,5 cm</p>",
      "<p>s ≈ *%s:s = √(1,5² + 2,5²)* cm</p>" % alt("2,92", "2,9", "2,915"),
      "<p>M ≈ *%s* cm²</p>" % alt("13,74", "13,76", "13,7", "13,8"),
      "<p>G ≈ *%s* cm²</p>" % alt("7,07", "7,1"),
      "<p>O ≈ *%s* cm²</p>" % alt("20,81", "20,8", "20,83", "20,82")],
    route("Notiere, bei welchem Schritt du hängst, und geh weiter zu P3. Ich komme zu dir.",
          "Richtig. Rechne c) und d) in P2 noch einmal, dann weiter zu P3."))])

stage("P3", "P3 Aufg. 3", 1480, 470, ["P2", "T", "P4"], [
    blanks("P3", """
<h3>P3 – Aufgabe 3: Mantellinie berechnen</h3>
<p>Ein Kegel hat den Oberflächeninhalt \\(O=20\\,\\text{cm}^2\\) und den Radius \\(r=1\\,\\text{cm}\\). Berechne die Länge der Mantellinie \\(s\\).</p>
""", ["<p>s ≈ *%s:Setze ein: 20 = π · 1 · (1 + s). Teile zuerst durch π.* cm</p>" % alt("5,37", "5,4", "5,36", "5,366")],
        route("Setze alles in die Formel ein und stelle nach s um. Der Tipp im Feld hilft.", "Richtig.")),
    text("P3-Erklaeren", "<p><strong>Erkläre dein Vorgehen</strong> in deinem Heft in zwei bis drei Sätzen. Weiter zu P4.</p>")])

stage("P4", "P4 Aufg. 4 Schultüte", 1250, 470, ["P3", "P5"], [
    text("P4", """
<h3>P4 – Aufgabe 4: Schultüte</h3>
<p>Eine Schultüte soll eine Höhe von \\(45\\,\\text{cm}\\) und an der Öffnung einen Durchmesser von \\(20\\,\\text{cm}\\) haben. Sie soll von außen mit Glitzerfarbe bemalt werden.</p>
"""),
    mc("P4-Flaeche", "<p>Welche Fläche wird bemalt?</p>",
       [("nur die Mantelfläche", True, ""),
        ("Mantelfläche und Grundfläche", False, "Oben ist die Öffnung. Dort gibt es keine Fläche zum Bemalen."),
        ("nur die Grundfläche", False, "Die Grundfläche wäre die Öffnung oben.")],
       route("Stell dir eine echte Schultüte vor: Was ist oben?", "Richtig."), single=True),
    blanks("P4-Rechnung", "<p>Berechne, für welche Fläche die Farbe reichen muss.</p>",
           ["<p>r = *%s* cm</p>" % alt("10", "10,0"),
            "<p>s ≈ *%s:s = √(r² + h²)* cm</p>" % alt("46,1", "46,10", "46,09"),
            "<p>M ≈ *%s* cm²</p>" % alt("1448,2", "1448,20", "1448,27", "1448,3", "1448", "1447,96", "1448,0")],
           route("Prüfe: Hast du den Durchmesser halbiert und s mit Pythagoras berechnet?",
                 "Richtig. Weiter zu P5."))])

stage("P5", "P5 Aufg. 5 Stolperstelle", 1020, 470, ["P4", "F", "B1"], [
    text("P5", """
<h3>P5 – Aufgabe 5: Stolperstelle</h3>
<p>Ein Kegel hat die Höhe \\(10\\,\\text{cm}\\) und den Grundflächenradius \\(6\\,\\text{cm}\\). Henry berechnet den Oberflächeninhalt so:</p>
<p>\\(G=\\pi\\cdot(6\\,\\text{cm})^2\\approx 113{,}10\\,\\text{cm}^2\\)<br>
\\(M=\\pi\\cdot 6\\,\\text{cm}\\cdot 10\\,\\text{cm}\\approx 188{,}50\\,\\text{cm}^2\\)<br>
\\(O=G+M\\approx 301{,}60\\,\\text{cm}^2\\)</p>
"""),
    mc("P5-Fehler", "<p>Welche Aussagen über Henrys Rechnung stimmen? (mehrere richtig)</p>",
       [("Henry hat für \\(M\\) die Höhe \\(h\\) statt der Mantellinie \\(s\\) eingesetzt.", True, ""),
        ("Die Grundfläche \\(G\\) ist richtig berechnet.", True, ""),
        ("Henry hätte \\(G\\) nicht addieren dürfen.", False, "Zur Oberfläche gehört auch der Boden."),
        ("Für \\(G\\) muss man \\(2\\cdot\\pi\\cdot r\\) rechnen.", False, "Das ist der Umfang, keine Fläche.")],
       route("Vergleiche Henrys Rechnung mit der Formel M = π · r · s.", "Richtig.")),
    blanks("P5-Korrektur", "<p>Berechne den Oberflächeninhalt richtig.</p>",
           ["<p>s ≈ *%s:s = √(6² + 10²)* cm</p>" % alt("11,66", "11,7", "11,662"),
            "<p>M ≈ *%s* cm²</p>" % alt("219,82", "219,8", "219,78", "219,9", "220,5"),
            "<p>O ≈ *%s* cm²</p>" % alt("332,92", "332,9", "332,88", "333", "333,6")],
           route("War Aufgabe 5 nicht richtig? Dann geh zuerst zum Abzweig F, sonst weiter zu B1.",
                 "Richtig. Weiter zu den weiterführenden Aufgaben (B1)."))])

stage("F", "F Förderung", 900, 590, ["P5", "B1"], [blanks("F", """
<h3>F – Abzweig Förderung</h3>
<p>Erst ohne Pythagoras, dann mit. Der Rechenweg ist immer gleich: \\(s\\) bestimmen → \\(G\\) → \\(M\\) → \\(O=G+M\\).</p>
""", ["<p><strong>1.</strong> Kegel mit r = 2 cm und s = 5 cm (s ist gegeben!)</p>",
      "<p>G ≈ *%s:G = π · 2²* cm²</p>" % alt("12,57", "12,6", "12,56"),
      "<p>M ≈ *%s:M = π · 2 · 5* cm²</p>" % alt("31,42", "31,4", "31,41"),
      "<p>O ≈ *%s* cm²</p>" % alt("43,98", "44", "43,97", "44,0"),
      "<p><strong>2.</strong> Kegel mit r = 6 cm und h = 8 cm</p>",
      "<p>s = *%s:s = √(6² + 8²)* cm</p>" % alt("10", "10,0"),
      "<p>O ≈ *%s:O = π · 6 · (6 + 10)* cm²</p>" % alt("301,59", "301,6")],
    route("Notiere das auf deinem Zettel und geh weiter zu B1. Ich komme zu dir.",
          "Richtig. Weiter zu B1."))])

# ================================================================ Weiterführende Aufgaben (Stufe 2)
stage("B1", "B1 Aufg. 8 Turmdach", 780, 470, ["P5", "F", "B2"], [blanks("B1", """
<h3>B1 – Aufgabe 8: Turmdach</h3>
<p>Das Dach eines Turms hat die Form eines Kegels mit der Höhe \\(6\\,\\text{m}\\) und dem Grundflächenradius \\(3\\,\\text{m}\\). Berechne die Materialkosten für die Neueindeckung des Dachs, wenn der Preis pro Quadratmeter \\(87\\,€\\) beträgt.</p>
""", ["<p>Eingedeckte Fläche ≈ *%s:Gedeckt wird nur das Dach, also der Mantel.* m²</p>" % alt("63,22", "63,2", "63,23"),
      "<p>Kosten ≈ *%s* €</p>" % alt("5500,43", "5500,14", "5500,4", "5500,1", "5500", "5498,4", "5501,01")],
    route("Welche Fläche wird beim Dach gedeckt? Den Boden des Kegels gibt es beim Dach nicht.",
          "Richtig. Weiter zu B2."))])

stage("B2", "B2 Aufg. 9 Lampenschirm", 560, 470, ["B1", "B3"], [blanks("B2", """
<h3>B2 – Aufgabe 9: Lampenschirme aus Blech</h3>
<p>Eine Firma stellt aus Blech Lampenschirme her, die etwa die Form eines Kegels haben (ohne Boden). Die Höhe eines Lampenschirms beträgt \\(30\\,\\text{cm}\\), der Umfang der Grundfläche \\(80\\,\\text{cm}\\).</p>
<p>a) Ermittle, wie viel Blech für einen Lampenschirm benötigt wird. b) \\(1\\,\\text{cm}^2\\) Blech kostet \\(0{,}275\\,€\\). Berechne die Materialkosten für einen Lampenschirm.</p>
""", ["<p>r ≈ *%s:u = 2 · π · r, also r = u : (2 · π)* cm</p>" % alt("12,73", "12,7", "12,732"),
      "<p>s ≈ *%s* cm</p>" % alt("32,59", "32,6", "32,58"),
      "<p>a) Blech ≈ *%s* cm²</p>" % alt("1303,6", "1303,60", "1303,35", "1303,4", "1303,5", "1302,7", "1304"),
      "<p>b) Kosten ≈ *%s* €</p>" % alt("358,49", "358,5", "358,42", "358,4", "358,45", "358,46", "358,44")],
    route("Tipp: Aus dem Umfang bekommst du r, dann s mit Pythagoras. Der Lampenschirm hat keinen Boden.",
          "Richtig. Weiter zu B3."))])

stage("B3", "B3 Aufg. 10 Netze", 340, 470, ["B2", "B4"], [
    mc("B3", """<h3>B3 – Aufgabe 10: Kegelnetz oder nicht?</h3>
<p>Begründe, ob es sich um das Netz eines Kegels handelt. Vergleiche dazu die Länge des Kreisbogens mit dem Umfang des Kreises.</p>
<p>Welche Figuren sind Netze eines Kegels? (mehrere richtig)</p>""",
       [("a) Viertelkreis mit s = 4 cm und Kreis mit r = 1 cm", True, ""),
        ("b) Halbkreis mit s = 4 cm und Kreis mit r = 1 cm", False,
         "Der Bogen ist ½ · 2 · π · 4 ≈ 12,57 cm lang, der Kreisumfang nur 2 · π · 1 ≈ 6,28 cm."),
        ("c) Halbkreis mit s = 4 cm und Kreis mit r = 2 cm", True, "")],
       route("Berechne für jede Figur die Bogenlänge (Anteil des Vollkreises · 2 · π · s) und den Kreisumfang 2 · π · r.",
             "Richtig: Bei a) und c) ist der Bogen genauso lang wie der Kreisumfang. Notiere die Begründung im Heft. Weiter zu B4.")),
    image("B3-Bild", IMG_A10)])

stage("B4", "B4 Aufg. 11 Winkel", 130, 360, ["B3", "B5"], [
    dragtext("B4-a", """<h3>B4 – Aufgabe 11: Netz und Mittelpunktswinkel</h3>
<p>Um das Netz eines Kegels zu zeichnen, braucht man den Mittelpunktswinkel \\(\\alpha\\) des Kreisausschnitts.</p>
<p>a) Begründe, dass \\(\\alpha=\\frac{360^\\circ\\cdot r}{s}\\) gilt. Ziehe die passenden Begriffe in die Lücken.</p>
""", "Der Mantelbogen ist so lang wie der *Umfang* der Grundfläche: 2 · π · r.\n\n"
         "Ein ganzer Kreis mit dem Radius s hat den Umfang *2 · π · s* und den Mittelpunktswinkel *360°*.\n\n"
         "Der Kreisausschnitt ist davon der *Anteil* 2 · π · r geteilt durch 2 · π · s, gekürzt also r geteilt durch s.\n\n"
         "Deshalb ist auch der Winkel α dieser Anteil von 360°.",
            route("Vergleiche den Kreisausschnitt mit dem ganzen Kreis.", "Richtig."),
            distractors="*180°* *π · r²*"),
    blanks("B4-b", "<p>b) Ein Kegel hat die Höhe \\(7\\,\\text{cm}\\) und den Radius \\(3\\,\\text{cm}\\). Berechne \\(s\\), \\(\\alpha\\) und \\(O\\). Zeichne dann das Netz in dein Heft.</p>",
           ["<p>s ≈ *%s* cm</p>" % alt("7,62", "7,6", "7,616"),
            "<p>α ≈ *%s:α = 360° · r : s* °</p>" % alt("141,8", "141,73", "141,81", "141,7", "142", "141,9", "142,1"),
            "<p>O ≈ *%s* cm²</p>" % alt("100,05", "100,1", "100,09", "100,06", "100")],
           route("Erst s mit Pythagoras, dann in die Formeln einsetzen.", "Richtig. Weiter zu B5."))])

stage("B5", "B5 Aufg. 6 Prüfen", 300, 220, ["B4", "S1", "S2", "S3", "S4"], [
    blanks("B5", """
<h3>B5 – Aufgabe 6: Rechnen und prüfen</h3>
<p>Ein Kegel soll die Mantelfläche \\(M=1000\\,\\text{cm}^2\\) und die Mantellinie \\(s=10\\,\\text{cm}\\) haben. Berechne den Radius \\(r\\).</p>
""", ["<p>r ≈ *%s:M = π · r · s, also r = M : (π · s)* cm</p>" % alt("31,83", "31,8", "31,831")],
        route("Stelle M = π · r · s nach r um.", "Richtig gerechnet – aber schau genau hin!")),
    mc("B5-Pruefen", "<p>Kann es einen Kegel mit \\(M=1000\\,\\text{cm}^2\\) und \\(s=10\\,\\text{cm}\\) geben?</p>",
       [("Nein, denn der Radius wäre größer als die Mantellinie.", True, ""),
        ("Ja, man muss nur genau genug rechnen.", False,
         "Im Stützdreieck ist s die Hypotenuse. Die Hypotenuse ist immer die längste Seite."),
        ("Ja, der Kegel ist dann nur sehr flach.", False,
         "Auch ein sehr flacher Kegel hat einen Radius, der kleiner ist als s.")],
       route("Denk an das Stützdreieck aus h, r und s. Welche Seite ist die längste?",
             "Richtig: s ist die Hypotenuse, also muss r < s sein."), single=True),
    text("B5-Weiter", """
<p><strong>Für dein Heft:</strong> Ändere die Mantellinie so, dass es den Kegel geben kann (zum Beispiel \\(s=30\\,\\text{cm}\\)), und berechne dann \\(O\\).</p>
<p>Danach wählst du auf der Karte eine oder mehrere Profi-Aufgaben <strong>S1–S4</strong>.</p>
""")])

# ================================================================ Profi-Aufgaben zur Wahl (Stufe 3)
stage("S1", "S1 Radius gesucht", 820, 95, ["B5", "Ziel"], [blanks("S1", """
<h3>S1 – Aufgabe 7: Radius gesucht</h3>
<p>Berechne den Radius des Kegels. Setze in \\(O=\\pi\\cdot r\\cdot(r+s)\\) ein. Es entsteht eine quadratische Gleichung.</p>
""", ["<p>a) O = 219,91 cm², s = 9 cm: r ≈ *%s:Teile durch π und bringe alles auf eine Seite: r² + 9r − 70 = 0. Dann pq-Formel.* cm</p>" % alt("5", "5,0", "5,00"),
      "<p>c) O = 23 926,37 m², s = 80 m: r ≈ *%s:r² + 80r − O : π = 0* m</p>" % alt("56", "56,0", "56,00"),
      "<p>d) O = 225 m², s = 17,5 m: r ≈ *%s* m</p>" % alt("3,42", "3,4", "3,43")],
    route("Nur die positive Lösung ist ein Radius. Nutze die Tipps in den Feldern.",
          "Richtig. Geh zum Ziel oder wähle eine weitere Profi-Aufgabe."))])

stage("S2", "S2 Sandhaufen", 820, 185, ["B5", "Ziel"], [
    text("S2", """
<h3>S2 – Aufgabe 14: Sandhaufen</h3>
<p>Bei einem kegelförmigen Sandhaufen ist das Verhältnis Höhe : Radius \\(=3:5=0{,}6\\). Seine Mantellinie ist \\(5\\,\\text{m}\\) lang.</p>
"""),
    mc("S2-a", "<p>a) Schätze, in welchem Winkel der Sandhaufen ungefähr ansteigt. Prüfe deine Schätzung mit einer Zeichnung im Heft.</p>",
       [("α = 10°", False, "Zu flach: Bei 10° wäre die Höhe nur etwa ein Sechstel des Radius."),
        ("α = 31°", True, ""),
        ("α = 85°", False, "Das wäre fast senkrecht."),
        ("α = 113°", False, "Ein Steigungswinkel ist kleiner als 90°.")],
       route("Zeichne ein Dreieck mit 5 cm Grundseite und 3 cm Höhe.", "Richtig."), single=True),
    blanks("S2-b", "<p>b) Berechne Radius, Höhe und Mantelflächeninhalt des Sandhaufens.</p>",
           ["<p>r ≈ *%s:h = 0,6 · r einsetzen in r² + h² = 5²* m</p>" % alt("4,29", "4,3", "4,287", "4,28"),
            "<p>h ≈ *%s* m</p>" % alt("2,57", "2,6", "2,572", "2,58"),
            "<p>M ≈ *%s* m²</p>" % alt("67,35", "67,4", "67,39", "67,3", "67,24", "67,54")],
           route("Setze h = 0,6 · r in den Satz des Pythagoras ein.", "Richtig.")),
    blanks("S2-c", "<p>c) Für alle Kegel mit Höhe : Radius = 0,6 kann man \\(M\\) nur aus \\(r\\) berechnen. Gib die Formel an (Faktor auf zwei Nachkommastellen).</p>",
           ["<p>M ≈ *%s:s = √(r² + 0,36 · r²) = √1,36 · r* · r²</p>" % alt("3,66", "3,7", "3,664", "3,67")],
           route("Drücke zuerst s durch r aus.", "Richtig.")),
    mc("S2-d", "<p>d) Welche Art von Funktion beschreibt den Zusammenhang Radius r → Mantelflächeninhalt M?</p>",
       [("eine quadratische Funktion", True, ""),
        ("eine lineare Funktion", False, "r kommt im Quadrat vor."),
        ("eine antiproportionale Funktion", False, "Wird r größer, wird M auch größer.")],
       route("Schau auf deine Formel aus c).", "Richtig. Zeichne den Graphen in dein Heft."), single=True)])

stage("S3", "S3 Ausblick Stoffschirm", 820, 275, ["B5", "Ziel"], [
    text("S3", """
<h3>S3 – Aufgabe 15: Ausblick</h3>
<p>Aus der blauen Stofffläche soll ein Lampenschirm gefertigt werden (Angaben in cm).</p>
"""),
    image("S3-Bild", IMG_A15),
    mc("S3-a", "<p>a) Welche geometrische Form hat der fertige Schirm?</p>",
       [("die Form eines Kegelstumpfs (Kegel ohne Spitze)", True, ""),
        ("die Form eines Kegels", False, "Die Spitze (gestrichelter Teil) fehlt."),
        ("die Form eines Zylinders", False, "Oben und unten sind die Ränder verschieden groß.")],
       route("Stell dir vor, du rollst die Stofffläche auf.", "Richtig."), single=True),
    blanks("S3-bcd", "<p>b) Bestimme x. c) Berechne, wie viel Stoff mindestens benötigt wird. d) Bestimme den Anteil des gestrichelten Kreisausschnitts an der Gesamtfläche.</p>",
           ["<p>b) x = *%s:Die Bögen verhalten sich wie die Radien. 50 zu 100 = x zu (x + 70)* cm</p>" % alt("70", "70,0"),
            "<p>c) Stoff = *%s:Großer Kreisausschnitt minus kleiner. Fläche Kreisausschnitt = ½ · Bogen · Radius* cm²</p>" % alt("5250", "5250,0"),
            "<p>d) Anteil = *%s* %%</p>" % alt("25", "25,0")],
           route("Nutze die Tipps in den Feldern.", "Richtig.")),
    text("S3-f", "<p>f) <strong>Recherchiere</strong>, was ein Rotationskörper ist. Erläutere in deinem Heft, welche geometrische Figur den Lampenschirm erzeugt, wenn sie sich um eine Achse dreht.</p>")])

stage("S4", "S4 Kegel basteln", 820, 365, ["B5", "Ziel"], [
    blanks("S4", """
<h3>S4 – Aufgabe 13: Kegel basteln</h3>
<p>Stelle aus Zeichenkarton einen \\(8\\,\\text{cm}\\) hohen Kegel mit einem Grundflächenradius von \\(3\\,\\text{cm}\\) her.</p>
<p>Berechne zuerst die Maße für das Netz.</p>
""", ["<p>s ≈ *%s* cm</p>" % alt("8,54", "8,5", "8,544"),
      "<p>α ≈ *%s:α = 360° · r : s* °</p>" % alt("126,4", "126,41", "126,46", "126,47", "126,5", "126,3", "127", "126"),
      "<p>O ≈ *%s* cm²</p>" % alt("108,8", "108,80", "108,81", "108,79", "108,9")],
        route("Erst s mit Pythagoras, dann α wie in Aufgabe 11.", "Richtig.")),
    text("S4-Basteln", "<p>Zeichne das Netz mit Zirkel und Geodreieck: Kreisausschnitt mit Radius s und Winkel α, dazu den Grundkreis mit r = 3 cm. Plane Klebelaschen ein. Schneide aus und klebe den Kegel zusammen.</p>")])

stage("Ziel", "Ziel", 1250, 200, ["S1", "S2", "S3", "S4"], [{}], special="finish")

# ================================================================ Zusammenbau
index = {s["key"]: i for i, s in enumerate(S)}
for s in S:
    for n in s["nb"]:
        assert s["key"] in S[index[n]]["nb"], (s["key"], n)

W_PCT, H_PCT = 4.0, 6.4
elements, paths = [], []
for i, s in enumerate(S):
    el = {
        "id": "kegel-" + s["key"].lower(),
        "label": s["label"],
        "telemetry": {"x": str(round(s["cx"] / 16 - W_PCT / 2, 3)), "y": str(round(s["cy"] / 10 - H_PCT / 2, 3)),
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
                          "customVisuals": {"colorPath": "rgba(0, 0, 0, 0.7)", "pathWidth": "0.2",
                                            "pathStyle": "dotted"}})

# Etappenliste für karte_beschriften.py
with open(os.path.join(HERE, "bilder", "etappen.json"), "w", encoding="utf-8") as f:
    json.dump([{"code": s["key"], "cx": s["cx"], "cy": s["cy"], "nb": [index[n] for n in s["nb"]],
                "finish": s["special"] == "finish"} for s in S], f, ensure_ascii=False, indent=1)

ref = json.load(open(os.path.join(REF, "content", "content.json"), encoding="utf-8"))
END = """<p style="text-align: center;"><strong>Leitfrage:</strong> Wie viel Material braucht man für einen Kegel – und warum ist sein Mantel ein Kreisausschnitt?</p>
<p style="text-align: center;">Beantworte die Leitfrage in deinem Heft in höchstens drei Sätzen. Nutze die Wörter Mantellinie, Kreisausschnitt und Umfang.</p>
"""
hintergrund = "karte-beschriftet.jpg" if os.path.exists(os.path.join(HERE, "bilder", "karte-beschriftet.jpg")) else "karte.jpg"
content = {
    "showTitleScreen": False,
    "titleScreen": {"titleScreenIntroduction": "<p style=\"text-align: center;\"></p>"},
    "headline": "Oberflächeninhalt des Kegels",
    "gamemapSteps": {
        "backgroundImageSettings": {
            "backgroundColor": "rgb(176, 218, 144)",
            "backgroundImage": {"path": "images/" + hintergrund, "mime": "image/jpeg",
                                "copyright": {"license": "U"}, "width": 1600, "height": 1000}},
        "gamemap": {"elements": elements, "paths": paths},
    },
    "endScreen": {
        "noSuccess": {"endScreenTextNoSuccess": END},
        "success": {"endScreenTextSuccess": END},
        "overallFeedback": [{"from": 0, "to": 100}],
    },
    "visual": ref["visual"],
    "audio": ref["audio"],
    "behaviour": {"enableRetry": True, "enableSolutionsButton": False,
                  "map": {"showLabels": True, "roaming": "free"}},
    "l10n": ref["l10n"],
    "a11y": ref["a11y"],
}
content["l10n"]["restrictionStageProgressIs"] = "Der Fortschritt von Etappe @label ist @value."
content["l10n"]["restrictionStageProgressIsNot"] = "Der Fortschritt von Etappe @label ist nicht @value."

h5p = json.load(open(os.path.join(REF, "h5p.json"), encoding="utf-8"))
h5p["title"] = "Oberflächeninhalt des Kegels – Lernpfad"
h5p["language"] = "de"
h5p["license"] = "U"
h5p["preloadedDependencies"].append({"machineName": "H5P.Video", "majorVersion": "1", "minorVersion": "6"})

bilder = [hintergrund, "kegel-netz.png", "aufgabe1-kegel.png", "aufgabe10-netze.png",
          "aufgabe15-lampenschirm.png", "hut.png"]
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
    for root, dirs, files in os.walk(VIDEO_LIB):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            p = os.path.join(root, f)
            z.write(p, os.path.join("H5P.Video-1.6", os.path.relpath(p, VIDEO_LIB)))
print("geschrieben:", OUT, "Etappen:", len(elements), "Wege:", len(paths), "Hintergrund:", hintergrund)
