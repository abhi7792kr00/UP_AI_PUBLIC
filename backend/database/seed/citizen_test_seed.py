from datetime import date

from sqlalchemy.orm import Session

from core.database.session import SessionLocal

from database.models.auth.role import Role
from database.models.auth.user import User
from database.models.citizen.citizen import Citizen


def seed_test_citizen(db: Session):

    # ---------------------------------
    # Find Citizen Role
    # ---------------------------------

    role = (
        db.query(Role)
        .filter(
            Role.role_name == "Citizen"
        )
        .first()
    )

    if role is None:
        raise ValueError(
            "Citizen role not found. "
            "Run the role seed first."
        )

    # ---------------------------------
    # Find Existing Test User
    # ---------------------------------

    user = (
        db.query(User)
        .filter(
            User.username == "test.citizen"
        )
        .first()
    )

    if user is None:

        user = User(
            full_name="Test Citizen",
            username="test.citizen",
            email="test.citizen@upai.local",
            password_hash="TEST_ONLY_PASSWORD_HASH",
            mobile="9876543210",
            role_id=role.id,
            is_active=True,
        )

        db.add(user)
        db.flush()

        print("✓ Test User Created")

    else:

        print("⚠️ Test User Already Exists")

    # ---------------------------------
    # Find Existing Citizen
    # ---------------------------------

    citizen = (
        db.query(Citizen)
        .filter(
            Citizen.user_id == user.id
        )
        .first()
    )

    if citizen is None:

        citizen = Citizen(
            user_id=user.id,

            father_name="Test Father",
            mother_name="Test Mother",

            gender="Male",
            dob=date(2000, 1, 1),

            address=(
                "Test Address, "
                "Ghazipur, Uttar Pradesh"
            ),

            pincode="233001",

            # Existing seeded location
            state_id=1,
            district_id=1,

            tehsil_id=1,
            block_id=1,
            gram_panchayat_id=1,
            village_id=1,
        )

        db.add(citizen)

        print("✓ Test Citizen Created")

    else:

        print("⚠️ Test Citizen Already Exists")

    db.commit()

    print()
    print("======================================")
    print("       ✓ TEST CITIZEN READY")
    print("======================================")


def main():

    db: Session = SessionLocal()

    try:

        seed_test_citizen(db)

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()
