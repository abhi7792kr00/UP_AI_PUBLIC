from __future__ import annotations

import csv
from pathlib import Path


RESOLVED = Path(
    "data/source/up/reconciliation/"
    "gp_block_resolved.csv"
)

LGD_GP = Path(
    "data/master/up/gram_panchayats.csv"
)

LGD_BLOCKS = Path(
    "data/master/up/blocks.csv"
)

OUT = Path(
    "data/source/up/reconciliation/"
    "final_gp_block_mapping.csv"
)

PRD_ONLY = Path(
    "data/source/up/reconciliation/"
    "prd_only_gp_block_mapping.csv"
)


def read(path: Path, encoding="utf-8"):
    with path.open(
        newline="",
        encoding=encoding,
    ) as f:
        return list(csv.DictReader(f))


def main():
    resolved = read(RESOLVED)
    gps = read(
        LGD_GP,
        "utf-8-sig",
    )
    blocks = read(
        LGD_BLOCKS,
        "utf-8-sig",
    )

    lgd_gp_codes = {
        row["gram_panchayat_code"]
        for row in gps
    }

    lgd_block_codes = {
        row["block_code"]
        for row in blocks
    }

    safe = []
    prd_only = []

    seen_gp = set()

    for row in resolved:
        gp_code = row[
            "gram_panchayat_code"
        ]

        if gp_code in seen_gp:
            raise RuntimeError(
                f"Duplicate GP mapping: {gp_code}"
            )

        seen_gp.add(gp_code)

        if gp_code not in lgd_gp_codes:
            prd_only.append(row)
            continue

        block_code = row[
            "lgd_block_code"
        ]

        if block_code not in lgd_block_codes:
            raise RuntimeError(
                "Resolved block_code does not "
                f"exist in LGD blocks: "
                f"{block_code}"
            )

        safe.append(
            {
                "district_code":
                    row["district_code"],
                "gram_panchayat_code":
                    gp_code,
                "block_code":
                    block_code,
                "resolution":
                    row["resolution"],
            }
        )

    OUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fields = [
        "district_code",
        "gram_panchayat_code",
        "block_code",
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
        writer.writerows(safe)

    with PRD_ONLY.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "district_code",
                "district_name",
                "gram_panchayat_code",
                "gram_panchayat_name",
                "prd_block_name",
                "prd_block_code",
                "lgd_block_code",
                "lgd_block_name",
                "resolution",
            ],
        )

        writer.writeheader()
        writer.writerows(prd_only)

    print("========== FINAL GP → BLOCK MAPPING ==========")
    print("RESOLVED PRD:", len(resolved))
    print("LGD-VALID:", len(safe))
    print("PRD-ONLY:", len(prd_only))
    print("OUTPUT:", OUT)
    print("PRD-ONLY OUTPUT:", PRD_ONLY)


if __name__ == "__main__":
    main()
