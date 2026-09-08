from sqlalchemy.orm import Session

from core.database.session import SessionLocal
from database.models.master.state import State


DATA = [
    {
        "state_name": "Uttar Pradesh",
        "state_code": "UP",
    },
]


def seed_states(db: Session | None = None):
    own_session = False

    if db is None:
        db = SessionLocal()
        own_session = True

    try:
        for item in DATA:
            exists = (
                db.query(State)
                .filter(
                    State.state_code == item["state_code"]
                )
                .first()
            )

            if exists:
                print(
                    f"⚠️ State already exists: "
                    f"{item['state_name']}"
                )
                continue

            db.add(State(**item))

            print(
                f"✓ State added: "
                f"{item['state_name']}"
            )

        db.commit()

        print("✓ States seeded successfully")

    except Exception:
        db.rollback()
        raise

    finally:
        if own_session:
            db.close()