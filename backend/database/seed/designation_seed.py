from sqlalchemy.orm import Session

from core.database.session import SessionLocal

from database.models.government.designation import Designation
from database.models.government.department import Department


DATA = [
    {
        "designation_name": "Junior Engineer - Electricity",
        "designation_code": "JE-ELEC",
        "description": "Junior Engineer for Electricity Department",
        "department_code": "ELEC",
    },
    {
        "designation_name": "Assistant Engineer - Electricity",
        "designation_code": "AE-ELEC",
        "description": "Assistant Engineer for Electricity Department",
        "department_code": "ELEC",
    },
    {
        "designation_name": "Block Development Officer",
        "designation_code": "BDO-RD",
        "description": "Block Development Officer for Rural Development",
        "department_code": "RD",
    },
    {
        "designation_name": "Assistant Development Officer",
        "designation_code": "ADO-RD",
        "description": "Assistant Development Officer for Rural Development",
        "department_code": "RD",
    },
    {
        "designation_name": "Junior Engineer - PWD",
        "designation_code": "JE-PWD",
        "description": "Junior Engineer for Public Works Department",
        "department_code": "PWD",
    },
    {
        "designation_name": "Assistant Engineer - PWD",
        "designation_code": "AE-PWD",
        "description": "Assistant Engineer for Public Works Department",
        "department_code": "PWD",
    },
]


def seed_designations(db: Session):

    for item in DATA:

        department = (
            db.query(Department)
            .filter(
                Department.department_code
                == item["department_code"]
            )
            .first()
        )

        if department is None:
            print(
                f"⚠️ Department not found: "
                f"{item['department_code']}"
            )
            continue

        exists = (
            db.query(Designation)
            .filter(
                Designation.designation_code
                == item["designation_code"]
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ Designation already exists: "
                f"{item['designation_code']}"
            )
            continue

        designation = Designation(
            designation_name=item["designation_name"],
            designation_code=item["designation_code"],
            description=item["description"],
            department_id=department.id,
        )

        db.add(designation)

    db.commit()

    print("✓ Designations Seeded")


def main():

    db = SessionLocal()

    try:
        seed_designations(db)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
