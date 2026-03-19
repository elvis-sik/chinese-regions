#!/usr/bin/env python3
from __future__ import annotations

import csv
import time
from pathlib import Path

import requests


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = REPO_ROOT / "data/raw/region_image_sources.csv"
MEDIA_DIR = REPO_ROOT / "media/regions"

TITLE_TO_FILENAME = {
    "China_blank_map.svg": "china_blank_map.svg",
    "North_China.svg": "north_china_locator.svg",
    "East_China.svg": "east_china_locator.svg",
    "South_Central_China.svg": "south_central_china_locator.svg",
    "Southwest_China.svg": "southwest_china_locator.svg",
    "Northeast_China.svg": "northeast_china_locator.svg",
    "Northwest_China.svg": "northwest_china_locator.svg",
    "Regions_of_China.svg": "regions_of_china_overview.svg",
}

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def redirect_url_for_title(title: str) -> str:
    return f"https://commons.wikimedia.org/wiki/Special:Redirect/file/{title}"


def download(url: str, dest: Path) -> None:
    last_error: Exception | None = None
    for attempt in range(4):
        response = requests.get(
            url,
            timeout=120,
            allow_redirects=True,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "image/svg+xml,image/*;q=0.9,*/*;q=0.8",
            },
        )
        if response.status_code == 429:
            wait_seconds = max(2, 2 * (attempt + 1))
            retry_after = response.headers.get("Retry-After")
            if retry_after and retry_after.isdigit():
                wait_seconds = max(wait_seconds, int(retry_after))
            time.sleep(wait_seconds)
            last_error = requests.HTTPError(
                f"429 Too Many Requests after attempt {attempt + 1}",
                response=response,
            )
            continue
        response.raise_for_status()
        dest.write_bytes(response.content)
        return

    if last_error is not None:
        raise last_error
    raise RuntimeError(f"Failed to download {url}")


def main() -> int:
    rows = read_rows(SOURCE_CSV)
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    downloaded = 0
    skipped = 0

    for row in rows:
        title = (row.get("commons_title") or "").strip()
        if not title:
            continue
        if title not in TITLE_TO_FILENAME:
            continue

        dest = MEDIA_DIR / TITLE_TO_FILENAME[title]
        if dest.exists() and dest.stat().st_size > 0:
            skipped += 1
            print(f"skip  {dest.name}")
            continue

        print(f"fetch {dest.name}")
        download(redirect_url_for_title(title), dest)
        downloaded += 1
        time.sleep(1.0)

    print(f"done: downloaded={downloaded} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
