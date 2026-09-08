from __future__ import annotations

import csv

from sqlalchemy import text

from core.database.session import SessionLocal


MAP = (
    "data/source/up/reconciliation/"
    "block_tehsil_mapping.csv"
)


def main():
    with open(
        MAP,
        newline="",
        encoding="utf-8-sig",
    ) as f:
        rows = list(csv.DictReader(f))

    verified = [
        row
        for row in rows
        if row["resolution"].strip()
        in {
            "exact",
            "verified_name_variant",
        }
    ]

    db = SessionLocal()

    inserted = 0
    existing = 0

    try:
        block_ids = {}
        tehsil_ids = {}

        for row in verified:
            block = db.execute(
                text("""
                    SELECT id
                    FROM blocks
                    WHERE block_code = :code
                """),
                {
                    "code": row["block_code"].strip()
                },
            ).fetchone()

            tehsil = db.execute(
                text("""
                    SELECT id
                    FROM tehsils
                    WHERE tehsil_code = :code
                """),
                {
                    "code": row["tehsil_code"].strip()
                },
            ).fetchone()

            if block is None:
                raise RuntimeError(
                    f"Block not found: "
                    f"{row['block_code']}"
                )

            if tehsil is None:
                raise RuntimeError(
                    f"Tehsil not found: "
                    f"{row['tehsil_code']}"
                )

            block_ids[
                row["block_code"].strip()
            ] = block[0]

            tehsil_ids[
                row["tehsil_code"].strip()
            ] = tehsil[0]

        for row in verified:
            block_id = block_ids[
                row["block_code"].strip()
            ]

            tehsil_id = tehsil_ids[
                row["tehsil_code"].strip()
            ]

            exists = db.execute(
                text("""
                    SELECT 1
                    FROM block_tehsils
                    WHERE block_id = :block_id
                      AND tehsil_id = :tehsil_id
                """),
                {
                    "block_id": block_id,
                    "tehsil_id": tehsil_id,
                },
            ).fetchone()

            if exists:
                existing += 1
                continue

            db.execute(
                text("""
                    INSERT INTO block_tehsils (
                        block_id,
                        tehsil_id,
                        created_at,
                        updated_at,
                        is_active
                    )
                    VALUES (
                        :block_id,
                        :tehsil_id,
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP,
                        1
                    )
                """),
                {
                    "block_id": block_id,
                    "tehsil_id": tehsil_id,
                },
            )

            inserted += 1

        db.commit()

        print(
            "========== BLOCK → TEHSIL =========="
        )
        print("Verified source rows:", len(verified))
        print("Inserted:", inserted)
        print("Already existing:", existing)
        print("TOTAL:", inserted + existing)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
