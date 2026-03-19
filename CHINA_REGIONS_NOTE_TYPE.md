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
6. `member_provinces`
   Comma-separated provincial-level divisions that belong to the region.
7. `connections`
   A compact geography field that lists:
   - which provincial-level divisions border which
   - cross-region province borders
   - coasts / seas
   - bordering countries where applicable

## Card Templates

1. `Hanzi -> Pinyin`
2. `Hanzi -> English`
3. `English -> Chinese`
4. `Region -> Member Provinces`
5. `Members + Blank -> Locator Map`
6. `Region -> Connections`
7. `Region + Blank -> Locator Map`
8. `Locator Map -> Region Name`

## Derived Build-Time Fields

The APKG builder derives a few helper fields from the source fields:

- a members-chip block parsed from `member_provinces`
- a connection list parsed from the remaining geography lines
- local `<img>` HTML for the blank map and locator map once media has been fetched

## Current Assumption

The seed data follows the six standard PRC statistical regions used on the English Wikipedia page and includes all relevant provincial-level divisions in that scheme, including Hong Kong, Macau, and Taiwan.

## Source Files

- [`data/raw/china_regions_notes_seed.csv`](/Users/elvis/Code/anki-studying/chinese-regions/data/raw/china_regions_notes_seed.csv)
- [`data/raw/region_image_sources.csv`](/Users/elvis/Code/anki-studying/chinese-regions/data/raw/region_image_sources.csv)
