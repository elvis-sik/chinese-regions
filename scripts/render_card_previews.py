#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

from build_apkg import (
    MEDIA_DIR,
    REPO_ROOT,
    fieldnames_for_model,
    make_model,
    note_fields,
    read_rows,
)


OUTPUT_DIR = REPO_ROOT / "out" / "card_previews"
SECTION_RE = re.compile(r"{{#([A-Za-z0-9_]+)}}(.*?){{/\1}}", re.DOTALL)
FIELD_RE = re.compile(r"{{([A-Za-z0-9_]+)}}")
MODEL = make_model()


PREVIEW_PAGES = [
    {
        "filename": "map-to-name-pair.html",
        "cards": [
            {
                "note": "North China",
                "template": "Locator Map -> Region Name",
                "side": "front",
            },
            {
                "note": "North China",
                "template": "Locator Map -> Region Name",
                "side": "back",
            }
        ],
    },
]


def preview_css() -> str:
    return """
body{
  margin:0;
  padding:36px;
  background:
    radial-gradient(circle at top left, rgba(213,177,95,0.22), transparent 24%),
    radial-gradient(circle at 78% 12%, rgba(141,20,36,0.14), transparent 22%),
    linear-gradient(180deg, #f2e3c9 0%, #e8d5b7 100%);
}
.showcase{
  max-width:1480px;
  margin:0 auto;
  display:grid;
  grid-template-columns:repeat(2, minmax(0, 1fr));
  gap:28px;
}
.slot{
  min-width:0;
}
.preview-frame{
  border-radius:34px;
  overflow:hidden;
  box-shadow:
    0 30px 70px rgba(63,30,14,0.22),
    0 8px 24px rgba(63,30,14,0.12);
}
.preview-frame .card{
  margin:0;
}
@media (max-width:1120px){
  body{
    padding:24px;
  }
  .showcase{
    grid-template-columns:1fr;
  }
}
""".strip()


def render_template(template: str, fields: dict[str, str]) -> str:
    rendered = template
    while True:
        updated = SECTION_RE.sub(
            lambda match: render_template(match.group(2), fields) if fields.get(match.group(1), "") else "",
            rendered,
        )
        if updated == rendered:
            break
        rendered = updated
    rendered = FIELD_RE.sub(lambda match: fields.get(match.group(1), ""), rendered)
    return re.sub(r"{{[^}]+}}", "", rendered)


def absolutize_media_html(value: str) -> str:
    return re.sub(
        r'src="([^"]+)"',
        lambda match: f'src="{(MEDIA_DIR / match.group(1)).resolve().as_uri()}"',
        value,
    )


def note_lookup() -> dict[str, dict[str, str]]:
    rows = read_rows(REPO_ROOT / "data/raw/china_regions_notes_seed.csv")
    names = fieldnames_for_model()
    by_name: dict[str, dict[str, str]] = {}
    for row in rows:
        fields = dict(zip(names, note_fields(row), strict=True))
        fields["Card_BlankMap_HTML"] = absolutize_media_html(fields["Card_BlankMap_HTML"])
        fields["Card_LocatorMap_HTML"] = absolutize_media_html(fields["Card_LocatorMap_HTML"])
        english_name = fields["english_name"]
        by_name[english_name] = fields
    return by_name


def template_lookup() -> dict[str, dict[str, str]]:
    return {template["name"]: template for template in MODEL.templates}


def page_html(
    cards: list[dict[str, str]],
    templates: dict[str, dict[str, str]],
    notes: dict[str, dict[str, str]],
) -> str:
    rendered_cards: list[str] = []
    for card in cards:
        template = templates[card["template"]]
        note = notes[card["note"]]
        rendered = render_template(template["qfmt" if card["side"] == "front" else "afmt"], note)
        rendered_cards.append(
            f'<div class="slot"><div class="preview-frame"><div class="card">{rendered}</div></div></div>'
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>China Regions card previews</title>
  <style>
  {MODEL.css}
  {preview_css()}
  </style>
</head>
<body>
  <main class="showcase">
    {''.join(rendered_cards)}
  </main>
</body>
</html>
"""


def render_pages() -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    notes = note_lookup()
    templates = template_lookup()
    written: list[Path] = []
    for page in PREVIEW_PAGES:
        path = OUTPUT_DIR / page["filename"]
        path.write_text(page_html(page["cards"], templates, notes), encoding="utf-8")
        written.append(path)
    return written


def main() -> None:
    for path in render_pages():
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
