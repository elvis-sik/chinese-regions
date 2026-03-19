#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
from pathlib import Path

import genanki


REPO_ROOT = Path(__file__).resolve().parents[1]
NOTES_CSV = REPO_ROOT / "data/raw/china_regions_notes_seed.csv"
OUTPUT_APKG = REPO_ROOT / "out/chinese-regions.apkg"
MEDIA_DIR = REPO_ROOT / "media/regions"
MODEL_ID = 1_893_420_011
DECK_ID = 1_893_420_012
MODEL_SCHEMA_VERSION = 3

BLANK_MAP_FILENAME = "china_blank_map.svg"

LOCATOR_URL_TO_FILENAME = {
    "https://commons.wikimedia.org/wiki/Special:FilePath/North_China.svg": "north_china_locator.svg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/East_China.svg": "east_china_locator.svg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/South_Central_China.svg": "south_central_china_locator.svg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Southwest_China.svg": "southwest_china_locator.svg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Northeast_China.svg": "northeast_china_locator.svg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Northwest_China.svg": "northwest_china_locator.svg",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def split_connection_lines(value: str) -> list[str]:
    return [piece.strip() for piece in (value or "").split("<br>") if piece.strip()]


def split_csv_like_values(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split(",") if part.strip()]


def html_list(items: list[str], klass: str) -> str:
    if not items:
        return ""
    lis = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f'<ul class="{klass}">{lis}</ul>'


def html_member_chips(items: list[str]) -> str:
    if not items:
        return ""
    chips = "".join(f'<span class="member-chip">{html.escape(item)}</span>' for item in items)
    return f'<div class="member-chips">{chips}</div>'


def html_connection_rows(lines: list[str]) -> str:
    if not lines:
        return ""
    rows: list[str] = []
    for line in lines:
        if ":" in line:
            region, neighbors = line.split(":", 1)
            rows.append(
                '<div class="connection-row">'
                f'<div class="connection-region">{html.escape(region.strip())}</div>'
                f'<div class="connection-neighbors">{html.escape(neighbors.strip())}</div>'
                "</div>"
            )
        else:
            rows.append(f'<div class="connection-row"><div class="connection-neighbors">{html.escape(line)}</div></div>')
    return '<div class="connection-rows">' + "".join(rows) + "</div>"


def make_map_html(filename: str, alt_text: str, klass: str) -> str:
    return f'<img class="{klass}" src="{filename}" alt="{html.escape(alt_text)}">'


def collect_media(rows: list[dict[str, str]]) -> list[str]:
    out: list[str] = []
    blank = MEDIA_DIR / BLANK_MAP_FILENAME
    if blank.exists():
        out.append(str(blank))
    for row in rows:
        locator_url = (row.get("locator_map") or "").strip()
        filename = LOCATOR_URL_TO_FILENAME.get(locator_url)
        if not filename:
            continue
        path = MEDIA_DIR / filename
        if path.exists():
            out.append(str(path))
    return sorted(dict.fromkeys(out))


def fieldnames_for_model() -> list[str]:
    return [
        "mandarin_name",
        "blank_map",
        "locator_map",
        "pinyin_name",
        "english_name",
        "member_provinces",
        "connections",
        "Card_Member_Chips",
        "Card_Connections_HTML",
        "Card_BlankMap_HTML",
        "Card_LocatorMap_HTML",
    ]


def model_css() -> str:
    return """
:root{
  --paper:#f8f1e5;
  --paper-deep:#ecdcc4;
  --ink:#1e1a16;
  --muted:#66594b;
  --jade:#1f6a5a;
  --jade-soft:#d8ebe3;
  --vermillion:#b14a2f;
  --gold:#c8a866;
  --rule:rgba(42,31,20,0.14);
  --shadow:rgba(45,31,14,0.18);
}
.card{
  font-family:"Baskerville","Iowan Old Style","Palatino Linotype","Book Antiqua",serif;
  color:var(--ink);
  background:
    radial-gradient(circle at top left, rgba(200,168,102,0.18), transparent 32%),
    radial-gradient(circle at bottom right, rgba(31,106,90,0.12), transparent 28%),
    linear-gradient(180deg, #fbf6ef 0%, var(--paper) 55%, #f2e6d4 100%);
  font-size:20px;
  line-height:1.42;
  padding:22px 18px 28px;
}
.wrap{
  max-width:760px;
  margin:0 auto;
  position:relative;
}
.plate{
  background:linear-gradient(180deg, rgba(255,255,255,0.62), rgba(255,255,255,0.32));
  border:1px solid var(--rule);
  border-radius:26px;
  padding:22px 22px 24px;
  box-shadow:0 18px 42px var(--shadow);
  backdrop-filter:blur(2px);
}
.eyebrow{
  font-family:"Avenir Next","Gill Sans","Trebuchet MS",sans-serif;
  text-transform:uppercase;
  letter-spacing:0.16em;
  font-size:11px;
  color:var(--jade);
  margin:0 0 10px;
}
.title{
  font-size:52px;
  line-height:0.98;
  letter-spacing:-0.03em;
  margin:0;
}
.hanzi{
  font-size:70px;
  line-height:0.94;
  letter-spacing:-0.04em;
  margin:0;
}
.pinyin{
  font-family:"Avenir Next","Gill Sans","Trebuchet MS",sans-serif;
  color:var(--muted);
  font-size:20px;
  margin-top:8px;
}
.subtitle{
  color:var(--muted);
  font-size:17px;
  margin-top:8px;
}
.prompt{
  margin-top:18px;
  padding-top:16px;
  border-top:1px solid var(--rule);
  color:var(--muted);
  font-size:17px;
}
.answer-panel{
  margin-top:18px;
  border-radius:22px;
  border:1px solid rgba(31,106,90,0.18);
  background:linear-gradient(180deg, rgba(31,106,90,0.10), rgba(255,255,255,0.65));
  padding:18px 18px 16px;
}
.answer-label{
  font-family:"Avenir Next","Gill Sans","Trebuchet MS",sans-serif;
  text-transform:uppercase;
  letter-spacing:0.14em;
  font-size:11px;
  color:var(--vermillion);
  margin:0 0 8px;
}
.answer-main{
  font-size:34px;
  line-height:1.06;
  margin:0;
}
.answer-sub{
  font-family:"Avenir Next","Gill Sans","Trebuchet MS",sans-serif;
  color:var(--muted);
  font-size:18px;
  margin-top:8px;
}
.rule{
  height:1px;
  background:linear-gradient(90deg, transparent, var(--gold), transparent);
  margin:18px 0;
}
.meta-grid{
  display:grid;
  grid-template-columns:1fr;
  gap:16px;
  margin-top:18px;
}
@media (min-width:700px){
  .meta-grid{
    grid-template-columns:1fr 1fr;
  }
}
.panel{
  border:1px solid var(--rule);
  border-radius:18px;
  background:rgba(255,255,255,0.52);
  padding:16px 16px 14px;
}
.panel-title{
  font-family:"Avenir Next","Gill Sans","Trebuchet MS",sans-serif;
  font-size:12px;
  text-transform:uppercase;
  letter-spacing:0.12em;
  color:var(--jade);
  margin:0 0 10px;
}
.region-list,
.connection-list{
  margin:0;
  padding-left:18px;
}
.region-list li,
.connection-list li{
  margin:0 0 8px;
}
.member-chips{
  display:flex;
  flex-wrap:wrap;
  gap:10px;
}
.member-chip{
  display:inline-flex;
  align-items:center;
  border-radius:999px;
  border:1px solid rgba(31,106,90,0.18);
  background:linear-gradient(180deg, rgba(31,106,90,0.14), rgba(255,255,255,0.72));
  padding:8px 12px;
  font-family:"Avenir Next","Gill Sans","Trebuchet MS",sans-serif;
  font-size:14px;
  color:var(--ink);
}
.connections-layout{
  display:grid;
  grid-template-columns:1fr;
  gap:18px;
  margin-top:18px;
}
@media (min-width:760px){
  .connections-layout{
    grid-template-columns:0.95fr 1.15fr;
    align-items:start;
  }
}
.connection-rows{
  display:grid;
  gap:10px;
}
.connection-row{
  border-radius:16px;
  border:1px solid var(--rule);
  background:rgba(255,255,255,0.62);
  padding:12px 13px;
}
.connection-region{
  font-family:"Avenir Next","Gill Sans","Trebuchet MS",sans-serif;
  font-size:11px;
  text-transform:uppercase;
  letter-spacing:0.12em;
  color:var(--vermillion);
  margin-bottom:6px;
}
.connection-neighbors{
  font-size:16px;
  line-height:1.45;
}
.map-stack{
  display:grid;
  grid-template-columns:1fr;
  gap:18px;
  margin-top:18px;
}
@media (min-width:760px){
  .map-stack{
    grid-template-columns:1.05fr 1fr;
  }
}
.map-frame{
  position:relative;
  border-radius:24px;
  border:1px solid var(--rule);
  background:
    linear-gradient(180deg, rgba(255,255,255,0.92), rgba(248,241,229,0.9)),
    linear-gradient(135deg, rgba(200,168,102,0.12), rgba(31,106,90,0.06));
  padding:16px;
  box-shadow:0 18px 42px rgba(27,21,12,0.14);
}
.map-caption{
  font-family:"Avenir Next","Gill Sans","Trebuchet MS",sans-serif;
  text-transform:uppercase;
  letter-spacing:0.12em;
  font-size:11px;
  color:var(--muted);
  margin:0 0 10px;
}
.blank-map,
.locator-map{
  display:block;
  width:100%;
  height:auto;
}
.member-map-layout{
  display:grid;
  grid-template-columns:1fr;
  gap:18px;
  margin-top:18px;
}
@media (min-width:760px){
  .member-map-layout{
    grid-template-columns:1.05fr 0.95fr;
    align-items:start;
  }
}
.footer{
  margin-top:18px;
  font-family:"Avenir Next","Gill Sans","Trebuchet MS",sans-serif;
  font-size:13px;
  color:var(--muted);
}
""".strip()


def wrap_front(inner: str) -> str:
    return f'<div class="wrap"><div class="plate">{inner}</div></div>'


def answer_header() -> str:
    return """
<div class="footer">{{english_name}} | {{mandarin_name}} | {{pinyin_name}}</div>
""".strip()


def make_model() -> genanki.Model:
    templates = [
        {
            "name": "Hanzi -> Pinyin",
            "qfmt": wrap_front(
                """
<div class="eyebrow">Chinese to Pinyin</div>
<div class="hanzi">{{mandarin_name}}</div>
<div class="prompt">Read the region name in Mandarin pinyin.</div>
"""
            ),
            "afmt": wrap_front(
                """
<div class="eyebrow">Chinese to Pinyin</div>
<div class="hanzi">{{mandarin_name}}</div>
<div class="answer-panel">
  <div class="answer-label">Pinyin</div>
  <div class="answer-main">{{pinyin_name}}</div>
</div>
"""
                + answer_header()
            ),
        },
        {
            "name": "Hanzi -> English",
            "qfmt": wrap_front(
                """
<div class="eyebrow">Chinese to English</div>
<div class="hanzi">{{mandarin_name}}</div>
<div class="prompt">What is the English name of this region?</div>
"""
            ),
            "afmt": wrap_front(
                """
<div class="eyebrow">Chinese to English</div>
<div class="hanzi">{{mandarin_name}}</div>
<div class="answer-panel">
  <div class="answer-label">English</div>
  <div class="answer-main">{{english_name}}</div>
  <div class="answer-sub">{{pinyin_name}}</div>
</div>
"""
                + answer_header()
            ),
        },
        {
            "name": "English -> Chinese",
            "qfmt": wrap_front(
                """
<div class="eyebrow">English to Chinese</div>
<div class="title">{{english_name}}</div>
<div class="prompt">Recall the Chinese name in Hanzi and pinyin.</div>
"""
            ),
            "afmt": wrap_front(
                """
<div class="eyebrow">English to Chinese</div>
<div class="title">{{english_name}}</div>
<div class="answer-panel">
  <div class="answer-label">Chinese</div>
  <div class="answer-main">{{mandarin_name}}</div>
  <div class="answer-sub">{{pinyin_name}}</div>
</div>
"""
                + answer_header()
            ),
        },
        {
            "name": "Region -> Member Provinces",
            "qfmt": wrap_front(
                """
<div class="eyebrow">Region to Members</div>
<div class="title">{{english_name}}</div>
<div class="subtitle">{{mandarin_name}} | {{pinyin_name}}</div>
<div class="prompt">Which provincial-level divisions belong to this region?</div>
"""
            ),
            "afmt": wrap_front(
                """
<div class="eyebrow">Region to Members</div>
<div class="title">{{english_name}}</div>
<div class="subtitle">{{mandarin_name}} | {{pinyin_name}}</div>
<div class="connections-layout">
  <div class="map-frame">
    <div class="map-caption">Locator Map</div>
    {{Card_LocatorMap_HTML}}
  </div>
  <div class="answer-panel">
    <div class="answer-label">Members</div>
    {{Card_Member_Chips}}
  </div>
</div>
"""
                + answer_header()
            ),
        },
        {
            "name": "Members + Blank -> Locator Map",
            "qfmt": (
                "{{#Card_BlankMap_HTML}}{{#Card_LocatorMap_HTML}}"
                + wrap_front(
                    """
<div class="eyebrow">Members to Map</div>
<div class="title">{{english_name}}</div>
<div class="subtitle">{{mandarin_name}} | {{pinyin_name}}</div>
<div class="member-map-layout">
  <div class="answer-panel">
    <div class="answer-label">Members</div>
    {{Card_Member_Chips}}
  </div>
  <div class="map-frame">
    <div class="map-caption">Blank Map</div>
    {{Card_BlankMap_HTML}}
  </div>
</div>
<div class="prompt">Use the member set to place the region on the blank map, then reveal the locator.</div>
"""
                )
                + "{{/Card_LocatorMap_HTML}}{{/Card_BlankMap_HTML}}"
            ),
            "afmt": (
                "{{#Card_BlankMap_HTML}}{{#Card_LocatorMap_HTML}}"
                + wrap_front(
                    """
<div class="eyebrow">Members to Map</div>
<div class="title">{{english_name}}</div>
<div class="subtitle">{{mandarin_name}} | {{pinyin_name}}</div>
<div class="map-stack">
  <div class="map-frame">
    <div class="map-caption">Blank Map</div>
    {{Card_BlankMap_HTML}}
  </div>
  <div class="map-frame">
    <div class="map-caption">Locator Map</div>
    {{Card_LocatorMap_HTML}}
  </div>
</div>
<div class="answer-panel">
  <div class="answer-label">Members</div>
  {{Card_Member_Chips}}
</div>
"""
                    + answer_header()
                )
                + "{{/Card_LocatorMap_HTML}}{{/Card_BlankMap_HTML}}"
            ),
        },
        {
            "name": "Region -> Connections",
            "qfmt": wrap_front(
                """
<div class="eyebrow">Region to Connections</div>
<div class="title">{{english_name}}</div>
<div class="subtitle">{{mandarin_name}} | {{pinyin_name}}</div>
<div class="prompt">Recall the bordering provinces, seas, and neighboring countries.</div>
"""
            ),
            "afmt": wrap_front(
                """
<div class="eyebrow">Region to Connections</div>
<div class="title">{{english_name}}</div>
<div class="subtitle">{{mandarin_name}} | {{pinyin_name}}</div>
<div class="connections-layout">
  <div class="map-frame">
    <div class="map-caption">Locator Map</div>
    {{Card_LocatorMap_HTML}}
  </div>
  <div class="panel">
    <div class="panel-title">Connections</div>
    {{Card_Connections_HTML}}
  </div>
</div>
"""
                + answer_header()
            ),
        },
        {
            "name": "Region + Blank -> Locator Map",
            "qfmt": (
                "{{#Card_BlankMap_HTML}}{{#Card_LocatorMap_HTML}}"
                + wrap_front(
                    """
<div class="eyebrow">Atlas Recall</div>
<div class="title">{{english_name}}</div>
<div class="subtitle">{{mandarin_name}} | {{pinyin_name}}</div>
<div class="prompt">Picture the region on a blank map of China, then reveal the locator map.</div>
<div class="map-stack">
  <div class="map-frame">
    <div class="map-caption">Blank Map</div>
    {{Card_BlankMap_HTML}}
  </div>
</div>
"""
                )
                + "{{/Card_LocatorMap_HTML}}{{/Card_BlankMap_HTML}}"
            ),
            "afmt": (
                "{{#Card_BlankMap_HTML}}{{#Card_LocatorMap_HTML}}"
                + wrap_front(
                    """
<div class="eyebrow">Atlas Recall</div>
<div class="title">{{english_name}}</div>
<div class="subtitle">{{mandarin_name}} | {{pinyin_name}}</div>
<div class="map-stack">
  <div class="map-frame">
    <div class="map-caption">Blank Map</div>
    {{Card_BlankMap_HTML}}
  </div>
  <div class="map-frame">
    <div class="map-caption">Locator Map</div>
    {{Card_LocatorMap_HTML}}
  </div>
</div>
"""
                    + answer_header()
                )
                + "{{/Card_LocatorMap_HTML}}{{/Card_BlankMap_HTML}}"
            ),
        },
        {
            "name": "Locator Map -> Region Name",
            "qfmt": (
                "{{#Card_LocatorMap_HTML}}"
                + wrap_front(
                    """
<div class="eyebrow">Map to Name</div>
<div class="map-frame">
  <div class="map-caption">Locator Map</div>
  {{Card_LocatorMap_HTML}}
</div>
<div class="prompt">Name the highlighted region in English, Hanzi, and pinyin.</div>
"""
                )
                + "{{/Card_LocatorMap_HTML}}"
            ),
            "afmt": (
                "{{#Card_LocatorMap_HTML}}"
                + wrap_front(
                    """
<div class="eyebrow">Map to Name</div>
<div class="map-frame">
  <div class="map-caption">Locator Map</div>
  {{Card_LocatorMap_HTML}}
</div>
<div class="answer-panel">
  <div class="answer-label">Region</div>
  <div class="answer-main">{{english_name}}</div>
  <div class="answer-sub">{{mandarin_name}} | {{pinyin_name}}</div>
</div>
"""
                    + answer_header()
                )
                + "{{/Card_LocatorMap_HTML}}"
            ),
        },
    ]

    return genanki.Model(
        model_id=MODEL_ID,
        name=f"China Regions v{MODEL_SCHEMA_VERSION}",
        fields=[{"name": field} for field in fieldnames_for_model()],
        templates=templates,
        css=model_css(),
    )


def note_fields(row: dict[str, str]) -> list[str]:
    member_provinces = row.get("member_provinces", "")
    connections = row.get("connections", "")
    members = split_csv_like_values(member_provinces)
    member_chips = html_member_chips(members)
    connection_html = html_connection_rows(split_connection_lines(connections))

    blank_map_path = MEDIA_DIR / BLANK_MAP_FILENAME
    blank_map_html = ""
    if blank_map_path.exists():
        blank_map_html = make_map_html(BLANK_MAP_FILENAME, "Blank map of China", "blank-map")

    locator_map_html = ""
    locator_url = (row.get("locator_map") or "").strip()
    locator_filename = LOCATOR_URL_TO_FILENAME.get(locator_url)
    if locator_filename and (MEDIA_DIR / locator_filename).exists():
        locator_map_html = make_map_html(
            locator_filename,
            f"Locator map for {row.get('english_name', '').strip()}",
            "locator-map",
        )

    return [
        row.get("mandarin_name", ""),
        row.get("blank_map", ""),
        row.get("locator_map", ""),
        row.get("pinyin_name", ""),
        row.get("english_name", ""),
        member_provinces,
        connections,
        member_chips,
        connection_html,
        blank_map_html,
        locator_map_html,
    ]


def build_deck() -> None:
    rows = read_rows(NOTES_CSV)
    model = make_model()
    deck = genanki.Deck(DECK_ID, "China Regions")
    for row in rows:
        note = genanki.Note(model=model, fields=note_fields(row))
        deck.add_note(note)

    package = genanki.Package(deck)
    package.media_files = collect_media(rows)
    OUTPUT_APKG.parent.mkdir(parents=True, exist_ok=True)
    package.write_to_file(str(OUTPUT_APKG))
    print(f"wrote {OUTPUT_APKG}")


if __name__ == "__main__":
    build_deck()
