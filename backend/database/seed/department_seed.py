from sqlalchemy.orm import Session

from database.models.government.department import (
    Department,
)


DATA = [
    {
        "department_name": "Electricity Department",
        "department_code": "ELEC",
        "description": (
            "Electricity and power related complaints"
        ),
    },

    {
        "department_name": "Public Works Department",
        "department_code": "PWD",
        "description": (
            "Road and public infrastructure related services"
        ),
    },
]


def seed_departments(db: Session):
    for item in DATA:

        exists = (
            db.query(Department)
            .filter(
                Department.department_code
                == item["department_code"]
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ Department already exists: "
                f"{item['department_name']}"
            )
            continue

        department = Department(
            department_name=item["department_name"],
            department_code=item["department_code"],
            description=item["description"],
        )

        db.add(department)

        print(
            f"✓ Department added: "
            f"{item['department_name']}"
        )

    db.commit()

    print("✓ Departments seeded successfully")