from sqlalchemy.orm import Session

from core.database.session import SessionLocal

from database.models.complaint.complaint_category_mapping import (
    ComplaintCategoryMapping,
)

from database.models.complaint.complaint_category import (
    ComplaintCategory,
)

from database.models.master.administrative_level import (
    AdministrativeLevel,
)

from database.models.government.department import (
    Department,
)

from database.models.government.office import (
    Office,
)

from database.models.government.designation import (
    Designation,
)

from database.models.complaint.complaint_priority import (
    ComplaintPriority,
)


DATA = [
    {
        "category_code": "ELECTRICITY",
        "administrative_level_code": "DISTRICT",
        "department_code": "ELEC",
        "office_code": "ELEC-GHAZ-DIV",
        "designation_code": "JE-ELEC",
        "priority_code": "HIGH",
        "sla_days": 3,
    },
    {
        "category_code": "ROADS",
        "administrative_level_code": "DISTRICT",
        "department_code": "PWD",
        "office_code": "PWD-GHAZ-DIST",
        "designation_code": "JE-PWD",
        "priority_code": "MEDIUM",
        "sla_days": 7,
    },
    {
        "category_code": "WATER",
        "administrative_level_code": "DISTRICT",
        "department_code": "RD",
        "office_code": "RD-GHAZ-DIST",
        "designation_code": "BDO-RD",
        "priority_code": "MEDIUM",
        "sla_days": 7,
    },
    {
        "category_code": "SANITATION",
        "administrative_level_code": "DISTRICT",
        "department_code": "RD",
        "office_code": "RD-GHAZ-DIST",
        "designation_code": "ADO-RD",
        "priority_code": "LOW",
        "sla_days": 15,
    },
]


def get_by_code(db, model, field, value):

    return (
        db.query(model)
        .filter(field == value)
        .first()
    )


def seed_category_mappings(db: Session):

    for item in DATA:

        category = get_by_code(
            db,
            ComplaintCategory,
            ComplaintCategory.category_code,
            item["category_code"],
        )

        administrative_level = get_by_code(
            db,
            AdministrativeLevel,
            AdministrativeLevel.level_code,
            item["administrative_level_code"],
        )

        department = get_by_code(
            db,
            Department,
            Department.department_code,
            item["department_code"],
        )

        office = get_by_code(
            db,
            Office,
            Office.office_code,
            item["office_code"],
        )

        designation = get_by_code(
            db,
            Designation,
            Designation.designation_code,
            item["designation_code"],
        )

        priority = get_by_code(
            db,
            ComplaintPriority,
            ComplaintPriority.priority_code,
            item["priority_code"],
        )

        if category is None:
            print(
                f"⚠️ Category not found: "
                f"{item['category_code']}"
            )
            continue

        if administrative_level is None:
            print(
                f"⚠️ Administrative level not found: "
                f"{item['administrative_level_code']}"
            )
            continue

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

        if priority is None:
            print(
                f"⚠️ Priority not found: "
                f"{item['priority_code']}"
            )
            continue

        exists = (
            db.query(ComplaintCategoryMapping)
            .filter(
                ComplaintCategoryMapping.category_id
                == category.id
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ Mapping already exists: "
                f"{item['category_code']}"
            )
            continue

        mapping = ComplaintCategoryMapping(
            category_id=category.id,
            administrative_level_id=administrative_level.id,
            department_id=department.id,
            office_id=office.id,
            designation_id=designation.id,
            priority_id=priority.id,
            sla_days=item["sla_days"],
        )

        db.add(mapping)

        print(
            f"✓ Mapping added: "
            f"{item['category_code']}"
        )

    db.commit()

    print()
    print("✓ Complaint Category Mappings Seeded")


def main():

    db = SessionLocal()

    try:

        seed_category_mappings(db)

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()
