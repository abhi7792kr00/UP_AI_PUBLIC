from __future__ import annotations

import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


DISTRICTS_FILE = Path(
    "data/master/up/districts.csv"
)

OUTPUT_FILE = Path(
    "data/source/up/prd_gram_panchayat_block.csv"
)

URL = (
    "https://panchayatiraj.up.nic.in/"
    "pblc_pg/Reports/PB2FormReport"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml",
}


def normalize(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("&", "and")
    value = re.sub(
        r"[\(\)\-_,.&.]",
        " ",
        value,
    )
    value = re.sub(
        r"\s+",
        " ",
        value,
    )
    return value


def build_session() -> requests.Session:
    session = requests.Session()

    retry = Retry(
        total=4,
        connect=4,
        read=4,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )

    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=2,
        pool_maxsize=2,
    )

    session.mount(
        "https://",
        adapter,
    )

    session.headers.update(
        HEADERS
    )

    return session


def parse_table(
    html: str,
) -> list[dict[str, str]]:
    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    required = {
        "जनपद",
        "विकास खण्ड",
        "ग्राम पंचायत",
        "विकास खण्ड कोड",
        "ग्राम पंचायत कोड",
    }

    target = None

    for table in soup.find_all("table"):
        rows = table.find_all("tr")

        if not rows:
            continue

        header = [
            c.get_text(
                " ",
                strip=True,
            )
            for c in rows[0].find_all(
                ["th", "td"]
            )
        ]

        if required.issubset(set(header)):
            target = (
                table,
                header,
            )
            break

    if target is None:
        raise RuntimeError(
            "Target PRD table not found"
        )

    table, header = target

    index = {
        name: i
        for i, name in enumerate(header)
    }

    result = []

    for tr in table.find_all("tr")[1:]:
        cells = [
            c.get_text(
                " ",
                strip=True,
            )
            for c in tr.find_all(
                ["th", "td"]
            )
        ]

        if len(cells) < len(header):
            continue

        district = cells[
            index["जनपद"]
        ].strip()

        block = cells[
            index["विकास खण्ड"]
        ].strip()

        gp = cells[
            index["ग्राम पंचायत"]
        ].strip()

        block_code = cells[
            index["विकास खण्ड कोड"]
        ].strip()

        gp_code = cells[
            index["ग्राम पंचायत कोड"]
        ].strip()

        if not (
            district
            and block
            and gp
            and block_code
            and gp_code
        ):
            continue

        result.append(
            {
                "district_name": district,
                "block_name": block,
                "block_code": block_code,
                "gram_panchayat_name": gp,
                "gram_panchayat_code": gp_code,
            }
        )

    return result


def load_existing() -> dict[tuple[str, str, str], dict]:
    if not OUTPUT_FILE.exists():
        return {}

    with OUTPUT_FILE.open(
        newline="",
        encoding="utf-8",
    ) as file:
        rows = csv.DictReader(file)

        return {
            (
                row["district_name"],
                row["block_code"],
                row["gram_panchayat_code"],
            ): row
            for row in rows
        }


def save_rows(rows: dict):
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "district_name",
        "block_name",
        "block_code",
        "gram_panchayat_name",
        "gram_panchayat_code",
    ]

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for row in sorted(
            rows.values(),
            key=lambda r: (
                normalize(
                    r["district_name"]
                ),
                normalize(
                    r["block_name"]
                ),
                r["gram_panchayat_code"],
            ),
        ):
            writer.writerow(row)


def main():
    with DISTRICTS_FILE.open(
        newline="",
        encoding="utf-8-sig",
    ) as file:
        districts = list(
            csv.DictReader(file)
        )

    existing = load_existing()

    print(
        "Existing mappings:",
        len(existing),
    )

    session = build_session()

    success = 0
    failed = 0

    for number, district in enumerate(
        districts,
        start=1,
    ):
        name = district[
            "district_name"
        ]

        # Skip districts already collected.
        collected = any(
            normalize(
                row["district_name"]
            )
            == normalize(name)
            for row in existing.values()
        )

        if collected:
            print(
                f"[{number}/"
                f"{len(districts)}] "
                f"{name} -> SKIP"
            )
            continue

        print(
            f"[{number}/"
            f"{len(districts)}] "
            f"{name}"
        )

        try:
            response = session.get(
                URL,
                params={
                    "District":
                        name.upper(),
                    "ReportType":
                        "Filled",
                },
                timeout=(15, 60),
            )

            response.raise_for_status()

            rows = parse_table(
                response.text
            )

            for row in rows:
                key = (
                    row["district_name"],
                    row["block_code"],
                    row["gram_panchayat_code"],
                )

                existing[key] = row

            save_rows(existing)

            print(
                "  rows:",
                len(rows),
                "| total:",
                len(existing),
            )

            success += 1

        except Exception as exc:
            failed += 1

            print(
                "  ERROR:",
                repr(exc),
            )

        time.sleep(1.5)

    print()
    print(
        "SUCCESS DISTRICTS:",
        success,
    )
    print(
        "FAILED DISTRICTS:",
        failed,
    )
    print(
        "TOTAL MAPPINGS:",
        len(existing),
    )
    print(
        "OUTPUT:",
        OUTPUT_FILE,
    )


if __name__ == "__main__":
    main()
