from __future__ import annotations

import csv
import re
from difflib import SequenceMatcher
from pathlib import Path


RAW = Path("data/source/up/block_tehsil_raw.csv")
BLOCKS = Path("data/master/up/blocks.csv")
TEHSILS = Path("data/master/up/tehsils.csv")

OUT = Path(
    "data/source/up/reconciliation/"
    "block_tehsil_review.csv"
)


def norm(value: str) -> str:
    value = value.lower().strip()
    return re.sub(r"\s+", " ", value)


def score(a: str, b: str) -> float:
    return SequenceMatcher(
        None,
        norm(a),
        norm(b),
    ).ratio()


def read(path: Path, encoding="utf-8-sig"):
    with path.open(
        newline="",
        encoding=encoding,
    ) as f:
        return list(csv.DictReader(f))


def main():
    raw = read(RAW, "utf-8")
    blocks = read(BLOCKS)
    tehsils = read(TEHSILS)

    block_index = {
        (
            r["district_code"],
            norm(r["block_name"]),
        )
        for r in blocks
    }

    tehsil_index = {
        (
            r["district_code"],
            norm(r["tehsil_name"]),
        )
        for r in tehsils
    }

    rows = []

    for r in raw:
        district = r["district_code"]

        block_exact = (
            district,
            norm(r["block_name"]),
        ) in block_index

        tehsil_exact = (
            district,
            norm(r["tehsil_name"]),
        ) in tehsil_index

        if block_exact and tehsil_exact:
            continue

        block_candidates = []

        if not block_exact:
            for b in blocks:
                if b["district_code"] != district:
                    continue

                block_candidates.append(
                    (
                        score(
                            r["block_name"],
                            b["block_name"],
                        ),
                        b["block_code"],
                        b["block_name"],
                    )
                )

        tehsil_candidates = []

        if not tehsil_exact:
            for t in tehsils:
                if t["district_code"] != district:
                    continue

                tehsil_candidates.append(
                    (
                        score(
                            r["tehsil_name"],
                            t["tehsil_name"],
                        ),
                        t["tehsil_code"],
                        t["tehsil_name"],
                    )
                )

        block_candidates.sort(reverse=True)
        tehsil_candidates.sort(reverse=True)

        best_block = (
            block_candidates[0]
            if block_candidates
            else ("", "", "")
        )

        best_tehsil = (
            tehsil_candidates[0]
            if tehsil_candidates
            else ("", "", "")
        )

        rows.append(
            {
                "district_code": district,
                "district_name":
                    r["district_name"],
                "source_block_name":
                    r["block_name"],
                "source_tehsil_name":
                    r["tehsil_name"],
                "best_lgd_block_code":
                    best_block[1],
                "best_lgd_block_name":
                    best_block[2],
                "block_score":
                    f"{best_block[0]:.3f}"
                    if best_block[0] != ""
                    else "",
                "best_lgd_tehsil_code":
                    best_tehsil[1],
                "best_lgd_tehsil_name":
                    best_tehsil[2],
                "tehsil_score":
                    f"{best_tehsil[0]:.3f}"
                    if best_tehsil[0] != ""
                    else "",
            }
        )

    OUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fields = [
        "district_code",
        "district_name",
        "source_block_name",
        "source_tehsil_name",
        "best_lgd_block_code",
        "best_lgd_block_name",
        "block_score",
        "best_lgd_tehsil_code",
        "best_lgd_tehsil_name",
        "tehsil_score",
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
        writer.writerows(rows)

    print("REVIEW ROWS:", len(rows))
    print("OUTPUT:", OUT)


if __name__ == "__main__":
    main()
