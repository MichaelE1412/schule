#!/usr/bin/env python3
"""Baut den Lernpfad „Volumen der Pyramide“ als H5P Game Map.

Aufruf:  python3 build.py <Ordner mit entpackter Referenz-H5P> <Ausgabedatei.h5p>

Die Bibliotheken (H5P.GameMap 1.5 usw.) werden aus der Referenzdatei
„Umfang und Flächeninhalt – Trapez“ übernommen, die Inhalte stehen unten.
"""
import json
import os
import shutil
import sys
import uuid
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REF = sys.argv[1]
OUT = sys.argv[2]

NS = uuid.UUID("6f1c3a52-6b0e-4a43-9d6e-7b3f0f2c9a10")


def uid(name):
    return str(uuid.uuid5(NS, name))


# ---------------------------------------------------------------- Bausteine
def image_lib(path, w, h, alt, key):
    return {
        "library": "H5P.Image 1.1",
        "params": {
            "decorative": False,
            "contentName": "Bild",
            "expandImage": "Bild vergrößern",
            "minimizeImage": "Bild verkleinern",
            "alt": alt,
            "file": {"path": path, "mime": "image/png", "copyright": {"license": "U"},
                     "width": w, "height": h},
        },
        "metadata": {"contentType": "Image", "license": "U", "title": alt},
        "subContentId": uid("img-" + key),
    }


IMG_HA = ("images/stuetzdreieck-ha.png", 640, 480,
          "Quadratische Pyramide mit Stützdreieck aus h, h_a und a/2")
IMG_S = ("images/stuetzdreieck-s.png", 640, 480,
         "Rechteckige Pyramide mit Stützdreieck aus h, s und d/2")
IMG_Q = ("images/quader-pyramide.png", 640, 480,
         "Quader 5 cm × 3 cm × 6 cm mit Pyramide, deren Spitze auf der Deckfläche liegt")


def text(key, html):
    return {"contentType": {
        "params": {"text": html},
        "library": "H5P.AdvancedText 1.1",
        "metadata": {"contentType": "Text", "license": "U", "title": key},
        "subContentId": uid("txt-" + key)}}


def image(key, img):
    return {"contentType": image_lib(*img, key=key)}


def feedback(ranges):
    """ranges: Liste (von, bis, Text)"""
    return [{"from": a, "to": b, "feedback": t} for a, b, t in ranges]


def blanks(key, intro, questions, fb, img=None):
    p = {
        "media": {"disableImageZooming": False},
        "text": intro,
        "questions": questions,
        "overallFeedback": feedback(fb),
        "showSolutions": "Lösung anzeigen",
        "tryAgain": "Wiederholen",
        "checkAnswer": "Überprüfen",
        "submitAnswer": "Absenden",
        "notFilledOut": "Bitte fülle alle Lücken aus, um die Lösung ansehen zu können",
        "answerIsCorrect": "&#039;:ans&#039; ist korrekt",
        "answerIsWrong": "&#039;:ans&#039; ist falsch",
        "answeredCorrectly": "Korrekt beantwortet",
        "answeredIncorrectly": "Falsch beantwortet",
        "solutionLabel": "Korrekte Antwort:",
        "inputLabel": "Lücke @num von @total",
        "inputHasTipLabel": "Tipp verfügbar",
        "tipLabel": "Tipp",
        "behaviour": {
            "enableRetry": True, "enableSolutionsButton": False, "enableCheckButton": True,
            "autoCheck": False, "caseSensitive": False, "showSolutionsRequiresInput": True,
            "separateLines": False, "confirmCheckDialog": False, "confirmRetryDialog": False,
            "acceptSpellingErrors": False},
        "scoreBarLabel": "Du hast :num von :total Punkten erreicht.",
        "a11yCheck": "Die Antworten überprüfen. Die Eingaben werden als richtig, falsch oder unbeantwortet markiert.",
        "a11yShowSolution": "Die Lösung anzeigen. Die richtigen Lösungen werden in der Aufgabe angezeigt.",
        "a11yRetry": "Die Aufgabe wiederholen. Alle Eingaben werden zurückgesetzt und die Aufgabe wird erneut gestartet.",
        "a11yCheckingModeHeader": "Überprüfen-Modus aktiv",
        "confirmCheck": {"header": "Beenden?", "body": "Ganz sicher beenden?",
                         "cancelLabel": "Abbrechen", "confirmLabel": "Beenden"},
        "confirmRetry": {"header": "Wiederholen?", "body": "Ganz sicher wiederholen?",
                         "cancelLabel": "Abbrechen", "confirmLabel": "Bestätigen"},
    }
    if img:
        p["media"]["type"] = image_lib(*img, key=key)
    return {"contentType": {
        "params": p, "library": "H5P.Blanks 1.14",
        "metadata": {"contentType": "Fill in the Blanks", "license": "U", "title": key},
        "subContentId": uid("blk-" + key)}}


