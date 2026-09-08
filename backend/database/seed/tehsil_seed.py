from sqlalchemy.orm import Session

from database.models.master.tehsil import Tehsil
from database.models.master.district import District


DATA = [
    {
        "tehsil_name": "Saidpur",
        "tehsil_code": "SAIDPUR",
        "district_code": "GHAZIPUR",
    },
]


def seed_tehsils(db: Session):
    for item in DATA:

        district = (
            db.query(District)
            .filter(
                District.district_code
                == item["district_code"]
            )
            .first()
        )

        if district is None:
            raise RuntimeError(
                f"District not found: "
                f"{item['district_code']}"
            )

        exists = (
            db.query(Tehsil)
            .filter(
                Tehsil.tehsil_code
                == item["tehsil_code"]
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ Tehsil already exists: "
                f"{item['tehsil_name']}"
            )
            continue

        tehsil = Tehsil(
            tehsil_name=item["tehsil_name"],
            tehsil_code=item["tehsil_code"],
            district_id=district.id,
        )

        db.add(tehsil)

        print(
            f"✓ Tehsil added: "
            f"{item['tehsil_name']}"
        )

    db.commit()

    print("✓ Tehsils seeded successfully")