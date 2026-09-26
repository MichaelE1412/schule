# Hilfekarten für Arbeitsblätter

## Struktur
```
index.html                 → Übersichtsseite mit Links zu allen Sets
brechung-reflexion.html     → Set 1
mechanik-kraefte.html       → Set 2 (Vorlage/Beispiel)
millikan-diagramm.html      → Set 3
vogelschutzgebiet.html      → Set 4
css/style.css               → gemeinsames Design für alle Sets
js/hints.js                 → gemeinsame Logik (Hinweise, Denkpause)
img/                        → Bilder für die Aufgaben
```

## Neues Kartenset hinzufügen
1. Eine bestehende `.html`-Datei kopieren (z. B. `mechanik-kraefte.html`) und umbenennen, z. B. `stromkreise.html`.
2. `<title>`, Fach-Zeile (`kicker`) und `<h1>` anpassen.
3. Pro Aufgabe einen Block `<section class="task" id="task1" data-label="Aufgabe 1"> … </section>` anlegen:
   - optional `<h2>Kurzer Titel</h2>`
   - optional Aufgabentext oder Bild (`<img src="img/DEINBILD.jpg" alt="…">`)
   - jeden Hinweis als `<div class="hint">…</div>` (die Nummer „Hinweis 1“ usw. wird automatisch ergänzt)
4. Die Auswahl-Buttons und der Button „Hinweis aufdecken“ entstehen automatisch.
5. Optional: Link in `index.html` ergänzen.
6. Datei ins GitHub-Repo hochladen (commit + push).

## Wartezeit zwischen den Hinweisen
Nach jedem aufgedeckten Hinweis gibt es eine Denkpause, bevor der nächste freigeschaltet wird.
Die Dauer (in Sekunden) steht pro Set im `<main>`-Tag:
```html
<main class="hilfekarten" data-wartezeit="60">
```
Soll eine einzelne Aufgabe abweichen, kann dort ebenfalls eine Wartezeit stehen:
```html
<section class="task" id="task3" data-label="Aufgabe 3" data-wartezeit="120">
```
`data-wartezeit="0"` schaltet die Pause ab.

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