def mc(key, question, answers, fb, single=False):
    """answers: Liste (html, richtig, rückmeldung_bei_wahl)"""
    p = {
        "media": {"disableImageZooming": False},
        "question": question,
        "answers": [{"correct": c, "text": "<div>%s</div>\n" % t,
                     "tipsAndFeedback": {"tip": "", "chosenFeedback": f or "", "notChosenFeedback": ""}}
                    for t, c, f in answers],
        "overallFeedback": feedback(fb),
        "behaviour": {
            "enableRetry": True, "enableSolutionsButton": False, "enableCheckButton": True,
            "type": "single" if single else "auto", "singlePoint": False, "randomAnswers": True,
            "showSolutionsRequiresInput": True, "confirmCheckDialog": False,
            "confirmRetryDialog": False, "autoCheck": False, "passPercentage": 100,
            "showScorePoints": True},
        "UI": {
            "checkAnswerButton": "Überprüfen", "submitAnswerButton": "Absenden",
            "showSolutionButton": "Lösung anzeigen", "tryAgainButton": "Wiederholen",
            "tipsLabel": "Hinweis anzeigen", "scoreBarLabel": "Du hast :num von :total Punkten erreicht.",
            "tipAvailable": "Hinweis verfügbar", "feedbackAvailable": "Rückmeldung verfügbar",
            "readFeedback": "Rückmeldung vorlesen", "wrongAnswer": "Falsche Antwort",
            "correctAnswer": "Richtige Antwort", "shouldCheck": "Hätte gewählt werden müssen",
            "shouldNotCheck": "Hätte nicht gewählt werden sollen",
            "noInput": "Bitte antworte, bevor du die Lösung ansiehst",
            "a11yCheck": "Die Antworten überprüfen. Die Auswahlen werden als richtig, falsch oder fehlend markiert.",
            "a11yShowSolution": "Die Lösung anzeigen. Die richtigen Lösungen werden in der Aufgabe angezeigt.",
            "a11yRetry": "Die Aufgabe wiederholen. Alle Versuche werden zurückgesetzt und die Aufgabe wird erneut gestartet."},
        "confirmCheck": {"header": "Beenden?", "body": "Ganz sicher beenden?",
                         "cancelLabel": "Abbrechen", "confirmLabel": "Beenden"},
        "confirmRetry": {"header": "Wiederholen?", "body": "Ganz sicher wiederholen?",
                         "cancelLabel": "Abbrechen", "confirmLabel": "Bestätigen"},
    }
    return {"contentType": {
        "params": p, "library": "H5P.MultiChoice 1.16",
        "metadata": {"contentType": "Multiple Choice", "license": "U", "title": key},
        "subContentId": uid("mc-" + key)}}


def dragtext(key, task, textfield, fb):
    p = {
        "media": {"disableImageZooming": False},
        "taskDescription": task,
        "textField": textfield,
        "overallFeedback": feedback(fb),
        "checkAnswer": "Überprüfen", "submitAnswer": "Absenden", "tryAgain": "Wiederholen",
        "showSolution": "Lösung anzeigen", "dropZoneIndex": "Ablagefeld @index.",
        "empty": "Ablagefeld @index ist leer.",
        "contains": "Ablagefeld @index enthält ziehbaren Text @draggable.",
        "ariaDraggableIndex": "@index von @count ziehbaren Texten.",
        "tipLabel": "Tipp anzeigen", "correctText": "Richtig!", "incorrectText": "Falsch!",
        "resetDropTitle": "Ablagefelder zurücksetzen",
        "resetDropDescription": "Bist du sicher, dass du dieses Ablagefeld zurücksetzen möchtest?",
        "grabbed": "Ziehbarer Text wurde aufgenommen.", "cancelledDragging": "Ziehen abgebrochen.",
        "correctAnswer": "Korrekte Antwort:", "feedbackHeader": "Rückmeldung",
        "behaviour": {"enableRetry": True, "enableSolutionsButton": False,
                      "enableCheckButton": True, "instantFeedback": False},
        "scoreBarLabel": "Du hast :num von :total Punkten erreicht.",
        "a11yCheck": "Die Antworten überprüfen. Die Eingaben werden als richtig, falsch oder unbeantwortet markiert.",
        "a11yShowSolution": "Die Lösung anzeigen. Die richtigen Lösungen werden in der Aufgabe angezeigt.",
        "a11yRetry": "Die Aufgabe wiederholen. Alle Eingaben werden zurückgesetzt und die Aufgabe wird erneut gestartet.",
    }
    return {"contentType": {
        "params": p, "library": "H5P.DragText 1.10",
        "metadata": {"contentType": "Drag the Words", "license": "U", "title": key},
        "subContentId": uid("dt-" + key)}}


