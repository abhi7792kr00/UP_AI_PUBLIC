from sqlalchemy.orm import Session

from database.models.master.block import Block
from database.models.master.tehsil import Tehsil


DATA = [
    {
        "block_name": "Saidpur",
        "block_code": "SAIDPUR-BLOCK",
        "tehsil_code": "SAIDPUR",
    },
]


def seed_blocks(db: Session):
    for item in DATA:

        tehsil = (
            db.query(Tehsil)
            .filter(
                Tehsil.tehsil_code == item["tehsil_code"]
            )
            .first()
        )

        if tehsil is None:
            raise RuntimeError(
                f"Tehsil not found: {item['tehsil_code']}"
            )

        exists = (
            db.query(Block)
            .filter(
                Block.block_code == item["block_code"]
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ Block already exists: "
                f"{item['block_name']}"
            )
            continue

        block = Block(
            block_name=item["block_name"],
            block_code=item["block_code"],
            district_id=tehsil.district_id,
        )

        block.tehsils.append(tehsil)

        db.add(block)

        print(
            f"✓ Block added: "
            f"{item['block_name']}"
        )

    db.commit()

    print("✓ Blocks seeded successfully")
