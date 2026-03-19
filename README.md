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

## Verified SVG Sources

See [`data/raw/region_image_sources.csv`](/Users/elvis/Code/anki-studying/chinese-regions/data/raw/region_image_sources.csv) for the current manifest.

Highlights:

- The main six region maps are available as SVG and appear suitable for deck use.
- A combined [`Regions_of_China.svg`](https://commons.wikimedia.org/wiki/File:Regions_of_China.svg) is also available for overview cards.
- Wikimedia also hosts separate `China location map - ...` PNG files, but those are lower-value fallback assets because they are raster only.

## Caveats

- `Northwest_China.svg` currently carries a Commons update note about disputed-area rendering around Aksai Chin, so it is usable but worth one manual visual review before final deck export.
- `Northeast_China.svg` uses a lighter shade for Inner Mongolian areas that are sometimes included in the Northeast revitalization plan.
- `East_China.svg` and the combined overview use lighter shading for Taiwan / claimed-but-not-controlled areas.

## Suggested Next Step

If you want, the next pass can:

1. download the SVGs into `media/regions/`
2. normalize filenames and attribution metadata
3. set up the first note model / deck build script
