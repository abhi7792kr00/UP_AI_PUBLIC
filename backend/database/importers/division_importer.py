from pathlib import Path

from core.database.session import SessionLocal
from core.utils.csv_reader import read_csv

from database.models.master.state import State
from database.models.master.division import Division


def import_divisions():

    db = SessionLocal()

    csv_file = (
        Path(__file__).resolve().parent.parent.parent
        / "data"
        / "states"
        / "up"
        / "division.csv"
    )

    rows = read_csv(csv_file)

    for row in rows:

        state = (
            db.query(State)
            .filter(State.state_code == row["state_code"])
            .first()
        )

        if not state:
            continue

        exists = (
            db.query(Division)
            .filter(Division.division_code == row["division_code"])
            .first()
        )

        if exists:
            continue

        db.add(
            Division(
                division_name=row["division_name"],
                division_code=row["division_code"],
                state_id=state.id
            )
        )

    db.commit()
    db.close()

    print("✅ Divisions Imported")