# Rückmeldungstexte
PARALLEL_FB = [(0, 99, "Notiere das auf deinem Diagnosezettel und geh weiter. Ich komme zu dir."),
               (100, 100, "Richtig! Geh zurück auf den Hauptweg.")]


def route(fehler, weiter):
    return [(0, 99, fehler), (100, 100, weiter)]


# Varianten für Dezimalzahlen: Komma und Punkt
def alt(*vals):
    out = []
    for v in vals:
        for x in (v, v.replace(",", ".")):
            if x not in out:
                out.append(x)
    return "/".join(out)


# ---------------------------------------------------------------- Etappen
# (Schlüssel, Beschriftung, x, y, Nachbarn, Inhalte, Startetappe)
S = []


def stage(key, label, x, y, neighbors, contents, start=False, special=None):
    S.append(dict(key=key, label=label, x=x, y=y, nb=neighbors, contents=contents,
                  start=start, special=special))


stage("Start", "Start", 4, 83, ["D0"], [text("Start", """
<h2>Volumen der Pyramide</h2>
<p><strong>Leitfrage:</strong> Was brauche ich, um das Volumen einer Pyramide zu berechnen – und wie komme ich an die Höhe, wenn sie nicht gegeben ist?</p>
<p><strong>Ablauf:</strong> Diagnose (10 Min.) → Pflicht → Wahlaufgaben. Lege deinen Diagnosezettel neben dich.</p>
<ul>
<li><strong>D</strong> = Diagnose, <strong>P</strong> = Pflicht (gelb), <strong>B</strong> = Stufe 2 (blau), <strong>S</strong> = Stufe 3 (Wahlaufgaben)</li>
<li><strong>H, T, F</strong> sind Abzweige. Geh nur dorthin, wenn dich eine Rückmeldung hinschickt.</li>
</ul>
<p>Formel: \\(V=\\frac{1}{3}\\cdot G\\cdot h\\)</p>
""")], start=True)

stage("D0", "D0 Hausaufgabe", 15, 83, ["Start", "D1"], [text("D0", """
<h3>D0 – Vergleich mit deiner Hausaufgabe (Aufg. 1)</h3>
<p>Vergleiche mit deiner Hausaufgabe:</p>
<ul><li>1a) \\(48\\,\\text{cm}^3\\)</li><li>1b) \\(32{,}9\\,\\text{cm}^3\\)</li><li>1c) \\(19{,}2\\,\\text{cm}^3\\)</li></ul>
<p><strong>Häufige Fehler:</strong> \\(\\frac{1}{3}\\) vergessen oder die Dreiecksfläche nicht halbiert.</p>
<p>Weiter zu <strong>D1</strong>.</p>
""")])

stage("D1", "D1 Höhe", 27, 83, ["D0", "H1", "D2"], [blanks("D1", """
<h3>D1 – Körperhöhe aus der Seitenhöhe</h3>
<p>Eine quadratische Pyramide hat die Grundkante \\(a=6\\,\\text{cm}\\) und die Seitenhöhe \\(h_a=5\\,\\text{cm}\\). Berechne die Körperhöhe \\(h\\).</p>
""", ["<p>h = *%s* cm</p>" % alt("4", "4,0")],
    route("Geh zuerst zum Abzweig H1.", "Richtig. Weiter zu D2."), img=IMG_HA)])

