#!/usr/bin/env python3
"""Convert the Smithsonian GVP snapshot (moderndive/volcanoes R package) into data/volcanoes.json.

    pip install rdata pandas
    git clone --depth 1 https://github.com/moderndive/volcanoes
    python3 tools/prep_data.py volcanoes/data
"""
import json, os, re, sys, warnings
warnings.filterwarnings("ignore")
import rdata

src = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
v = rdata.read_rda(os.path.join(src, "volcanoes.rda"))["volcanoes"]
e = rdata.read_rda(os.path.join(src, "eruptions.rda"))["eruptions"]

# Ring of Fire = the subduction arcs around the Pacific rim (hotspots like Hawaii and Galapagos excluded)
RING = {
    "Alaska Peninsula Volcanic Arc", "Aleutian Ridge Volcanic Arc", "Garibaldi Volcanic Arc", "High Cascades Volcanic Arc",
    "Wrangell Volcanic Arc", "Central America Volcanic Arc", "Chiapanecan Volcanic Arc", "Trans-Mexican Volcanic Arc",
    "Austral Andean Volcanic Arc", "Central Andean Volcanic Arc", "Northern Andean Volcanic Arc", "Southern Andean Volcanic Arc",
    "Central Kamchatka Volcanic Arc", "Eastern Kamchatka Volcanic Arc", "Izu Volcanic Arc", "Kuril Volcanic Arc",
    "Mariana Volcanic Arc", "Northeast Japan Volcanic Arc", "Ogasawara Volcanic Arc",
    "Eastern Philippine Volcanic Arc", "Halmahera Volcanic Arc", "Luzon Volcanic Arc", "Mindanao Volcanic Province",
    "Nankai Volcanic Arc", "Negros-Sulu Volcanic Arc", "Ryukyu Volcanic Arc", "Sangihe Volcanic Arc",
    "Andaman Volcanic Province", "Inner Banda Volcanic Arc", "Sunda Volcanic Arc",
    "Bismarck Sea Volcanic Province", "Bismarck Volcanic Arc", "Bougainville Volcanic Arc", "Fiji Volcanic Arc",
    "Solomon Volcanic Province", "Trobriand Volcanic Province", "Vanuatu Volcanic Arc",
    "Middle Kermadec Volcanic Arc", "Northeast Lau Basin Volcano Group", "Northern Kermadec Volcanic Arc",
    "Southern Kermadec Volcanic Arc", "Taupo Volcanic Arc", "Tofua Volcanic Arc", "Western North Island Volcanic Province",
}
REGION_CONT = {
    "Antarctic-Scotia Volcanic Regions": "Antarctica", "Arabia-Central Asia Volcanic Regions": "Asia",
    "Atlantic Ocean Volcanic Regions": "Europe", "Eastern Africa Volcanic Regions": "Africa",
    "Eastern Asia Volcanic Regions": "Asia", "Eastern Australia Volcanic Regions": "Oceania",
    "Eastern Pacific Volcanic Regions": "Oceans", "European Volcanic Regions": "Europe",
    "Middle America-Caribbean Volcanic Regions": "North America", "North America Volcanic Regions": "North America",
    "Northern Africa Volcanic Regions": "Africa", "Northwestern Pacific Volcanic Regions": "Asia",
    "Somalian-Antarctic Volcanic Regions": "Oceans", "South America Volcanic Regions": "South America",
    "Southern Pacific Volcanic Regions": "Oceania", "Southwestern Pacific Volcanic Regions": "Oceania",
    "Sunda-Banda Volcanic Regions": "Asia", "Tonga-Kermadec Volcanic Regions": "Oceania",
    "Western Pacific Volcanic Regions": "Asia",
}
SUB_CONT = {
    "Central Mid-Atlantic Rift Volcanic Province": "Oceans", "Southern Atlantic Volcano Group": "Oceans",
    "Hawaiian-Emperor Hotspot Volcano Group": "Oceania", "Galapagos Hotspot Volcano Group": "South America",
    "Northern Galapagos Volcanic Province": "South America", "Gulf of California Rift Volcanic Province": "North America",
    "Mariana Volcanic Arc": "Oceania", "Madagascar-Comoros Volcanic Province": "Africa",
    "Reunion Hotspot Volcano Group": "Africa", "Pacific-Antarctic Ridge Volcanic Province": "Oceans",
    "Southern East Pacific Rise Volcanic Province": "Oceans", "Western Anatolian Volcanic Province": "Asia",
}
RENAME = {"Turkiye": "Türkiye", "Undersea Features": "Undersea features", "Union of the Comoros": "Comoros"}


def countries(c):
    m = re.match(r"(.+?) - (?:administered|claimed) by (.+)", c)
    if m:
        return [m.group(2), m.group(1)] if "administered" in c else [m.group(1), m.group(2)]
    return [RENAME.get(x.strip(), x.strip()) for x in c.split("-")]


e = e[e.eruption_category == "Confirmed Eruption"]
stats = {}
for vn, g in e.groupby("volcano_number"):
    vei = g.vei.dropna()
    stats[int(vn)] = (len(g), int(vei.max()) if len(vei) else None)

out = []
for _, r in v.iterrows():
    vn = int(r.volcano_number)
    c = str(r.country)
    photo = r.primary_photo_link if isinstance(r.primary_photo_link, str) else ""
    m = re.search(r"/(GVP-\d+)\.jpg$", photo)
    y = r.last_eruption_year
    ne, vei = stats.get(vn, (0, None))
    rec = {
        "id": vn, "n": str(r.volcano_name), "c": " / ".join(countries(c)) if " - " not in c else c.replace("Turkiye", "Türkiye"),
        "cs": countries(c), "t": str(r.primary_volcano_type).replace("(es)", "").replace("(s)", "").rstrip("?"),
        "y": None if y != y or y is None else int(y), "ev": str(r.evidence_category),
        "lat": round(float(r.latitude), 3), "lon": round(float(r.longitude), 3),
        "el": None if r.elevation != r.elevation else int(r.elevation), "sr": str(r.subregion),
        "ct": SUB_CONT.get(str(r.subregion), REGION_CONT[str(r.region)]),
        "rf": str(r.subregion) in RING, "s": str(r.geological_summary).strip(),
        "ne": ne, "vei": vei,
    }
    if m:
        rec["ph"] = m.group(1)
        rec["pc"] = str(r.primary_photo_caption).strip() if isinstance(r.primary_photo_caption, str) else ""
        rec["pr"] = str(r.primary_photo_credit).strip() if isinstance(r.primary_photo_credit, str) else ""
    out.append(rec)
out.sort(key=lambda x: x["n"])
path = os.path.join(ROOT, "data", "volcanoes.json")
json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
quiz = [x for x in out if x["ev"] in ("Eruption Observed", "Eruption Dated")]
print(f"{len(out)} volcanoes ({sum(x['rf'] for x in out)} Ring of Fire); quiz pool {len(quiz)} "
      f"({sum(x['rf'] for x in quiz)} ring); photos {sum('ph' in x for x in out)}; {os.path.getsize(path)/1024:.0f} KB")
from collections import Counter
print(Counter(x["ct"] for x in out))
