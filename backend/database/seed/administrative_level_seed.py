from sqlalchemy.orm import Session

from database.models.master.administrative_level import AdministrativeLevel


DATA = [
    {
        "level_name": "State",
        "level_code": "STATE",
        "display_order": 1,
    },
    {
        "level_name": "Division",
        "level_code": "DIVISION",
        "display_order": 2,
    },
    {
        "level_name": "District",
        "level_code": "DISTRICT",
        "display_order": 3,
    },
    {
        "level_name": "Tehsil",
        "level_code": "TEHSIL",
        "display_order": 4,
    },
    {
        "level_name": "Block",
        "level_code": "BLOCK",
        "display_order": 5,
    },
    {
        "level_name": "Gram Panchayat",
        "level_code": "GRAM_PANCHAYAT",
        "display_order": 6,
    },
    {
        "level_name": "Village",
        "level_code": "VILLAGE",
        "display_order": 7,
    },
]


def seed_administrative_levels(db: Session):
    for item in DATA:

        exists = (
            db.query(AdministrativeLevel)
            .filter(
                AdministrativeLevel.level_code == item["level_code"]
            )
            .first()
        )

        if exists:
            continue

        db.add(
            AdministrativeLevel(**item)
        )

    db.commit()

    print("✓ Administrative Levels Seeded")