stage("H1", "H1 Hilfe Höhe", 35, 68, ["D1", "D2"], [
    text("H1", """
<h3>H1 – Abzweig Höhe</h3>
<p>Die Körperhöhe \\(h\\) steht senkrecht auf der Grundfläche und endet im Mittelpunkt. Die Seitenhöhe \\(h_a\\) liegt in der Seitenfläche.</p>
<p>Mit der halben Grundkante \\(\\frac{a}{2}\\) bilden beide ein rechtwinkliges Dreieck. Die Hypotenuse ist \\(h_a\\), also</p>
<p>\\[ h^2=h_a^2-\\left(\\frac{a}{2}\\right)^2 \\]</p>
<p><strong>Muster:</strong> \\(a=8\\,\\text{cm}\\), \\(h_a=5\\,\\text{cm}\\): \\(h^2=5^2-4^2=9\\), also \\(h=3\\,\\text{cm}\\).</p>
"""),
    image("H1-Bild", IMG_HA),
    blanks("H1-Aufgabe", "<p><strong>Parallelaufgabe:</strong> \\(a=10\\,\\text{cm}\\), \\(h_a=13\\,\\text{cm}\\).</p>",
           ["<p>h = *12* cm</p>"], PARALLEL_FB)])

stage("D2", "D2 Grundfläche", 44, 83, ["D1", "H1", "H2", "D3"], [blanks("D2", """
<h3>D2 – Grundfläche</h3>
<p>Die Grundfläche einer Pyramide ist ein rechtwinkliges Dreieck mit den Katheten \\(5\\,\\text{mm}\\) und \\(6\\,\\text{mm}\\). Berechne \\(G\\).</p>
""", ["<p>G = *15* mm²</p>"],
    route("Geh zuerst zum Abzweig H2.", "Richtig. Weiter zu D3."))])

stage("H2", "H2 Hilfe Grundfläche", 52, 68, ["D2", "D3"], [
    text("H2", """
<h3>H2 – Abzweig Grundfläche</h3>
<table border="1" cellpadding="4" style="border-collapse:collapse">
<tr><td>Quadrat</td><td>\\(a^2\\)</td></tr>
<tr><td>Rechteck</td><td>\\(a\\cdot b\\)</td></tr>
<tr><td>Dreieck</td><td>\\(\\frac{1}{2}\\cdot g\\cdot h_g\\)</td></tr>
<tr><td>Parallelogramm</td><td>\\(g\\cdot h\\)</td></tr>
<tr><td>Trapez</td><td>\\(\\frac{1}{2}\\cdot(a+c)\\cdot h\\)</td></tr>
<tr><td>Drachenviereck</td><td>\\(\\frac{1}{2}\\cdot e\\cdot f\\)</td></tr>
</table>
<p>Flächen haben Einheiten wie \\(\\text{cm}^2\\). Beim rechtwinkligen Dreieck sind die Katheten Grundseite und Höhe.</p>
"""),
    blanks("H2-Aufgabe", "<p><strong>Parallelaufgabe:</strong> Ein rechtwinkliges Dreieck hat die Katheten \\(4\\,\\text{cm}\\) und \\(7\\,\\text{cm}\\).</p>",
           ["<p>G = *14* cm²</p>"], PARALLEL_FB)])

stage("D3", "D3 Volumen", 61, 83, ["D2", "H2", "H3", "P1"], [
    blanks("D3", """
<h3>D3 – Volumen und Einheit</h3>
<p>Eine Pyramide hat \\(G=36\\,\\text{cm}^2\\) und \\(h=4\\,\\text{cm}\\). Berechne das Volumen.</p>
""", ["<p>V = *48*</p>"],
        route("Geh zuerst zum Abzweig H3.", "Richtig. Beantworte noch die Frage zur Einheit.")),
    mc("D3-Einheit", "<p>Welche Einheit hat das Volumen \\(V\\)?</p>",
       [("cm", False, "cm ist eine Längeneinheit."),
        ("cm²", False, "cm² ist eine Flächeneinheit."),
        ("cm³", True, "")],
       route("Geh zuerst zum Abzweig H3.", "Richtig. Weiter zu P1 (Pflicht)."), single=True)])

stage("H3", "H3 Hilfe Drittel/Einheit", 69, 68, ["D3", "P1"], [
    text("H3", """
<h3>H3 – Abzweig Drittel und Einheit</h3>
<p>Eine Pyramide hat ein Drittel des Volumens eines Prismas mit gleicher Grundfläche \\(G\\) und gleicher Höhe \\(h\\) (siehe Aufg. 16). Deshalb steht \\(\\frac{1}{3}\\) in der Formel:</p>
<p>\\[ V=\\frac{1}{3}\\cdot G\\cdot h \\]</p>
<p><strong>Einheiten:</strong> Länge cm · Fläche cm² · Volumen cm³</p>
"""),
    blanks("H3-Aufgabe", "<p><strong>Parallelaufgabe:</strong> \\(G=25\\,\\text{cm}^2\\), \\(h=6\\,\\text{cm}\\).</p>",
           ["<p>V = *50* cm³</p>"], PARALLEL_FB)])

