from __future__ import annotations

import csv
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


INPUT_FILE = Path(
    "data/source/up/district_portals.csv"
)

OUTPUT_FILE = Path(
    "data/source/up/block_tehsil_pages.csv"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept":
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,*/*;q=0.8",
}

TIMEOUT = (5, 20)

URL_PATTERNS = [
    "/subdivision-blocks/",
    "/subdivision-block/",
    "/development-block/",
    "/development-blocks/",
    "/blocks/",
    "/block/",
    "/block-wise/",
    "/blockwise/",
    "/subdivision/",
    "/vikas-khand/",
    "/vikas-khand-wise/",
    "/vikas-khand-list/",
    "/blocks-list/",
]

LINK_KEYWORDS = (
    "block",
    "blocks",
    "development block",
    "development blocks",
    "subdivision",
    "sub-division",
    "vikas khand",
)

BLOCK_HEADERS = {
    "block",
    "block name",
    "development block",
    "development blocks",
    "vikas khand",
}

TEHSIL_HEADERS = {
    "tehsil",
    "tehsil name",
    "subdivision",
    "sub-division",
}


def norm(value: str) -> str:
    value = value.lower().strip()
    return re.sub(r"\s+", " ", value)


def same_domain(base_url: str, candidate_url: str) -> bool:
    base = urlparse(base_url).netloc.lower()
    candidate = urlparse(candidate_url).netloc.lower()

    return (
        candidate == ""
        or candidate == base
    )


def fetch(
    session: requests.Session,
    url: str,
):
    try:
        response = session.get(
            url,
            timeout=TIMEOUT,
            headers=HEADERS,
        )

        response.raise_for_status()

        return response

    except Exception as exc:
        print(
            "      FETCH ERROR:",
            repr(exc),
        )
        return None


def parse_block_tehsil_table(
    html: str,
):
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

        for index, name in enumerate(header):
            if name in BLOCK_HEADERS:
                block_index = index

            if name in TEHSIL_HEADERS:
                tehsil_index = index

        if (
            block_index is None
            or tehsil_index is None
        ):
            continue

        results = []

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

            if (
                not block_name
                or not tehsil_name
            ):
                continue

            results.append(
                (
                    block_name,
                    tehsil_name,
                )
            )

        if results:
            return results

    return []


def homepage_candidates(
    session: requests.Session,
    homepage: str,
):
    candidates = set()

    # -------------------------------------
    # Homepage itself
    # -------------------------------------

    response = fetch(
        session,
        homepage,
    )

    if response is None:
        return candidates, None

    # -------------------------------------
    # Parse links
    # -------------------------------------

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

        href = anchor[
            "href"
        ].strip()

        if not href:
            continue

        absolute = urljoin(
            response.url,
            href,
        )

        if not same_domain(
            response.url,
            absolute,
        ):
            continue

        combined = norm(
            f"{text} {href}"
        )

        if any(
            keyword in combined
            for keyword in LINK_KEYWORDS
        ):
            candidates.add(
                absolute
            )

    # -------------------------------------
    # robots.txt
    # -------------------------------------

    robots = urljoin(
        response.url,
        "/robots.txt",
    )

    robots_response = fetch(
        session,
        robots,
    )

    if robots_response is not None:
        for line in robots_response.text.splitlines():
            if line.lower().startswith(
                "sitemap:"
            ):
                sitemap_url = line.split(
                    ":",
                    1,
                )[1].strip()

                candidates.add(
                    sitemap_url
                )

    # -------------------------------------
    # sitemap common paths
    # -------------------------------------

    for path in (
        "/sitemap.xml",
        "/wp-sitemap.xml",
    ):
        candidates.add(
            urljoin(
                response.url,
                path,
            )
        )

    return candidates, response


def sitemap_links(
    session: requests.Session,
    url: str,
):
    response = fetch(
        session,
        url,
    )

    if response is None:
        return set()

    content_type = (
        response.headers.get(
            "Content-Type",
            "",
        ).lower()
    )

    if (
        "xml" not in content_type
        and not response.text.lstrip().startswith(
            "<?xml"
        )
    ):
        return set()

    links = set()

    try:
        soup = BeautifulSoup(
            response.text,
            "xml",
        )

        for loc in soup.find_all("loc"):
            value = loc.get_text(
                strip=True
            )

            if value:
                links.add(value)

    except Exception:
        pass

    return links


def verify_url(
    session: requests.Session,
    url: str,
):
    response = fetch(
        session,
        url,
    )

    if response is None:
        return None

    pairs = parse_block_tehsil_table(
        response.text
    )

    if not pairs:
        return None

    return {
        "url": response.url,
        "rows": len(pairs),
    }


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Missing: {INPUT_FILE}"
        )

    with INPUT_FILE.open(
        newline="",
        encoding="utf-8",
    ) as f:
        districts = list(
            csv.DictReader(f)
        )

    session = requests.Session()

    results = []

    for row in districts:
        district_code = row[
            "district_code"
        ].strip()

        district_name = row[
            "district_name"
        ].strip()

        homepage = row[
            "portal_url"
        ].strip()

        print()
        print("=" * 90)
        print(
            district_code,
            district_name,
        )

        if not homepage:
            print(
                "  MISSING HOMEPAGE"
            )

            results.append(
                {
                    "district_code":
                        district_code,
                    "district_name":
                        district_name,
                    "homepage_url":
                        homepage,
                    "block_tehsil_url":
                        "",
                    "link_text":
                        "",
                    "status":
                        "missing_homepage",
                }
            )

            continue

        discovered, homepage_response = (
            homepage_candidates(
                session,
                homepage,
            )
        )

        # -------------------------------------
        # Add known URL patterns
        # -------------------------------------

        base = homepage.rstrip("/")

        for pattern in URL_PATTERNS:
            discovered.add(
                base + pattern
            )

        # -------------------------------------
        # Probe sitemap URLs
        # -------------------------------------

        sitemap_candidates = set()

        for candidate in list(discovered):
            if (
                candidate.endswith(
                    "sitemap.xml"
                )
                or candidate.endswith(
                    "wp-sitemap.xml"
                )
            ):
                sitemap_candidates.update(
                    sitemap_links(
                        session,
                        candidate,
                    )
                )

        # Keep only links that look relevant.
        for link in sitemap_candidates:
            if any(
                keyword in norm(link)
                for keyword in LINK_KEYWORDS
            ):
                discovered.add(link)

        print(
            "  Candidates:",
            len(discovered),
        )

        # -------------------------------------
        # Verify candidates
        # -------------------------------------

        verified = None

        for candidate in sorted(
            discovered
        ):
            verification = verify_url(
                session,
                candidate,
            )

            if verification is None:
                continue

            verified = {
                "district_code":
                    district_code,
                "district_name":
                    district_name,
                "homepage_url":
                    homepage,
                "block_tehsil_url":
                    verification[
                        "url"
                    ],
                "link_text":
                    "",
                "status":
                    (
                        "verified_rows="
                        + str(
                            verification[
                                "rows"
                            ]
                        )
                    ),
            }

            print(
                "  VERIFIED:",
                verification["url"],
                "| rows:",
                verification["rows"],
            )

            break

        if verified is None:
            print(
                "  NO VERIFIED BLOCK/TEHSIL PAGE"
            )

            verified = {
                "district_code":
                    district_code,
                "district_name":
                    district_name,
                "homepage_url":
                    homepage,
                "block_tehsil_url":
                    "",
                "link_text":
                    "",
                "status":
                    "not_found",
            }

        results.append(
            verified
        )

        time.sleep(0.3)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "district_code",
                "district_name",
                "homepage_url",
                "block_tehsil_url",
                "link_text",
                "status",
            ],
        )

        writer.writeheader()
        writer.writerows(results)

    verified_count = sum(
        bool(
            row["block_tehsil_url"]
        )
        for row in results
    )

    print()
    print(
        "======================================"
    )
    print(
        "DISTRICTS PROCESSED:",
        len(results),
    )
    print(
        "VERIFIED PAGES:",
        verified_count,
    )
    print(
        "OUTPUT:",
        OUTPUT_FILE,
    )


if __name__ == "__main__":
    main()
