from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


LGD_DISTRICTS = Path(
    "data/master/up/districts.csv"
)

LGD_BLOCKS = Path(
    "data/master/up/blocks.csv"
)

LGD_GPS = Path(
    "data/master/up/gram_panchayats.csv"
)

PRD = Path(
    "data/source/up/"
    "prd_gram_panchayat_block.csv"
)

OUT_DIR = Path(
    "data/source/up/reconciliation"
)


def norm(value: str) -> str:
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


ALIASES = {
    "bara banki": "bara banki",
    "kushi nagar": "kushinagar",
    "maharajganj": "mahrajganj",
    "sant kabeer nagar": "sant kabir nagar",
    "sant ravidas nagar": "bhadohi",
    "shravasti": "shrawasti",
    "siddharth nagar": "siddharthnagar",
}


def district_alias(name: str) -> str:
    key = norm(name)
    return ALIASES.get(key, key)


def read_csv(path: Path):
    with path.open(
        newline="",
        encoding="utf-8-sig",
    ) as f:
        return list(csv.DictReader(f))


def main():
    districts = read_csv(
        LGD_DISTRICTS
    )

    blocks = read_csv(
        LGD_BLOCKS
    )

    gps = read_csv(
        LGD_GPS
    )

    prd = read_csv(
        PRD
    )

    # -----------------------------------------------------
    # District indexes
    # -----------------------------------------------------

    district_by_code = {
        r["district_code"]: r
        for r in districts
    }

    district_code_by_name = {
        district_alias(
            r["district_name"]
        ): r["district_code"]
        for r in districts
    }

    # -----------------------------------------------------
    # LGD block indexes
    # -----------------------------------------------------

    lgd_blocks_by_name = defaultdict(list)

    for row in blocks:
        district_code = row[
            "district_code"
        ]

        key = (
            district_code,
            norm(row["block_name"]),
        )

        lgd_blocks_by_name[
            key
        ].append(row)

    # -----------------------------------------------------
    # LGD GP indexes
    # -----------------------------------------------------

    lgd_gp_by_code = {
        r["gram_panchayat_code"]: r
        for r in gps
    }

    # -----------------------------------------------------
    # PRD GP indexes
    # -----------------------------------------------------

    prd_by_gp = defaultdict(list)

    for row in prd:
        prd_by_gp[
            row["gram_panchayat_code"]
        ].append(row)

    # -----------------------------------------------------
    # Exact GP-code reconciliation
    # -----------------------------------------------------

    exact_matches = []
    lgd_missing_prd = []
    prd_only = []

    for code, lgd_gp in (
        lgd_gp_by_code.items()
    ):
        rows = prd_by_gp.get(code, [])

        if not rows:
            lgd_missing_prd.append(
                lgd_gp
            )
            continue

        for row in rows:
            exact_matches.append(
                (
                    lgd_gp,
                    row,
                )
            )

    for code, rows in prd_by_gp.items():
        if code not in lgd_gp_by_code:
            prd_only.extend(rows)

    # -----------------------------------------------------
    # Block reconciliation for exact GP matches
    # -----------------------------------------------------

    block_matches = []
    block_missing = []
    block_ambiguous = []

    for lgd_gp, prd_row in exact_matches:

        district_code = lgd_gp[
            "district_code"
        ]

        key = (
            district_code,
            norm(
                prd_row[
                    "block_name"
                ]
            ),
        )

        candidates = lgd_blocks_by_name.get(
            key,
            []
        )

        base = {
            "district_code":
                district_code,

            "district_name":
                district_by_code[
                    district_code
                ]["district_name"],

            "gram_panchayat_code":
                lgd_gp[
                    "gram_panchayat_code"
                ],

            "gram_panchayat_name":
                lgd_gp[
                    "gram_panchayat_name"
                ],

            "prd_block_name":
                prd_row[
                    "block_name"
                ],

            "prd_block_code":
                prd_row[
                    "block_code"
                ],
        }

        if len(candidates) == 1:
            block = candidates[0]

            block_matches.append(
                {
                    **base,
                    "lgd_block_code":
                        block[
                            "block_code"
                        ],
                    "lgd_block_name":
                        block[
                            "block_name"
                        ],
                }
            )

        elif len(candidates) == 0:
            block_missing.append(base)

        else:
            block_ambiguous.append(
                base
            )

    # -----------------------------------------------------
    # District-level statistics
    # -----------------------------------------------------

    stats = defaultdict(
        lambda: {
            "lgd_gp": 0,
            "prd_gp": 0,
            "exact_gp": 0,
            "block_matched": 0,
            "block_missing": 0,
            "prd_only": 0,
        }
    )

    for row in gps:
        stats[
            row["district_code"]
        ]["lgd_gp"] += 1

    for row in prd:
        district_name = district_alias(
            row["district_name"]
        )

        district_code = (
            district_code_by_name.get(
                district_name
            )
        )

        if district_code:
            stats[
                district_code
            ]["prd_gp"] += 1

    for lgd_gp, _ in exact_matches:
        stats[
            lgd_gp["district_code"]
        ]["exact_gp"] += 1

    for row in block_matches:
        stats[
            row["district_code"]
        ]["block_matched"] += 1

    for row in block_missing:
        stats[
            row["district_code"]
        ]["block_missing"] += 1

    for row in prd_only:
        district_name = district_alias(
            row["district_name"]
        )

        district_code = (
            district_code_by_name.get(
                district_name
            )
        )

        if district_code:
            stats[
                district_code
            ]["prd_only"] += 1

    # -----------------------------------------------------
    # Output
    # -----------------------------------------------------

    OUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    def write(
        filename,
        fields,
        rows,
    ):
        path = OUT_DIR / filename

        with path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=fields,
            )

            writer.writeheader()

            for row in rows:
                writer.writerow(row)

    write(
        "block_matches.csv",
        [
            "district_code",
            "district_name",
            "gram_panchayat_code",
            "gram_panchayat_name",
            "prd_block_name",
            "prd_block_code",
            "lgd_block_name",
            "lgd_block_code",
        ],
        block_matches,
    )

    write(
        "block_missing.csv",
        list(
            block_missing[0].keys()
        )
        if block_missing
        else [
            "district_code",
            "district_name",
            "gram_panchayat_code",
            "gram_panchayat_name",
            "prd_block_name",
            "prd_block_code",
        ],
        block_missing,
    )

    write(
        "lgd_missing_prd.csv",
        [
            "district_code",
            "district_name",
            "gram_panchayat_code",
            "gram_panchayat_name",
            "parent_kp_code",
        ],
        [
            {
                "district_code":
                    r["district_code"],
                "district_name":
                    district_by_code[
                        r["district_code"]
                    ]["district_name"],
                "gram_panchayat_code":
                    r["gram_panchayat_code"],
                "gram_panchayat_name":
                    r["gram_panchayat_name"],
                "parent_kp_code":
                    r["parent_kp_code"],
            }
            for r in lgd_missing_prd
        ],
    )

    write(
        "prd_only.csv",
        [
            "district_name",
            "block_name",
            "block_code",
            "gram_panchayat_name",
            "gram_panchayat_code",
        ],
        prd_only,
    )

    stats_rows = []

    for code in sorted(
        stats,
        key=lambda x: int(x)
        if x.isdigit()
        else x,
    ):
        row = stats[code]

        row = {
            "district_code": code,
            "district_name":
                district_by_code.get(
                    code,
                    {}
                ).get(
                    "district_name",
                    "",
                ),
            **row,
        }

        stats_rows.append(row)

    write(
        "district_stats.csv",
        [
            "district_code",
            "district_name",
            "lgd_gp",
            "prd_gp",
            "exact_gp",
            "block_matched",
            "block_missing",
            "prd_only",
        ],
        stats_rows,
    )

    # -----------------------------------------------------
    # Console summary
    # -----------------------------------------------------

    print(
        "========== RECONCILIATION =========="
    )

    print(
        "LGD GP:",
        len(lgd_gp_by_code),
    )

    print(
        "PRD GP:",
        len(prd_by_gp),
    )

    print(
        "EXACT GP MATCH:",
        len(exact_matches),
    )

    print(
        "LGD WITHOUT PRD:",
        len(lgd_missing_prd),
    )

    print(
        "PRD ONLY:",
        len(prd_only),
    )

    print(
        "BLOCK MATCHED:",
        len(block_matches),
    )

    print(
        "BLOCK MISSING:",
        len(block_missing),
    )

    print(
        "BLOCK AMBIGUOUS:",
        len(block_ambiguous),
    )

    print()
    print(
        "OUTPUT:",
        OUT_DIR,
    )


if __name__ == "__main__":
    main()