stage("P1", "P1 Aufg. 3a (Pflicht)", 79, 83, ["D3", "H3", "P2"], [blanks("P1", """
<h3>P1 – Pflicht: Aufgabe 3a</h3>
<p>Eine quadratische Pyramide hat die Grundkante \\(a=5\\,\\text{cm}\\) und die Seitenhöhe \\(h_a=3\\,\\text{cm}\\). Berechne die Körperhöhe \\(h\\) und das Volumen \\(V\\). Runde auf zwei Nachkommastellen.</p>
""", ["<p>h ≈ *%s:Zeichne das Stützdreieck aus h, der halben Grundkante und h_a.* cm</p>" % alt("1,66", "1,7", "1,658"),
      "<p>V ≈ *%s* cm³</p>" % alt("13,8", "13,82", "13,83", "13,81")],
    route("Prüfe: Hast du h oder h_a eingesetzt? Und ist h_a die Hypotenuse?",
          "Richtig. Weiter zu P2."), img=IMG_HA)])

stage("P2", "P2 Aufg. 3b (Pflicht)", 89, 64, ["P1", "T", "P3"], [blanks("P2", """
<h3>P2 – Pflicht: Aufgabe 3b</h3>
<p>Eine Pyramide hat eine rechteckige Grundfläche mit \\(a=3{,}5\\,\\text{cm}\\) und \\(b=4{,}6\\,\\text{cm}\\). Die Seitenkanten sind \\(s=4\\,\\text{cm}\\) lang. Berechne das Volumen.</p>
""", ["<p>V ≈ *%s:s verläuft von einer Ecke zur Spitze. Welches rechtwinklige Dreieck enthält s und h?* cm³</p>"
      % alt("14,8", "14,84", "14,85", "14,86", "14,87", "14,9")],
    route("Nutze den Abzweig T mit den Zwischenschritten.", "Richtig. Weiter zu P3."), img=IMG_S)])

stage("T", "T Zwischenschritte 3b", 76, 52, ["P2", "P3"], [blanks("T", """
<h3>T – Abzweig: Zwischenschritte zu 3b</h3>
<p>\\(a=3{,}5\\,\\text{cm}\\), \\(b=4{,}6\\,\\text{cm}\\), \\(s=4\\,\\text{cm}\\). Rechne Schritt für Schritt. Runde auf zwei Nachkommastellen.</p>
""", ["<p>1. Diagonale der Grundfläche: d ≈ *%s:Pythagoras mit a und b* cm</p>" % alt("5,78", "5,8"),
      "<p>2. Halbe Diagonale: d : 2 ≈ *%s* cm</p>" % alt("2,89", "2,9"),
      "<p>3. Körperhöhe: h ≈ *%s:s ist die Hypotenuse* cm</p>" % alt("2,77", "2,8", "2,76"),
      "<p>4. Volumen: V ≈ *%s* cm³</p>" % alt("14,8", "14,84", "14,85", "14,86", "14,87", "14,9")],
    route("Notiere, bei welchem Schritt du hängst, und geh weiter zu P3. Ich komme zu dir.",
          "Richtig. Weiter zu P3."), img=IMG_S)])

stage("P3", "P3 Reflexion", 86, 38, ["P2", "T", "F", "B1"], [text("P3", """
<h3>P3 – Reflexion</h3>
<p>Schreibe in dein Heft: <strong>Warum brauchst du in 3b einen Rechenschritt mehr als in 3a?</strong></p>
<p>Benutze die Wörter <em>Körperhöhe</em>, <em>Seitenkante</em> und <em>Diagonale</em>.</p>
<p>&nbsp;</p>
<p><strong>War 3a oder 3b nicht richtig?</strong> Dann geh zuerst zum Abzweig <strong>F</strong>, sonst direkt zu Stufe 2 (<strong>B1</strong>).</p>
""")])

stage("F", "F Förderung", 73, 26, ["P3", "B1"], [blanks("F", """
<h3>F – Abzweig Förderung</h3>
<p>Gleiche Formel, glatte Zahlen, kein Pythagoras. Bearbeite im Buch <strong>Aufg. 2a</strong> und <strong>Aufg. 5a</strong> und trage deine Ergebnisse ein.</p>
""", ["<p>Aufg. 2a: V = *270* cm³</p>",
      "<p>Aufg. 5a: h = *12:Stelle die Formel nach h um: h = 3V : G* cm</p>"],
    route("Notiere das auf deinem Diagnosezettel und geh weiter zu B1. Ich komme zu dir.",
          "Richtig. Weiter zu Stufe 2 (B1)."))])

