from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


INPUT = Path(
    "data/source/up/block_tehsil_pages.csv"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

TIMEOUT = (5, 20)

PATHS = [
    "/development-block/",
    "/development-blocks/",
    "/block/",
    "/blocks/",
    "/block-list/",
    "/block-name/",
    "/block-wise/",
    "/block-level/",
    "/block-details/",
    "/subdivision-block/",
    "/subdivision-blocks/",
    "/administrative-setup/block/",
    "/administrative-setup/development/",
]


def norm(value: str) -> str:
    return " ".join(
        value.lower().strip().split()
    )


BLOCK_HEADERS = {
    "block",
    "block name",
    "development block",
    "development blocks",
    "block name (in english)",
    "vikas khand",
}

TEHSIL_HEADERS = {
    "tehsil",
    "tehsil name",
    "subdivision",
    "sub-division",
}


def extract_rows(html: str):
    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    for table in soup.find_all("table"):
        rows = table.find_all("tr")

        if not rows:
            continue

        header = [
            norm(
                cell.get_text(
                    " ",
                    strip=True,
                )
            )
            for cell in rows[0].find_all(
                ["th", "td"]
            )
        ]

        block_index = None
        tehsil_index = None

        for i, h in enumerate(header):
            if h in BLOCK_HEADERS:
                block_index = i

            if h in TEHSIL_HEADERS:
                tehsil_index = i

        if (
            block_index is None
            or tehsil_index is None
        ):
            continue

        data = []

        for row in rows[1:]:
            cells = [
                cell.get_text(
                    " ",
                    strip=True,
                )
                for cell in row.find_all(
                    ["th", "td"]
                )
            ]

            if len(cells) <= max(
                block_index,
                tehsil_index,
            ):
                continue

            block = cells[block_index].strip()
            tehsil = cells[tehsil_index].strip()

            if not block or not tehsil:
                continue

            data.append((block, tehsil))

        if data:
            return data

    return []


def main():
    with INPUT.open(
        newline="",
        encoding="utf-8",
    ) as f:
        districts = list(csv.DictReader(f))

    session = requests.Session()
    session.headers.update(HEADERS)

    for row in districts:
        if row["block_tehsil_url"].strip():
            continue

        district_code = row["district_code"]
        district_name = row["district_name"]
        base = row["homepage_url"].rstrip("/")

        print("\n" + "=" * 90)
        print(
            district_code,
            "|",
            district_name,
        )

        candidates = [
            urljoin(base + "/", path.lstrip("/"))
            for path in PATHS
        ]

        verified = []

        for url in candidates:
            try:
                r = session.get(
                    url,
                    timeout=TIMEOUT,
                    allow_redirects=True,
                )

                if r.status_code != 200:
                    continue

                pairs = extract_rows(r.text)

                if pairs:
                    verified.append(
                        (
                            r.url,
                            len(pairs),
                        )
                    )

            except Exception:
                continue

        if verified:
            for url, count in verified:
                print(
                    "VERIFIED:",
                    url,
                    "| ROWS:",
                    count,
                )
        else:
            print(
                "NO STRUCTURED BLOCK/TEHSIL TABLE"
            )


if __name__ == "__main__":
    main()
