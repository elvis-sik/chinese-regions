# chinese-regions

This repository is a scaffold for an Anki deck about the standard PRC statistical regions of China:

- North China
- East China
- South Central China
- Southwest China
- Northeast China
- Northwest China

## Status

The region images on the English Wikipedia page below are usable as high-quality SVG sources:

- [List of regions of China](https://en.wikipedia.org/wiki/List_of_regions_of_China)

The article's maps resolve to Wikimedia Commons SVG files, not just raster previews. The six region-specific SVGs are all available as original vector files at nominal size `857 x 699`, and there is also a combined overview SVG.

The shared blank-map base requested for every note is:

- [File:China blank map.svg](https://commons.wikimedia.org/wiki/File:China_blank_map.svg)

## Verified SVG Sources

See [`data/raw/region_image_sources.csv`](/Users/elvis/Code/anki-studying/chinese-regions/data/raw/region_image_sources.csv) for the current manifest.
The first seeded deck rows live in [`data/raw/china_regions_notes_seed.csv`](/Users/elvis/Code/anki-studying/chinese-regions/data/raw/china_regions_notes_seed.csv).
The field contract lives in [`CHINA_REGIONS_NOTE_TYPE.md`](/Users/elvis/Code/anki-studying/chinese-regions/CHINA_REGIONS_NOTE_TYPE.md).

Highlights:

- The main six region maps are available as SVG and appear suitable for deck use.
- A combined [`Regions_of_China.svg`](https://commons.wikimedia.org/wiki/File:Regions_of_China.svg) is also available for overview cards.
- Wikimedia also hosts separate `China location map - ...` PNG files, but those are lower-value fallback assets because they are raster only.

## Caveats

- `Northwest_China.svg` currently carries a Commons update note about disputed-area rendering around Aksai Chin, so it is usable but worth one manual visual review before final deck export.
- `Northeast_China.svg` uses a lighter shade for Inner Mongolian areas that are sometimes included in the Northeast revitalization plan.
- `East_China.svg` and the combined overview use lighter shading for Taiwan / claimed-but-not-controlled areas.

## Build Workflow

Install the deck-building dependencies:

```sh
uv sync --extra deck
```

Fetch the blank map and region locator SVGs:

```sh
.venv/bin/python scripts/fetch_region_media.py
```

Build the Anki package:

```sh
.venv/bin/python scripts/build_apkg.py
```

Output:

- `out/chinese-regions.apkg`

## Card Set

Current planned cards:

1. Hanzi -> Pinyin
2. Hanzi -> English
3. English -> Chinese
4. Region -> list of member provinces
5. Members + blank map -> locator map
6. Region -> connections
7. Region + blank map -> locator map
8. Locator map -> region name

The current visual direction is intentionally atlas-like rather than generic Anki:

- warm paper gradients instead of flat white
- jade / vermillion / gold accents
- editorial serif typography for names
- framed map panels for the image cards
