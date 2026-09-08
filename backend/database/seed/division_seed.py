from sqlalchemy.orm import Session

from database.models.master.division import Division
from database.models.master.state import State


DATA = [
    {
        "division_name": "Varanasi",
        "division_code": "VARANASI",
        "state_code": "UP",
    },
]


def seed_divisions(db: Session):
    for item in DATA:

        state = (
            db.query(State)
            .filter(
                State.state_code == item["state_code"]
            )
            .first()
        )

        if state is None:
            raise RuntimeError(
                f"State not found: {item['state_code']}"
            )

        exists = (
            db.query(Division)
            .filter(
                Division.division_code
                == item["division_code"]
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ Division already exists: "
                f"{item['division_name']}"
            )
            continue

        division = Division(
            division_name=item["division_name"],
            division_code=item["division_code"],
            state_id=state.id,
        )

        db.add(division)

        print(
            f"✓ Division added: "
            f"{item['division_name']}"
        )

    db.commit()

    print("✓ Divisions seeded successfully")