stage("B1", "B1 Aufg. 8 (blau)", 61, 38, ["P3", "F", "B2"], [blanks("B1", """
<h3>B1 – Stufe 2: Aufgabe 8 (andere Grundflächen)</h3>
<p>Bearbeite im Buch <strong>Aufg. 8</strong>. Berechne zuerst die Grundfläche, dann das Volumen. Runde auf eine Nachkommastelle.</p>
""", ["<p>8a) Parallelogramm: V ≈ *%s:Parallelogramm: G = g · h_g* cm³</p>" % alt("23,3", "23,33"),
      "<p>8b) Trapez: V ≈ *%s:Trapez: G = ½ · (a + c) · h* cm³</p>" % alt("76,8", "76,84"),
      "<p>8c) Drachenviereck: V ≈ *%s:Drachenviereck: G = ½ · e · f* cm³</p>" % alt("59,6", "59,58")],
    route("Prüfe die Formel für die Grundfläche – die Tipps in den Feldern helfen.",
          "Richtig. Weiter zu B2."))])

stage("B2", "B2 Aufg. 4 (blau)", 44, 38, ["B1", "B3"], [
    mc("B2-4a", "<h3>B2 – Stufe 2: Aufgabe 4 (Umkehrung)</h3><p>4a) Welche Umstellung der Formel \\(V=\\frac{1}{3}\\cdot G\\cdot h\\) nach \\(h\\) stimmt?</p>",
       [("\\(h=\\frac{3V}{G}\\)", True, ""),
        ("\\(h=\\frac{V}{3G}\\)", False, "Du musst mit 3 multiplizieren, um das Drittel aufzuheben."),
        ("\\(h=\\frac{3G}{V}\\)", False, "V und G sind vertauscht.")],
       route("Multipliziere beide Seiten mit 3 und teile dann durch G.", "Richtig."), single=True),
    blanks("B2-4b", "<p>4b) Bearbeite im Buch <strong>Aufg. 4b</strong>.</p>",
           ["<p>h = *15:h = 3V : G* cm</p>"],
           route("Setze in h = 3V : G ein.", "Richtig. Weiter zu B3."))])

stage("B3", "B3 Aufg. 9 Cheops (blau)", 27, 38, ["B2", "S1", "S2", "S3", "S4"], [
    blanks("B3-9a", """
<h3>B3 – Stufe 2: Aufgabe 9 (Cheops-Pyramide)</h3>
<p>Die Cheops-Pyramide hatte ursprünglich eine quadratische Grundfläche mit der Kantenlänge \\(230\\,\\text{m}\\) und eine Höhe von \\(147\\,\\text{m}\\). Heute misst die Grundkante \\(225\\,\\text{m}\\) und die Höhe \\(139\\,\\text{m}\\).</p>
<p>9a) Berechne beide Volumina.</p>
""", ["<p>ursprünglich: V = *2592100/2 592 100/2.592.100* m³</p>",
      "<p>heute: V = *2345625/2 345 625/2.345.625* m³</p>"],
        route("Prüfe: G = a² und das Drittel nicht vergessen.", "Richtig. Weiter mit 9b.")),
    mc("B3-9b", "<p>9b) Um wie viel Prozent hat das Volumen abgenommen?</p>",
       [("etwa 9,5 %", True, ""),
        ("etwa 10,5 %", False, "Du hast durch das heutige Volumen geteilt. Der Grundwert ist das ursprüngliche Volumen."),
        ("etwa 5,4 %", False, "Du hast nur die Höhen verglichen. Gefragt ist das Volumen.")],
       route("Lies die Rückmeldung zu deiner Antwort.", "Richtig."), single=True),
    text("B3-Validierung", """
<p><strong>Validieren:</strong> Auf Fotos der Cheops-Pyramide fehlt heute die Spitze. Ist es sinnvoll, mit einer vollständigen Pyramide von \\(139\\,\\text{m}\\) Höhe zu rechnen? Notiere einen Satz in dein Heft.</p>
<p>Danach wählst du auf der Karte eine Herausforderung <strong>S1–S4</strong>.</p>
""")])

