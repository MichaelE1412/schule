#!/usr/bin/env python3
"""Prüft eine .h5p-Datei: Enthält ein Textfeld HTML-Tags, die laut semantics.json
der jeweiligen Bibliothek nicht erlaubt sind? (Lumi/H5P entfernt solche Tags beim Import.)

Aufruf: python3 pruefe_tags.py datei.h5p [...]
"""
import json
import re
import sys
import zipfile



def semantics(z, lib):
    name, ver = lib.split(" ")
    pfad = f"{name}-{ver}/semantics.json"
    return json.loads(z.read(pfad)) if pfad in z.namelist() else []


def pruefe(z, fields, params, lib, pfad, fehler):
    for fld in fields:
        if not isinstance(fld, dict) or fld.get("name") not in params:
            continue
        wert = params[fld["name"]]
        typ = fld.get("type")
        if typ == "text" and isinstance(wert, str) and "tags" in fld:
            erlaubt = set(fld["tags"]) | {"p", "br", "div", "span"}
            if "table" in erlaubt:
                erlaubt |= {"tr", "td", "th", "thead", "tbody", "tfoot"}
            if "ul" in erlaubt or "ol" in erlaubt:
                erlaubt.add("li")
            if "h2" in erlaubt or "h3" in erlaubt:
                erlaubt |= {"h2", "h3"}
            gefunden = {t.lower() for t in re.findall(r"<\s*([a-zA-Z0-9]+)", wert)}
            falsch = gefunden - erlaubt
            if falsch:
                fehler.append(f"{lib} · {pfad}/{fld['name']}: nicht erlaubt {sorted(falsch)}")
        elif typ == "group" and isinstance(wert, dict):
            pruefe(z, fld.get("fields", []), wert, lib, pfad + "/" + fld["name"], fehler)
        elif typ == "group" and len(fld.get("fields", [])) == 1 and not isinstance(wert, dict):
            pruefe(z, fld["fields"], {fld["fields"][0]["name"]: wert}, lib, pfad, fehler)
        elif typ == "list" and isinstance(wert, list):
            sub = fld.get("field", {})
            for i, eintrag in enumerate(wert):
                pruefe(z, [sub], {sub.get("name"): eintrag}, lib, f"{pfad}/{fld['name']}[{i}]", fehler)
        elif typ == "library" and isinstance(wert, dict) and "library" in wert:
            pruefe(z, semantics(z, wert["library"]), wert.get("params", {}), wert["library"],
                   pfad + "/" + fld["name"], fehler)


for datei in sys.argv[1:]:
    with zipfile.ZipFile(datei) as z:
        h5p = json.loads(z.read("h5p.json"))
        content = json.loads(z.read("content/content.json"))
        haupt = next(d for d in h5p["preloadedDependencies"] if d["machineName"] == h5p["mainLibrary"])
        lib = f'{haupt["machineName"]} {haupt["majorVersion"]}.{haupt["minorVersion"]}'
        fehler = []
        pruefe(z, semantics(z, lib), content, lib, "", fehler)
    print(f"== {datei}: {len(fehler)} Problem(e)")
    for f in fehler:
        print("  ", f)
