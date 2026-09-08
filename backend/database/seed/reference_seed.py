from sqlalchemy.orm import Session

from core.database.session import SessionLocal

from database.models.reference.reference_type import (
    ReferenceType,
)

from database.models.reference.reference_format import (
    ReferenceFormat,
)


def seed_reference_data(db: Session):
    print("======================================")
    print("      REFERENCE DATA SEEDING")
    print("======================================")

    # -------------------------------------------------
    # 1. Reference Type
    # -------------------------------------------------

    reference_type = (
        db.query(ReferenceType)
        .filter(
            ReferenceType.module_code == "COMPLAINT"
        )
        .first()
    )

    if reference_type is None:

        reference_type = ReferenceType(
            module_name="Complaint",
            module_code="COMPLAINT",
            description=(
                "Reference number generator "
                "for citizen complaints."
            ),
            is_active=True,
        )

        db.add(reference_type)
        db.commit()
        db.refresh(reference_type)

        print("✓ Complaint Reference Type Seeded")

    else:

        print("⚠ Complaint Reference Type Already Exists")

    # -------------------------------------------------
    # 2. Reference Format
    # -------------------------------------------------

    reference_format = (
        db.query(ReferenceFormat)
        .filter(
            ReferenceFormat.reference_type_id
            == reference_type.id
        )
        .first()
    )

    if reference_format is None:

        reference_format = ReferenceFormat(
            reference_type_id=reference_type.id,
            format_name="Complaint Reference",
            prefix="UPAI",
            separator="-",
            sequence_length=6,
            is_active=True,
            description=(
                "Standard complaint reference format."
            ),
        )

        db.add(reference_format)
        db.commit()

        print("✓ Complaint Reference Format Seeded")

    else:

        print("⚠ Complaint Reference Format Already Exists")


def main():

    db: Session = SessionLocal()

    try:

        seed_reference_data(db)

        print()
        print("======================================")
        print("       ✓ REFERENCE DATA READY")
        print("======================================")

    except Exception as exc:

        db.rollback()

        print()
        print("❌ Reference seed failed:")
        print(exc)

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()
