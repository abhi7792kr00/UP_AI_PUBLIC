from __future__ import annotations

import csv
import re
from pathlib import Path


RAW = Path(
    "data/source/up/block_tehsil_raw.csv"
)

BLOCKS = Path(
    "data/master/up/blocks.csv"
)

TEHSILS = Path(
    "data/master/up/tehsils.csv"
)

OUT = Path(
    "data/source/up/reconciliation/"
    "block_tehsil_mapping.csv"
)


def norm(value: str) -> str:
    value = value.lower().strip()
    return re.sub(r"\s+", " ", value)


# Only verified source-name -> LGD-name variants.
BLOCK_ALIASES = {
    ("120", "bahariya"): "bahria",
    ("120", "kaundhiyara"): "kaudhiyara",
    ("120", "uruwa"): "uruwan",
    ("120", "shringverpur dham"): "sringverpur dham",

    ("157", "vidhnu"): "vidhunu",
    ("157", "sarsaul"): "sarsol",
}

TEHSIL_ALIASES = {
    ("120", "soroan"): "soraon",
    ("157", "kanpur sadar"): "kanpur",
}


def read_csv(path: Path, encoding: str):
    with path.open(
        newline="",
        encoding=encoding,
    ) as f:
        return list(csv.DictReader(f))


def main():
    raw = read_csv(RAW, "utf-8")
    blocks = read_csv(BLOCKS, "utf-8-sig")
    tehsils = read_csv(TEHSILS, "utf-8-sig")

    block_index = {
        (
            row["district_code"],
            norm(row["block_name"]),
        ): row
        for row in blocks
    }

    tehsil_index = {
        (
            row["district_code"],
            norm(row["tehsil_name"]),
        ): row
        for row in tehsils
    }

    output = []
    unresolved = []

    seen = set()

    for row in raw:
        district_code = row[
            "district_code"
        ]

        source_block = norm(
            row["block_name"]
        )

        source_tehsil = norm(
            row["tehsil_name"]
        )

        block_key = (
            district_code,
            BLOCK_ALIASES.get(
                (
                    district_code,
                    source_block,
                ),
                source_block,
            ),
        )

        tehsil_key = (
            district_code,
            TEHSIL_ALIASES.get(
                (
                    district_code,
                    source_tehsil,
                ),
                source_tehsil,
            ),
        )

        block = block_index.get(
            block_key
        )

        tehsil = tehsil_index.get(
            tehsil_key
        )

        if block is None or tehsil is None:
            unresolved.append(
                row
            )
            continue

        # Ensure Block and Tehsil belong
        # to the same district.
        if (
            block["district_code"]
            != tehsil["district_code"]
        ):
            unresolved.append(row)
            continue

        key = (
            district_code,
            block["block_code"],
            tehsil["tehsil_code"],
        )

        if key in seen:
            continue

        seen.add(key)

        resolution = (
            "exact"
        )

        if (
            (
                district_code,
                source_block,
            )
            in BLOCK_ALIASES
            or (
                district_code,
                source_tehsil,
            )
            in TEHSIL_ALIASES
        ):
            resolution = (
                "verified_name_variant"
            )

        output.append(
            {
                "district_code":
                    district_code,
                "district_name":
                    row["district_name"],
                "block_code":
                    block["block_code"],
                "block_name":
                    block["block_name"],
                "tehsil_code":
                    tehsil["tehsil_code"],
                "tehsil_name":
                    tehsil["tehsil_name"],
                "source_block_name":
                    row["block_name"],
                "source_tehsil_name":
                    row["tehsil_name"],
                "source_url":
                    row["source_url"],
                "resolution":
                    resolution,
            }
        )

    OUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fields = [
        "district_code",
        "district_name",
        "block_code",
        "block_name",
        "tehsil_code",
        "tehsil_name",
        "source_block_name",
        "source_tehsil_name",
        "source_url",
        "resolution",
    ]

    with OUT.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fields,
        )
        writer.writeheader()
        writer.writerows(output)

    print(
        "========== BLOCK → TEHSIL MAPPING =========="
    )
    print("RAW ROWS:", len(raw))
    print("RESOLVED:", len(output))
    print("UNRESOLVED:", len(unresolved))
    print("OUTPUT:", OUT)

    if unresolved:
        print("\nUNRESOLVED ROWS:")
        for row in unresolved:
            print(
                row["district_name"],
                "|",
                row["block_name"],
                "|",
                row["tehsil_name"],
            )


if __name__ == "__main__":
    main()
