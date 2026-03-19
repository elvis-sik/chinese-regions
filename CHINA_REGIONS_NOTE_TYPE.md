# China Regions Note Type

This is the current note-field contract for the deck.

## Fields

1. `mandarin_name`
   The region name in Chinese characters, for example `华北`.
2. `blank_map`
   Shared base-map asset for every note. During data gathering this field stores the source SVG URL; the build step can later convert it into local Anki media.
3. `locator_map`
   Region-specific locator-map SVG. During data gathering this field stores the source SVG URL; the build step can later convert it into local Anki media.
4. `pinyin_name`
   Mandarin pinyin with tone marks, for example `Huáběi`.
5. `english_name`
   English region name, for example `North China`.
6. `connections`
   A compact geography field that lists:
   - which provincial-level divisions are members of the region
   - which provincial-level divisions border which
   - cross-region province borders
   - coasts / seas
   - bordering countries where applicable

## Current Assumption

The seed data follows the six standard PRC statistical regions used on the English Wikipedia page and includes all relevant provincial-level divisions in that scheme, including Hong Kong, Macau, and Taiwan.

## Source Files

- [`data/raw/china_regions_notes_seed.csv`](/Users/elvis/Code/anki-studying/chinese-regions/data/raw/china_regions_notes_seed.csv)
- [`data/raw/region_image_sources.csv`](/Users/elvis/Code/anki-studying/chinese-regions/data/raw/region_image_sources.csv)
