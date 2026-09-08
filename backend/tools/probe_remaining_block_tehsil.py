from __future__ import annotations

import csv
import re
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

TIMEOUT = (5, 15)

PATHS = [
    "/subdivision-blocks/",
    "/subdivision-block/",
    "/development-block/",
    "/development-blocks/",
    "/blocks/",
    "/block/",
    "/block-wise/",
    "/blockwise/",
    "/subdivision/",
    "/tehsil/",
    "/administrative-setup/",
]


def norm(s: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        s.lower().strip(),
    )


def candidate_links(
    base_url: str,
    html: str,
):
    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    found = set()

    for a in soup.find_all(
        "a",
        href=True,
    ):
        text = norm(
            a.get_text(
                " ",
                strip=True,
            )
        )

        href = a["href"].strip()

        combined = norm(
            text + " " + href
        )

        if any(
            x in combined
            for x in (
                "block",
                "tehsil",
                "subdivision",
                "vikas khand",
                "administrative",
            )
        ):
            found.add(
                urljoin(
                    base_url,
                    href,
                )
            )

    return found


def mentions_block_tehsil(
    html: str,
):
    text = norm(
        BeautifulSoup(
            html,
            "html.parser",
        ).get_text(
            " ",
            strip=True,
        )
    )

    return (
        "block" in text
        and "tehsil" in text
    )


def main():
    with INPUT.open(
        newline="",
        encoding="utf-8",
    ) as f:
        rows = list(
            csv.DictReader(f)
        )

    session = requests.Session()
    session.headers.update(
        HEADERS
    )

    targets = [
        r for r in rows
        if not r[
            "block_tehsil_url"
        ].strip()
    ]

    print(
        "TARGET DISTRICTS:",
        len(targets),
    )

    for row in targets:
        code = row[
            "district_code"
        ]

        name = row[
            "district_name"
        ]

        base = row[
            "homepage_url"
        ].rstrip("/")

        print("\n" + "=" * 80)
        print(
            code,
            "|",
            name,
        )

        candidates = {
            base + p
            for p in PATHS
        }

        try:
            r = session.get(
                base,
                timeout=TIMEOUT,
            )

            if r.ok:
                candidates.update(
                    candidate_links(
                        r.url,
                        r.text,
                    )
                )

        except Exception as exc:
            print(
                "HOME ERROR:",
                repr(exc),
            )

        print(
            "CANDIDATES:",
            len(candidates),
        )

        found = []

        for url in sorted(candidates):
            try:
                r = session.get(
                    url,
                    timeout=TIMEOUT,
                )

                if (
                    r.status_code != 200
                    or not r.text
                ):
                    continue

                if mentions_block_tehsil(
                    r.text
                ):
                    found.append(
                        url
                    )

            except Exception:
                continue

        if found:
            print(
                "CONTENT CANDIDATES:"
            )

            for url in found[:20]:
                print(
                    " ",
                    url,
                )
        else:
            print(
                "NO CONTENT CANDIDATE"
            )


if __name__ == "__main__":
    main()
