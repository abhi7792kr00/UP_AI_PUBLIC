from __future__ import annotations

import csv
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup


PAGES_FILE = Path(
    "data/source/up/block_tehsil_pages.csv"
)

OUTPUT_FILE = Path(
    "data/source/up/block_tehsil_raw.csv"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

TIMEOUT = 30


def extract_block_tehsil_rows(html: str):
    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    results = []

    block_headers = {
        "block",
        "block name",
        "development block",
        "development blocks",
        "vikas khand",
    }

    tehsil_headers = {
        "tehsil",
        "tehsil name",
        "subdivision",
        "sub-division",
    }

    for table in soup.find_all("table"):
        rows = table.find_all("tr")

        if not rows:
            continue

        header = [
            " ".join(
                cell.get_text(
                    " ",
                    strip=True,
                ).lower().split()
            )
            for cell in rows[0].find_all(
                ["th", "td"]
            )
        ]

        block_index = None
        tehsil_index = None

        for index, name in enumerate(header):
            if name in block_headers:
                block_index = index

            if name in tehsil_headers:
                tehsil_index = index

        if (
            block_index is None
            or tehsil_index is None
        ):
            continue

        table_results = []

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

            block_name = cells[
                block_index
            ].strip()

            tehsil_name = cells[
                tehsil_index
            ].strip()

            if not block_name or not tehsil_name:
                continue

            table_results.append(
                (
                    block_name,
                    tehsil_name,
                )
            )

        if table_results:
            return table_results

    return []

def main():
    if not PAGES_FILE.exists():
        raise FileNotFoundError(
            f"Missing: {PAGES_FILE}"
        )

    rows = []

    with PAGES_FILE.open(
        newline="",
        encoding="utf-8",
    ) as file:
        pages = list(
            csv.DictReader(file)
        )

    verified = [
        row
        for row in pages
        if row["block_tehsil_url"].strip()
    ]

    print(
        "VERIFIED PAGES:",
        len(verified),
    )

    for item in verified:
        district_code = item[
            "district_code"
        ].strip()

        district_name = item[
            "district_name"
        ].strip()

        url = item[
            "block_tehsil_url"
        ].strip()

        print(
            f"\n[{district_code}] "
            f"{district_name}"
        )

        print(
            "  URL:",
            url,
        )

        try:
            response = requests.get(
                url,
                timeout=TIMEOUT,
                headers=HEADERS,
            )

            response.raise_for_status()

            pairs = (
                extract_block_tehsil_rows(
                    response.text
                )
            )

            print(
                "  Rows found:",
                len(pairs),
            )

            for (
                block_name,
                tehsil_name,
            ) in pairs:
                rows.append(
                    {
                        "district_code":
                            district_code,
                        "district_name":
                            district_name,
                        "block_name":
                            block_name,
                        "tehsil_name":
                            tehsil_name,
                        "source_url":
                            url,
                    }
                )

        except Exception as exc:
            print(
                "  ERROR:",
                repr(exc),
            )

        time.sleep(0.5)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "district_code",
                "district_name",
                "block_name",
                "tehsil_name",
                "source_url",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    print()
    print(
        "TOTAL MAPPINGS:",
        len(rows),
    )
    print(
        "OUTPUT:",
        OUTPUT_FILE,
    )


if __name__ == "__main__":
    main()
