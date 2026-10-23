# Kazan 火山

A volcano map game and field guide. *Kazan* (火山) is Japanese for volcano: fire mountain.

**Play it:** https://jtrouern.github.io/Kazan/

## What's in it

- **Quiz, two maps.** Ten volcanoes per game, twelve seconds each. Click where you think each one is; closer and faster scores more, up to 1,000 points.
  - **Ring of Fire:** 585 volcanoes on the subduction arcs around the Pacific, from the Andes and Cascades to Kamchatka, Japan, Indonesia, Melanesia, Tonga and New Zealand. Hotspot volcanoes such as Hawaii and the Galápagos are deliberately left out.
  - **World:** 833 volcanoes with a dated eruption, anywhere on Earth except the deep seafloor.
  - Better-known volcanoes (those with longer eruption records) come up more often, so the game teaches the important ones first.
- **Field guide.** All 1,215 volcanoes the Smithsonian lists as active in the last 12,000 years. Browse by continent and country, search by name, or click any dot on the map. Each entry shows a photo, type, last eruption, summit height, number of recorded eruptions, largest eruption (VEI), a description, and links to the Smithsonian page and Wikipedia.
- **Shareable links.** `…/#v=283030` opens Fujisan in the field guide. Every volcano's number is its Smithsonian volcano number.

## Folder layout

```
template.html          the game (HTML, CSS, JavaScript) with data placeholders
data/volcanoes.json    1,215 volcanoes, built by tools/prep_data.py
data/world.topo.json   country outlines (Natural Earth 1:50m, via world-atlas)
tools/prep_data.py     converts the Smithsonian snapshot into data/volcanoes.json
tools/build.py         bundles template + data into docs/index.html
docs/index.html        the built game, one self-contained file (GitHub Pages serves this)
```

## Rebuilding

```
python3 tools/build.py          # after editing template.html
```

To refresh the volcano data from a newer Smithsonian snapshot:

```
pip install rdata pandas
git clone --depth 1 https://github.com/moderndive/volcanoes
python3 tools/prep_data.py volcanoes/data
python3 tools/build.py
```

## Customizing

At the top of the script in `template.html`:

- `ROUNDS`, `SECONDS`, `REVEAL_MS`: places per game, seconds per place, how long the answer stays up.
- `MAPS`: each quiz map's title, description, `scale` (miles at which a guess scores zero; smaller is stricter), the `pool` of volcanoes it draws from, and the map rotation. A third map is one more entry, for example `japan:{title:"Japan", ..., pool:v=>v.cs.includes("Japan")}`.
- Colors and fonts are CSS variables at the top of `<style>`.

Which volcanoes count as Ring of Fire, and which continent each belongs to, are set in `tools/prep_data.py` (`RING`, `REGION_CONT`, `SUB_CONT`).

## Credits and license

- **Code:** MIT License (see `LICENSE`).
- **Volcano data, descriptions and photos:** Smithsonian Institution, Global Volcanism Program, *Volcanoes of the World* (snapshot of 3 May 2026), via the [volcanoes](https://github.com/moderndive/volcanoes) R package by Chester Ismay. Cite as: Global Volcanism Program, 2026. Volcanoes of the World. Smithsonian Institution. https://volcano.si.edu. Photos are loaded from volcano.si.edu and credited to their photographers on screen; they are not included in this repository.
- **Map outlines:** Natural Earth (public domain), packaged as world-atlas by Mike Bostock (ISC).
- **Libraries:** D3 and topojson-client (ISC), loaded from public CDNs. Fonts: Shippori Mincho and Zen Kaku Gothic New (SIL Open Font License), from Google Fonts.
