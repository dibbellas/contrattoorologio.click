#!/usr/bin/env python3
"""Calcola gli hash sha256 di script e stili di index.html per la Content Security Policy.

Uso:  python3 tools/csp-hash.py
Sostituisci i valori 'sha256-...' in .htaccess e _headers con quelli stampati
(il primo in script-src, il secondo in style-src).
Chiunque può eseguirlo per verificare che gli hash pubblicati corrispondano al codice di questo repository.
"""
import base64, hashlib, pathlib, re

html = (pathlib.Path(__file__).resolve().parent.parent / "index.html").read_text(encoding="utf-8")
h = lambda s: "'sha256-" + base64.b64encode(hashlib.sha256(s.encode("utf-8")).digest()).decode() + "'"
for s in re.findall(r"<script>(.*?)</script>", html, re.S):
    print("script-src:", h(s))
for s in re.findall(r"<style>(.*?)</style>", html, re.S):
    print("style-src: ", h(s))

# Con l'opzione --write aggiorna da solo .htaccess, _headers e il meta CSP di index.html
import sys
if "--write" in sys.argv:
    root = pathlib.Path(__file__).resolve().parent.parent
    sc = [h(s) for s in re.findall(r"<script>(.*?)</script>", html, re.S)]
    st = [h(s) for s in re.findall(r"<style>(.*?)</style>", html, re.S)]
    for name in (".htaccess", "_headers", "index.html"):
        p = root / name
        t = p.read_text(encoding="utf-8")
        t = re.sub(r"script-src (?:'sha256-[^']+' ?)+", "script-src " + " ".join(sc) + " ", t)
        t = re.sub(r"style-src (?:'sha256-[^']+' ?)+", "style-src " + " ".join(st) + " ", t)
        t = t.replace("  ;", ";").replace(" ;", ";")
        p.write_text(t, encoding="utf-8")
        print("aggiornato", name)
