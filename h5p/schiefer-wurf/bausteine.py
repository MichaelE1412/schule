"""Bausteine für H5P-Inhalte (Text, Lückentext, Multiple Choice, Drag the Words, Bild, Video).

Gemeinsam genutzt von build.py. Übernommen aus h5p/pyramide-volumen/build.py.
"""
import uuid

NS = uuid.UUID("2b8e0f7c-5a1d-4c6e-9f3a-8d7c6b5a4e31")


def uid(name):
    return str(uuid.uuid5(NS, name))


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


def dragtext(key, task, textfield, fb, distractors=""):
    p = {
        "media": {"disableImageZooming": False},
        "taskDescription": task,
        "textField": textfield,
        "distractors": distractors,
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


def video(key, url, title):
    """YouTube-Video (H5P.Video 1.6)."""
    return {"contentType": {
        "params": {
            "sources": [{"path": url, "mime": "video/YouTube", "copyright": {"license": "U"}}],
            "visuals": {"fit": True, "controls": True},
            "playback": {"autoplay": False, "loop": False},
            "l10n": {
                "name": "Video", "loading": "Videoplayer lädt ...",
                "noPlayers": "Es wurde kein Videoplayer gefunden, der dieses Format abspielen kann.",
                "noSources": "Für das Video ist keine Quelle angegeben.",
                "aborted": "Die Wiedergabe wurde abgebrochen.", "networkFailure": "Netzwerkfehler.",
                "cannotDecode": "Das Video kann nicht dekodiert werden.",
                "formatNotSupported": "Das Videoformat wird nicht unterstützt.",
                "mediaEncrypted": "Das Video ist verschlüsselt.", "unknownError": "Unbekannter Fehler.",
                "invalidYtId": "Ungültige YouTube-ID.",
                "unknownYtId": "Es wurde kein Video mit dieser YouTube-ID gefunden.",
                "restrictedYt": "Der Besitzer dieses Videos erlaubt das Einbetten nicht."},
            "a11y": [],
        },
        "library": "H5P.Video 1.6",
        "metadata": {"contentType": "Video", "license": "U", "title": title},
        "subContentId": uid("vid-" + key)}}
