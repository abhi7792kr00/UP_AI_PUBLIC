from __future__ import annotations

import csv
import re
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


DISTRICTS = {
    "118",
    "119",
    "120",
    "125",
    "140",
    "184",
}

INPUT = Path(
    "data/source/up/district_portals.csv"
)

PATTERNS = [
    "/subdivision-blocks/",
    "/subdivision-block/",
    "/development-block/",
    "/development-blocks/",
    "/blocks/",
    "/subdivision/",
    "/block/",
    "/block-wise/",
    "/blockwise/",
    "/vikas-khand/",
    "/vikas-khand-wise/",
]

KEYWORDS = (
    "block",
    "blocks",
    "development block",
    "subdivision",
    "sub-division",
    "vikas khand",
)


def norm(value: str) -> str:
    return " ".join(
        value.lower().split()
    )


def looks_like_block_page(
    html: str,
) -> bool:
    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    text = norm(
        soup.get_text(
            " ",
            strip=True,
        )
    )

    # Strong page-level hint.
    if (
        "block" not in text
        and "blocks" not in text
        and "vikas khand" not in text
    ):
        return False

    for table in soup.find_all("table"):
        rows = table.find_all("tr")

        if not rows:
            continue

        header = [
            norm(
                c.get_text(
                    " ",
                    strip=True,
                )
            )
            for c in rows[0].find_all(
                ["th", "td"]
            )
        ]

        has_block = any(
            "block" in h
            or "vikas khand" in h
            for h in header
        )

        has_tehsil = any(
            "tehsil" in h
            or "subdivision" in h
            for h in header
        )

        if has_block and has_tehsil:
            return True

    return False


def main():
    with INPUT.open(
        newline="",
        encoding="utf-8",
    ) as f:
        districts = list(
            csv.DictReader(f)
        )

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0",
            "Accept":
                "text/html,application/xhtml+xml",
        }
    )

    for row in districts:
        if row["district_code"] not in DISTRICTS:
            continue

        district = row["district_name"]
        base = row["portal_url"].rstrip("/")

        print("\n" + "=" * 90)
        print(
            row["district_code"],
            district,
        )

        candidates = set()

        # ----------------------------------------
        # 1. Known URL patterns
        # ----------------------------------------

        for pattern in PATTERNS:
            candidates.add(
                base + pattern
            )

        # ----------------------------------------
        # 2. Homepage links
        # ----------------------------------------

        try:
            response = session.get(
                base,
                timeout=(5, 15),
            )

            if response.ok:
                soup = BeautifulSoup(
                    response.text,
                    "html.parser",
                )

                for anchor in soup.find_all(
                    "a",
                    href=True,
                ):
                    text = norm(
                        anchor.get_text(
                            " ",
                            strip=True,
                        )
                    )

                    href = anchor["href"].strip()

                    combined = norm(
                        f"{text} {href}"
                    )

                    if any(
                        keyword in combined
                        for keyword in KEYWORDS
                    ):
                        candidates.add(
                            urljoin(
                                response.url,
                                href,
                            )
                        )

        except Exception as exc:
            print(
                "Homepage error:",
                repr(exc),
            )

        # ----------------------------------------
        # 3. Probe candidates
        # ----------------------------------------

        verified = []

        for url in sorted(candidates):
            try:
                r = session.get(
                    url,
                    timeout=(5, 15),
                )

                if not r.ok:
                    continue

                if looks_like_block_page(
                    r.text
                ):
                    verified.append(url)

            except Exception:
                continue

        print(
            "Candidates:",
            len(candidates),
        )

        if verified:
            print(
                "VERIFIED:"
            )
            for url in verified:
                print(
                    " ",
                    url,
                )
        else:
            print(
                "NO VERIFIED BLOCK/TEHSIL PAGE"
            )


if __name__ == "__main__":
    main()
