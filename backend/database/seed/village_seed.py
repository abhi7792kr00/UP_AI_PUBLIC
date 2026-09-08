from sqlalchemy.orm import Session

from database.models.master.village import Village
from database.models.master.gram_panchayat import (
    GramPanchayat,
)


DATA = [
    {
        "village_name": "Darvepur",
        "village_code": "DARVEPUR",
        "gram_panchayat_code": "DARVEPUR-GP",
    },
]


def seed_villages(db: Session):
    for item in DATA:

        gram_panchayat = (
            db.query(GramPanchayat)
            .filter(
                GramPanchayat.gram_panchayat_code
                == item["gram_panchayat_code"]
            )
            .first()
        )

        if gram_panchayat is None:
            raise RuntimeError(
                "Gram Panchayat not found: "
                f"{item['gram_panchayat_code']}"
            )

        exists = (
            db.query(Village)
            .filter(
                Village.village_code
                == item["village_code"]
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ Village already exists: "
                f"{item['village_name']}"
            )
            continue

        village = Village(
            village_name=item["village_name"],
            village_code=item["village_code"],
            gram_panchayat_id=gram_panchayat.id,
        )

        db.add(village)

        print(
            f"✓ Village added: "
            f"{item['village_name']}"
        )

    db.commit()

    print("✓ Villages seeded successfully")