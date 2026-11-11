# Lernpfad „Volumen der Pyramide“ (H5P Game Map)

- `volumen-pyramide-gamemap.h5p` – fertige Datei zum Öffnen in Lumi
- `build.py` – erzeugt die Datei neu: `python3 build.py <entpackte Trapez-Referenz> volumen-pyramide-gamemap.h5p`
- `bilder/` – Karte und Skizzen (SVG-Quellen und gerenderte Bilder)

Inhalte nach dem Planungsdokument „H5P-Lernpfad: Volumen der Pyramide (Jg. 10, Lumi)“,
Bibliotheken und Einstellungen aus „Umfang und Flächeninhalt – Trapez“.

## Beschriftete Karte

- `bilder/karte-orientierung.png` – Orientierungskarte mit Kürzeln (D1, H1, P1, S1 …) und Legende, zum Ausdrucken oder Projizieren
- `bilder/karte-beschriftet.jpg` – derselbe Hintergrund mit Kürzeln, wird in der H5P verwendet (Lumi zeigt Etappennamen auf Touchgeräten nicht an)
- Neu erzeugen: `python3 karte_beschriften.py volumen-pyramide-gamemap.h5p`, dann in `bilder/`
  `node ../render.js '[["karte-beschriftet.svg","karte-beschriftet.jpg",1600,1000,"jpeg"],["karte-orientierung.svg","karte-orientierung.png",1600,1280,"png"]]'`
  und `build.py` erneut ausführen.
