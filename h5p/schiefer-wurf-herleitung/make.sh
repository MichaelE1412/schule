#!/usr/bin/env bash
# Baut die H5P-Datei komplett neu.
# Aufruf: ./make.sh <entpackte Trapez-Referenz>
set -euo pipefail
cd "$(dirname "$0")"
REF="$1"
OUT=schiefer-wurf-herleitung.h5p

python3 gen_bilder.py
python3 build.py "$REF" "$OUT"          # schreibt bilder/etappen.json
python3 karte_beschriften.py
(cd bilder && node ../render.js '[
  ["bahnkurven.svg","bahnkurven.png",1260,500,"png"],
  ["schwimmer.svg","schwimmer.png",1000,470,"png"],
  ["vektor.svg","vektor.png",1140,420,"png"],
  ["dreieck.svg","dreieck.png",1040,400,"png"],
  ["bahn.svg","bahn.png",1000,440,"png"],
  ["boule.svg","boule.png",1240,650,"png"],
  ["kugelstoss.svg","kugelstoss.png",1140,420,"png"],
  ["karte.svg","karte.jpg",1600,1000,"jpeg"],
  ["karte-beschriftet.svg","karte-beschriftet.jpg",1600,1000,"jpeg"],
  ["karte-orientierung.svg","karte-orientierung.png",1600,1300,"png"]]')
python3 build.py "$REF" "$OUT"          # jetzt mit beschrifteter Karte