stage("S1", "S1 Fehler finden", 6, 20, ["B3", "Ziel"], [
    text("S1", """
<h3>S1 – Fehler finden (Aufg. 14)</h3>
<p>Eine Pyramide hat eine rechteckige Grundfläche mit \\(a=3\\,\\text{cm}\\) und \\(b=5\\,\\text{cm}\\). Die Seitenhöhe zur Kante \\(a\\) ist \\(h_a=6\\,\\text{cm}\\).</p>
<p><strong>Piet rechnet:</strong></p>
<p>a) \\(h=\\sqrt{6^2-1{,}5^2}\\approx 6{,}2\\,\\text{cm}\\)<br>
b) \\(V=\\frac{1}{3}\\cdot 3\\cdot 5\\cdot 6=30\\,\\text{cm}^3\\)</p>
"""),
    mc("S1-Fehler", "<p>Welche Aussagen über Piets Rechnung stimmen? (mehrere richtig)</p>",
       [("Zu \\(h_a\\) gehört die halbe Kante \\(b\\), also \\(2{,}5\\,\\text{cm}\\), nicht \\(1{,}5\\,\\text{cm}\\).", True, ""),
        ("In b) hat Piet \\(h_a\\) statt \\(h\\) eingesetzt.", True, ""),
        ("\\(6{,}2\\,\\text{cm}\\) kann nicht stimmen: Die Körperhöhe ist immer kürzer als die Seitenhöhe.", True, ""),
        ("Piet hätte \\(\\frac{1}{2}\\) statt \\(\\frac{1}{3}\\) verwenden müssen.", False, "Die Formel mit ⅓ ist richtig."),
        ("Die Grundfläche ist falsch: Es müsste \\(G=3+5\\) heißen.", False, "G = a · b ist richtig.")],
       route("Schau dir das Stützdreieck genau an: Welche halbe Kante liegt unter h_a?", "Richtig.")),
    blanks("S1-Korrektur", "<p>Rechne richtig. Runde auf zwei Nachkommastellen.</p>",
           ["<p>h ≈ *%s* cm</p>" % alt("5,45", "5,5", "5,454"),
            "<p>V ≈ *%s* cm³</p>" % alt("27,3", "27,27", "27,25", "27,5")],
           route("Stützdreieck aus h, h_a und b : 2.", "Richtig. Geh zum Ziel oder wähle eine weitere Herausforderung."))])

stage("S2", "S2 Verändern", 19, 13, ["B3", "Ziel"], [
    dragtext("S2", "<h3>S2 – Verändern (Aufg. 10)</h3><p>Ziehe die passenden Wörter in die Lücken.</p>\n",
             "Wird die Grundfläche G verdoppelt und die Höhe h bleibt gleich, dann *verdoppelt* sich das Volumen.\n\n"
             "Wird die Höhe h halbiert und G bleibt gleich, dann *halbiert* sich das Volumen.\n\n"
             "Wird G verdreifacht, dann *verdreifacht* sich das Volumen.\n\n"
             "Wird G verdoppelt und gleichzeitig h halbiert, dann bleibt das Volumen *gleich*.",
             route("Setze in V = ⅓ · G · h Zahlen ein und vergleiche.", "Richtig.")),
    text("S2-Begründung", "<p><strong>Begründe mit der Formel</strong> \\(V=\\frac{1}{3}\\cdot G\\cdot h\\) in deinem Heft: Warum ändert sich \\(V\\) mit demselben Faktor wie \\(G\\) bzw. \\(h\\)?</p>")])

stage("S3", "S3 Knobeln", 35, 13, ["B3", "Ziel"], [
    text("S3", """
<h3>S3 – Knobeln (Aufg. 17)</h3>
<p>Ein Quader ist \\(5\\,\\text{cm}\\) lang, \\(3\\,\\text{cm}\\) breit und \\(6\\,\\text{cm}\\) hoch. Eine Pyramide hat die Bodenfläche des Quaders als Grundfläche. Ihre Spitze liegt irgendwo auf der gegenüberliegenden Deckfläche.</p>
"""),
    image("S3-Bild", IMG_Q),
    blanks("S3-Aufgabe", "<p>Berechne das Volumen der Pyramide.</p>",
           ["<p>V = *30:Wie hoch ist die Pyramide, wenn die Spitze auf der Deckfläche liegt?* cm³</p>"],
           route("Die Höhe der Pyramide ist die Höhe des Quaders.", "Richtig.")),
    mc("S3-Reflexion", "<p>Spielt es eine Rolle, welche Quaderfläche du als Grundfläche wählst (Spitze immer auf der gegenüberliegenden Fläche)?</p>",
       [("Nein, das Volumen ist immer \\(30\\,\\text{cm}^3\\).", True, ""),
        ("Ja, mit der größten Fläche als Grundfläche wird das Volumen am größten.", False,
         "Rechne nach: Wird G größer, wird h kleiner. G · h ist immer das Quadervolumen."),
        ("Ja, mit der kleinsten Fläche als Grundfläche wird das Volumen am größten.", False,
         "Rechne nach: G · h ist immer 90 cm³.")],
       route("Rechne alle drei Möglichkeiten aus.", "Richtig: Es ist immer ⅓ des Quadervolumens."), single=True)])

