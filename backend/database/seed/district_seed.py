from sqlalchemy.orm import Session

from database.models.master.district import District
from database.models.master.division import Division


DATA = [
    {
        "district_name": "Ghazipur",
        "district_code": "GHAZIPUR",
        "division_code": "VARANASI",
    },
]


def seed_districts(db: Session):
    for item in DATA:

        division = (
            db.query(Division)
            .filter(
                Division.division_code
                == item["division_code"]
            )
            .first()
        )

        if division is None:
            raise RuntimeError(
                f"Division not found: "
                f"{item['division_code']}"
            )

        exists = (
            db.query(District)
            .filter(
                District.district_code
                == item["district_code"]
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ District already exists: "
                f"{item['district_name']}"
            )
            continue

        district = District(
            district_name=item["district_name"],
            district_code=item["district_code"],
            division_id=division.id,
        )

        db.add(district)

        print(
            f"✓ District added: "
            f"{item['district_name']}"
        )

    db.commit()

    print("✓ Districts seeded successfully")