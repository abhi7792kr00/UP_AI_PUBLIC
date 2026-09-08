from sqlalchemy.orm import Session

from core.database.session import SessionLocal

from database.models.government.officer import Officer
from database.models.government.department import Department
from database.models.government.office import Office
from database.models.government.designation import Designation


DATA = [
    {
        "officer_name": "Electricity Junior Engineer - Ghazipur",
        "employee_code": "EMP-ELEC-JE-001",
        "mobile": "9000000001",
        "email": "je.electricity.ghazipur@example.gov.in",
        "department_code": "ELEC",
        "office_code": "ELEC-GHAZ-DIV",
        "designation_code": "JE-ELEC",
    },
    {
        "officer_name": "PWD Junior Engineer - Ghazipur",
        "employee_code": "EMP-PWD-JE-001",
        "mobile": "9000000002",
        "email": "je.pwd.ghazipur@example.gov.in",
        "department_code": "PWD",
        "office_code": "PWD-GHAZ-DIST",
        "designation_code": "JE-PWD",
    },
    {
        "officer_name": "Block Development Officer - Ghazipur",
        "employee_code": "EMP-RD-BDO-001",
        "mobile": "9000000003",
        "email": "bdo.rd.ghazipur@example.gov.in",
        "department_code": "RD",
        "office_code": "RD-GHAZ-DIST",
        "designation_code": "BDO-RD",
    },
    {
        "officer_name": "Assistant Development Officer - Ghazipur",
        "employee_code": "EMP-RD-ADO-001",
        "mobile": "9000000004",
        "email": "ado.rd.ghazipur@example.gov.in",
        "department_code": "RD",
        "office_code": "RD-GHAZ-DIST",
        "designation_code": "ADO-RD",
    },
]


def seed_officers(db: Session):

    for item in DATA:

        department = (
            db.query(Department)
            .filter(
                Department.department_code
                == item["department_code"]
            )
            .first()
        )

        office = (
            db.query(Office)
            .filter(
                Office.office_code
                == item["office_code"]
            )
            .first()
        )

        designation = (
            db.query(Designation)
            .filter(
                Designation.designation_code
                == item["designation_code"]
            )
            .first()
        )

        if department is None:
            print(
                f"⚠️ Department not found: "
                f"{item['department_code']}"
            )
            continue

        if office is None:
            print(
                f"⚠️ Office not found: "
                f"{item['office_code']}"
            )
            continue

        if designation is None:
            print(
                f"⚠️ Designation not found: "
                f"{item['designation_code']}"
            )
            continue

        exists = (
            db.query(Officer)
            .filter(
                Officer.employee_code
                == item["employee_code"]
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ Officer already exists: "
                f"{item['employee_code']}"
            )
            continue

        officer = Officer(
            officer_name=item["officer_name"],
            employee_code=item["employee_code"],
            mobile=item["mobile"],
            email=item["email"],
            department_id=department.id,
            designation_id=designation.id,
            office_id=office.id,
            is_public=True,
            is_active=True,
        )

        db.add(officer)

        print(
            f"✓ Officer added: "
            f"{item['officer_name']}"
        )

    db.commit()
    print("✓ Officers Seeded")


def main():

    db = SessionLocal()

    try:
        seed_officers(db)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
