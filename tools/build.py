#!/usr/bin/env python3
"""Bundle template.html + data/ into one self-contained page: docs/index.html.

    python3 tools/build.py            # writes docs/index.html
    python3 tools/build.py --out kazan.html
"""
import argparse, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument("--out", default=os.path.join(ROOT, "docs", "index.html")); a = ap.parse_args()
html = open(os.path.join(ROOT, "template.html"), encoding="utf-8").read()
world = open(os.path.join(ROOT, "data", "world.topo.json"), encoding="utf-8").read().strip()
volc = json.load(open(os.path.join(ROOT, "data", "volcanoes.json"), encoding="utf-8"))
html = html.replace("/*WORLD*/{}", world, 1).replace("/*VOLCANOES*/[]", json.dumps(volc, ensure_ascii=False, separators=(",", ":")), 1)
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
open(a.out, "w", encoding="utf-8").write(html)
print(f"Built {a.out}: {len(volc)} volcanoes, {os.path.getsize(a.out)/1024:,.0f} KB")
