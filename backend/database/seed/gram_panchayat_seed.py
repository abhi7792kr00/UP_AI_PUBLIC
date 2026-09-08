from sqlalchemy.orm import Session

from database.models.master.gram_panchayat import (
    GramPanchayat,
)
from database.models.master.block import Block


DATA = [
    {
        "gram_panchayat_name": "Darvepur",
        "gram_panchayat_code": "DARVEPUR-GP",
        "block_code": "SAIDPUR-BLOCK",
    },
]


def seed_gram_panchayats(db: Session):
    for item in DATA:

        block = (
            db.query(Block)
            .filter(
                Block.block_code
                == item["block_code"]
            )
            .first()
        )

        if block is None:
            raise RuntimeError(
                f"Block not found: "
                f"{item['block_code']}"
            )

        exists = (
            db.query(GramPanchayat)
            .filter(
                GramPanchayat.gram_panchayat_code
                == item["gram_panchayat_code"]
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ Gram Panchayat already exists: "
                f"{item['gram_panchayat_name']}"
            )
            continue

        gram_panchayat = GramPanchayat(
            gram_panchayat_name=(
                item["gram_panchayat_name"]
            ),
            gram_panchayat_code=(
                item["gram_panchayat_code"]
            ),
            block_id=block.id,
        )

        db.add(gram_panchayat)

        print(
            f"✓ Gram Panchayat added: "
            f"{item['gram_panchayat_name']}"
        )

    db.commit()

    print(
        "✓ Gram Panchayats seeded successfully"
    )