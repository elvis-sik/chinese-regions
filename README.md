# China Regions

An Anki deck for learning the standard PRC statistical regions of China through Hanzi, pinyin, English names, member provinces, and crisp SVG map recall.

Published deck:

- [AnkiWeb shared deck](https://ankiweb.net/shared/info/159990073?cb=1774480687353)

The deck covers:

- North China
- East China
- South Central China
- Southwest China
- Northeast China
- Northwest China

## Why This Deck Works

- atlas-style locator maps instead of generic prompts
- clean member-province grouping
- compact border/coast/country cues
- bold Hanzi / pinyin / English recognition in both directions

## Sources

The deck is based on the region definitions and map files used on:

- [List of regions of China](https://en.wikipedia.org/wiki/List_of_regions_of_China)

The article's maps resolve to Wikimedia Commons SVG files, not just raster previews. The six region-specific SVGs are available as original vector files at nominal size `857 x 699`, and there is also a combined overview SVG.

The shared blank-map base requested for every note is:

- [File:China blank map.svg](https://commons.wikimedia.org/wiki/File:China_blank_map.svg)

## Verified SVG Sources

See [`data/raw/region_image_sources.csv`](data/raw/region_image_sources.csv) for the current manifest.
The seed note rows live in [`data/raw/china_regions_notes_seed.csv`](data/raw/china_regions_notes_seed.csv).
The note-field and card contract lives in [`CHINA_REGIONS_NOTE_TYPE.md`](CHINA_REGIONS_NOTE_TYPE.md).

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

The builder expects the required SVG files to be present locally and will stop with a clear error if the fetch step has not been run.

## Card Set

Current live cards:

1. Hanzi -> Pinyin
2. Hanzi -> English
3. English -> Chinese
4. Region -> list of member provinces
5. Members + blank map -> locator map
6. Region -> connections
7. Region + blank map -> locator map
8. Locator map -> region name

The visual direction is intentionally atlas-like rather than generic Anki:

- warm paper gradients instead of flat white
- jade / vermillion / gold accents
- editorial serif typography for names
- framed map panels for the image cards

## Repo Layout

- `data/raw/` contains the reviewed seed rows and media-source manifest
- `scripts/fetch_region_media.py` downloads the required SVG files from Wikimedia Commons
- `scripts/build_apkg.py` builds the final `.apkg`
- `media/regions/` is a generated local cache for deck media and is not committed
