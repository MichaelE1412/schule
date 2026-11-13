#!/usr/bin/env bash
# Baut den Lernpfad komplett neu.
# Aufruf: ./make.sh <entpackte Trapez-Referenz> <Ordner H5P.Video 1.6.66>
set -euo pipefail
cd "$(dirname "$0")"
REF="$1"
VIDEO="$2"
OUT=oberflaeche-kegel-gamemap.h5p

python3 gen_bilder.py
python3 build.py "$REF" "$VIDEO" "$OUT"          # schreibt bilder/etappen.json
python3 karte_beschriften.py
(cd bilder && node ../render.js '[
  ["kegel-netz.svg","kegel-netz.png",960,480,"png"],
  ["aufgabe1-kegel.svg","aufgabe1-kegel.png",860,420,"png"],
  ["aufgabe10-netze.svg","aufgabe10-netze.png",1060,490,"png"],
  ["aufgabe15-lampenschirm.svg","aufgabe15-lampenschirm.png",800,460,"png"],
  ["hut.svg","hut.png",820,470,"png"],
  ["karte.svg","karte.jpg",1600,1000,"jpeg"],
  ["karte-beschriftet.svg","karte-beschriftet.jpg",1600,1000,"jpeg"],
  ["karte-orientierung.svg","karte-orientierung.png",1600,1330,"png"]]')
python3 build.py "$REF" "$VIDEO" "$OUT"          # jetzt mit beschrifteter Karte
