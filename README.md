# Hilfekarten für Arbeitsblätter

## Struktur
```
index.html                 → Übersichtsseite mit Links zu allen Sets
brechung-reflexion.html     → Set 1
mechanik-kraefte.html       → Set 2 (Vorlage/Beispiel)
css/style.css               → gemeinsames Design für alle Sets
js/hints.js                 → gemeinsame Logik (Hinweise anzeigen)
img/                        → Bilder für die Aufgaben
```

## Neues Kartenset hinzufügen
1. Eine bestehende `.html`-Datei kopieren (z. B. `mechanik-kraefte.html`) und umbenennen, z. B. `stromkreise.html`.
2. `<title>` und `<h1>` anpassen.
3. Buttons und `task`-Divs für die gewünschten Aufgaben ergänzen/entfernen (IDs wie `task1`, `task2`, ... müssen zu den `onclick`-Aufrufen passen).
4. Bilder in `img/` ablegen und im jeweiligen Set per `<img src="img/DEINBILD.jpg">` einbinden.
5. Optional: Link in `index.html` ergänzen.
6. Datei ins GitHub-Repo hochladen (commit + push).

## QR-Code pro Set
Nach dem Hochladen ist jedes Set unter einer eigenen URL erreichbar, z. B.:
```
https://DEINNAME.github.io/DEINREPO/brechung-reflexion.html
https://DEINNAME.github.io/DEINREPO/mechanik-kraefte.html
```
Diese URL kannst du direkt in einen QR-Code-Generator (z. B. qr-code-generator.com) eingeben.

## GitHub Pages aktivieren
1. Repo auf GitHub erstellen und alle Dateien hochladen.
2. Unter **Settings → Pages** als Quelle den `main`-Branch (Ordner `/root`) auswählen.
3. Nach kurzer Zeit ist die Seite unter `https://DEINNAME.github.io/DEINREPO/` erreichbar.
