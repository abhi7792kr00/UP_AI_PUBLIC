from pathlib import Path

from core.database.session import SessionLocal
from core.utils.csv_reader import read_csv

from database.models.master.state import State


def import_states():

    db = SessionLocal()

    csv_file = (
        Path(__file__).resolve().parent.parent.parent
        / "data"
        / "states"
        / "up"
        / "state.csv"
    )

    rows = read_csv(csv_file)

    for row in rows:

        exists = (
            db.query(State)
            .filter(State.state_code == row["state_code"])
            .first()
        )

        if exists:
            continue

        db.add(
            State(
                state_name=row["state_name"],
                state_code=row["state_code"],
            )
        )

    db.commit()
    db.close()

    print("✅ States Imported")