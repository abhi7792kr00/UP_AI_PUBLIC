from __future__ import annotations

import csv
from pathlib import Path


DISTRICTS = Path(
    "data/master/up/districts.csv"
)

PRD = Path(
    "data/source/up/"
    "prd_gram_panchayat_block.csv"
)

BLOCKS = Path(
    "data/master/up/blocks.csv"
)

ALIASES = Path(
    "data/master/up/mappings/"
    "block_name_aliases.csv"
)

OUT = Path(
    "data/source/up/reconciliation/"
    "gp_block_resolved.csv"
)

UNRESOLVED = Path(
    "data/source/up/reconciliation/"
    "gp_block_unresolved.csv"
)


def norm(value: str) -> str:
    return " ".join(
        value.strip().lower().split()
    )


def read_csv(
    path: Path,
    encoding: str = "utf-8-sig",
):
    with path.open(
        newline="",
        encoding=encoding,
    ) as f:
        return list(
            csv.DictReader(f)
        )


def main():
    districts = read_csv(DISTRICTS)
    prd = read_csv(PRD, "utf-8")
    blocks = read_csv(BLOCKS)
    aliases = read_csv(ALIASES)

    # --------------------------------------------------
    # District name -> LGD district code
    # --------------------------------------------------

    district_by_name = {
        norm(row["district_name"]):
            row["district_code"]
        for row in districts
    }

    # Known district-name variants
    district_aliases = {
        "bara banki": "bara banki",
        "kushi nagar": "kushinagar",
        "maharajganj": "mahrajganj",
        "sant kabeer nagar":
            "sant kabir nagar",
        "sant ravidas nagar":
            "bhadohi",
        "shravasti": "shrawasti",
        "siddharth nagar":
            "siddharthnagar",
    }

    def district_code_for(name: str):
        key = norm(name)

        key = district_aliases.get(
            key,
            key,
        )

        return district_by_name.get(
            key
        )

    # --------------------------------------------------
    # LGD block index
    # --------------------------------------------------

    block_by_name = {}

    for row in blocks:
        key = (
            row["district_code"],
            norm(row["block_name"]),
        )

        if key in block_by_name:
            raise RuntimeError(
                "Duplicate LGD block key: "
                + repr(key)
            )

        block_by_name[key] = row

    # --------------------------------------------------
    # Explicit aliases
    # --------------------------------------------------

    alias_by_name = {}

    for row in aliases:
        alias_by_name[
            (
                row["district_code"],
                norm(
                    row["prd_block_name"]
                ),
            )
        ] = row

    # --------------------------------------------------
    # Resolve
    # --------------------------------------------------

    resolved = []
    unresolved = []

    seen_gp = set()

    for row in prd:
        gp_code = row[
            "gram_panchayat_code"
        ]

        if gp_code in seen_gp:
            continue

        seen_gp.add(gp_code)

        district_code = (
            district_code_for(
                row["district_name"]
            )
        )

        base = {
            "district_code":
                district_code or "",
            "district_name":
                row["district_name"],
            "gram_panchayat_code":
                gp_code,
            "gram_panchayat_name":
                row["gram_panchayat_name"],
            "prd_block_name":
                row["block_name"],
            "prd_block_code":
                row["block_code"],
        }

        if not district_code:
            unresolved.append(
                {
                    **base,
                    "resolution":
                        "district_unresolved",
                }
            )
            continue

        # ----------------------------------------------
        # 1. Exact block-name match
        # ----------------------------------------------

        exact = block_by_name.get(
            (
                district_code,
                norm(
                    row["block_name"]
                ),
            )
        )

        if exact:
            resolved.append(
                {
                    **base,
                    "lgd_block_code":
                        exact["block_code"],
                    "lgd_block_name":
                        exact["block_name"],
                    "resolution":
                        "exact_name",
                }
            )
            continue

        # ----------------------------------------------
        # 2. Explicit alias
        # ----------------------------------------------

        alias = alias_by_name.get(
            (
                district_code,
                norm(
                    row["block_name"]
                ),
            )
        )

        if alias:
            lgd = block_by_name.get(
                (
                    district_code,
                    norm(
                        alias["lgd_block_name"]
                    ),
                )
            )

            if lgd:
                resolved.append(
                    {
                        **base,
                        "lgd_block_code":
                            lgd["block_code"],
                        "lgd_block_name":
                            lgd["block_name"],
                        "resolution":
                            "explicit_alias",
                    }
                )
                continue

        unresolved.append(
            {
                **base,
                "resolution":
                    "block_unresolved",
            }
        )

    # --------------------------------------------------
    # Write resolved
    # --------------------------------------------------

    OUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    resolved_fields = [
        "district_code",
        "district_name",
        "gram_panchayat_code",
        "gram_panchayat_name",
        "prd_block_name",
        "prd_block_code",
        "lgd_block_code",
        "lgd_block_name",
        "resolution",
    ]

    with OUT.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=resolved_fields,
        )

        writer.writeheader()
        writer.writerows(
            resolved
        )

    # --------------------------------------------------
    # Write unresolved
    # --------------------------------------------------

    unresolved_fields = [
        "district_code",
        "district_name",
        "gram_panchayat_code",
        "gram_panchayat_name",
        "prd_block_name",
        "prd_block_code",
        "resolution",
    ]

    with UNRESOLVED.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=unresolved_fields,
        )

        writer.writeheader()
        writer.writerows(
            unresolved
        )

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    exact_count = sum(
        r["resolution"]
        == "exact_name"
        for r in resolved
    )

    alias_count = sum(
        r["resolution"]
        == "explicit_alias"
        for r in resolved
    )

    print(
        "========== GP → BLOCK RESOLUTION =========="
    )

    print(
        "PRD UNIQUE GP:",
        len(seen_gp),
    )

    print(
        "RESOLVED:",
        len(resolved),
    )

    print(
        "  exact_name:",
        exact_count,
    )

    print(
        "  explicit_alias:",
        alias_count,
    )

    print(
        "UNRESOLVED:",
        len(unresolved),
    )

    print(
        "OUTPUT:",
        OUT,
    )

    print(
        "UNRESOLVED OUTPUT:",
        UNRESOLVED,
    )


if __name__ == "__main__":
    main()
