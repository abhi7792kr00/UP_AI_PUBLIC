from __future__ import annotations

import csv
import re
from pathlib import Path

from bs4 import BeautifulSoup


SOURCE = Path(
    "data/source/up/prd"
)

OUTPUT = Path(
    "data/source/up/"
    "prd_gram_panchayat_block.csv"
)


def norm(value: str) -> str:
    value = value.lower().strip()
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


def parse_file(path: Path):
    soup = BeautifulSoup(
        path.read_text(
            encoding="utf-8",
            errors="replace",
        ),
        "html.parser",
    )

    required = {
        "जनपद",
        "विकास खण्ड",
        "ग्राम पंचायत",
        "विकास खण्ड कोड",
        "ग्राम पंचायत कोड",
    }

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

        if not required.issubset(
            set(header)
        ):
            continue

        index = {
            name: i
            for i, name in enumerate(header)
        }

        result = []

        for tr in rows[1:]:
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

            row = {
                "district_name": cells[
                    index["जनपद"]
                ].strip(),

                "block_name": cells[
                    index["विकास खण्ड"]
                ].strip(),

                "block_code": cells[
                    index["विकास खण्ड कोड"]
                ].strip(),

                "gram_panchayat_name": cells[
                    index["ग्राम पंचायत"]
                ].strip(),

                "gram_panchayat_code": cells[
                    index["ग्राम पंचायत कोड"]
                ].strip(),
            }

            if all(row.values()):
                result.append(row)

        return result

    raise RuntimeError(
        f"Target PRD table not found: {path}"
    )


def main():
    all_rows = {}
    failed = 0

    files = sorted(
        SOURCE.glob("*.html")
    )

    print(
        "Cached PRD files:",
        len(files),
    )

    for path in files:
        try:
            rows = parse_file(path)

            print(
                path.name,
                "->",
                len(rows),
                "rows",
            )

            for row in rows:
                key = (
                    row["district_name"],
                    row["block_code"],
                    row["gram_panchayat_code"],
                )

                all_rows[key] = row

        except Exception as exc:
            failed += 1
            print(
                path.name,
                "ERROR:",
                repr(exc),
            )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fields = [
        "district_name",
        "block_name",
        "block_code",
        "gram_panchayat_name",
        "gram_panchayat_code",
    ]

    with OUTPUT.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )

        writer.writeheader()

        for row in sorted(
            all_rows.values(),
            key=lambda r: (
                norm(r["district_name"]),
                norm(r["block_name"]),
                r["gram_panchayat_code"],
            ),
        ):
            writer.writerow(row)

    print()
    print(
        "TOTAL UNIQUE MAPPINGS:",
        len(all_rows),
    )

    print(
        "FAILED FILES:",
        failed,
    )

    print(
        "OUTPUT:",
        OUTPUT,
    )


if __name__ == "__main__":
    main()
