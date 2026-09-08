from sqlalchemy.orm import Session

from core.database.session import SessionLocal
from database.models.government.office import Office
from database.models.government.department import Department


DATA = [
    {
        "office_name": "Electricity Department - Ghazipur Division Office",
        "office_code": "ELEC-GHAZ-DIV",
        "address": "Ghazipur, Uttar Pradesh",
        "phone": "0548-0000000",
        "email": "electricity.ghazipur@example.gov.in",
        "department_code": "ELEC",
    },
    {
        "office_name": "Rural Development Department - Ghazipur",
        "office_code": "RD-GHAZ-DIST",
        "address": "Ghazipur, Uttar Pradesh",
        "phone": "0548-0000001",
        "email": "rd.ghazipur@example.gov.in",
        "department_code": "RD",
    },
    {
        "office_name": "Public Works Department - Ghazipur",
        "office_code": "PWD-GHAZ-DIST",
        "address": "Ghazipur, Uttar Pradesh",
        "phone": "0548-0000002",
        "email": "pwd.ghazipur@example.gov.in",
        "department_code": "PWD",
    },
]


def seed_offices(db: Session):

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
            db.query(Office)
            .filter(
                Office.office_code
                == item["office_code"]
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ Office already exists: "
                f"{item['office_code']}"
            )
            continue

        office = Office(
            office_name=item["office_name"],
            office_code=item["office_code"],
            address=item["address"],
            phone=item["phone"],
            email=item["email"],
            department_id=department.id,
        )

        db.add(office)

    db.commit()

    print("✓ Offices Seeded")


def main():

    db = SessionLocal()

    try:
        seed_offices(db)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