stage("S4", "S4 Volumen und Oberfläche", 51, 18, ["B3", "Ziel"], [blanks("S4", """
<h3>S4 – Volumen und Oberfläche (Aufg. 15)</h3>
<p>Eine Pyramide hat eine rechteckige Grundfläche. Die Kante \\(b\\) ist doppelt so lang wie \\(a\\). Die Körperhöhe ist \\(h=20\\,\\text{cm}\\), das Volumen \\(V=1080\\,\\text{cm}^3\\).</p>
<p>Berechne die Kanten, die beiden Seitenhöhen und den Oberflächeninhalt. Runde auf zwei Nachkommastellen.</p>
""", ["<p>a = *9:Setze b = 2a in V = ⅓ · a · b · h ein.* cm</p>",
      "<p>b = *18* cm</p>",
      "<p>Seitenhöhe zur Kante a: h<sub>a</sub> ≈ *%s:Stützdreieck aus h und b : 2* cm</p>" % alt("21,93", "21,9"),
      "<p>Seitenhöhe zur Kante b: h<sub>b</sub> ≈ *%s:Stützdreieck aus h und a : 2* cm</p>" % alt("20,5", "20,50"),
      "<p>O ≈ *%s:O = G + a · h_a + b · h_b* cm²</p>" % alt("728,4", "728,37", "728,1", "728,3", "728,5")],
    route("Nutze die Tipps in den Feldern.", "Richtig. Geh zum Ziel."))])

stage("Ziel", "Ziel", 27, 2, ["S1", "S2", "S3", "S4"], [{}], special="finish")

# ---------------------------------------------------------------- Zusammenbau
index = {s["key"]: i for i, s in enumerate(S)}
# Nachbarschaft symmetrisch prüfen
for s in S:
    for n in s["nb"]:
        assert s["key"] in S[index[n]]["nb"], (s["key"], n)

W, H = 4.0, 6.4  # Größe der Etappenmarker in % (Bild 1600 × 1000)
elements, paths = [], []
for i, s in enumerate(S):
    el = {
        "id": uid("stage-" + s["key"]),
        "label": s["label"],
        "telemetry": {"x": str(s["x"]), "y": str(s["y"]), "width": str(W), "height": str(H)},
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

ref = json.load(open(os.path.join(REF, "content", "content.json"), encoding="utf-8"))
END = """<p style="text-align: center;"><strong>Leitfrage:</strong> Was brauche ich, um das Volumen einer Pyramide zu berechnen – und wie komme ich an die Höhe, wenn sie nicht gegeben ist?</p>
<p style="text-align: center;">Beantworte die Leitfrage in deinem Heft in höchstens drei Sätzen. Nutze ein Beispiel aus Aufg. 3.</p>
"""
content = {
    "showTitleScreen": False,
    "titleScreen": {"titleScreenIntroduction": "<p style=\"text-align: center;\"></p>"},
    "headline": "Volumen der Pyramide",
    "gamemapSteps": {
        "backgroundImageSettings": {
            "backgroundColor": "rgb(241, 215, 156)",
            "backgroundImage": {"path": "images/karte.jpg", "mime": "image/jpeg",
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
h5p["title"] = "Volumen der Pyramide – Lernpfad"
h5p["language"] = "de"
h5p["license"] = "U"

# ---------------------------------------------------------------- Packen
if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("h5p.json", json.dumps(h5p, ensure_ascii=False))
    z.writestr("content/content.json", json.dumps(content, ensure_ascii=False))
    for name in ("karte.jpg", "stuetzdreieck-ha.png", "stuetzdreieck-s.png", "quader-pyramide.png"):
        z.write(os.path.join(HERE, "bilder", name), "content/images/" + name)
    for d in sorted(os.listdir(REF)):
        full = os.path.join(REF, d)
        if not os.path.isdir(full) or d == "content":
            continue
        for root, _, files in os.walk(full):
            for f in files:
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, REF))
print("geschrieben:", OUT, "Etappen:", len(elements), "Wege:", len(paths))
