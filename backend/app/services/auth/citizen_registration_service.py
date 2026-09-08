from sqlalchemy.orm import Session

from app.repositories.auth.user_repository import user_repository
from app.repositories.citizen.citizen_repository import citizen_repository

from core.security.password import hash_password

from database.models.auth.user import User
from database.models.citizen.citizen import Citizen


CITIZEN_ROLE_ID = 9


def register_citizen(
    db: Session,
    *,
    full_name: str,
    username: str,
    email: str,
    mobile: str | None,
    password: str,
    father_name: str | None,
    mother_name: str | None,
    gender: str | None,
    dob,
    address: str,
    pincode: str | None,
    state_id: int,
    district_id: int,
    area_type: str,
    tehsil_id: int | None,
    block_id: int | None,
    gram_panchayat_id: int | None,
    village_id: int | None,
    municipal_body_id: int | None,
    ward_id: int | None,
    locality_id: int | None,
):
    area_type = area_type.strip().lower()

    if area_type not in {"rural", "urban"}:
        raise ValueError(
            "area_type must be either rural or urban."
        )

    if user_repository.get_by_username(db, username):
        raise ValueError(
            "Username already exists."
        )

    if user_repository.get_by_email(db, email):
        raise ValueError(
            "Email already exists."
        )

    if mobile and user_repository.get_by_mobile(
        db,
        mobile,
    ):
        raise ValueError(
            "Mobile already exists."
        )

    if area_type == "rural":
        municipal_body_id = None
        ward_id = None
        locality_id = None
    else:
        tehsil_id = None
        block_id = None
        gram_panchayat_id = None
        village_id = None

    user = User(
        full_name=full_name,
        username=username,
        email=email,
        password_hash=hash_password(password),
        mobile=mobile,
        role_id=CITIZEN_ROLE_ID,
        officer_id=None,
    )

    db.add(user)
    db.flush()

    citizen = Citizen(
        user_id=user.id,
        father_name=father_name,
        mother_name=mother_name,
        gender=gender,
        dob=dob,
        address=address,
        pincode=pincode,
        state_id=state_id,
        district_id=district_id,
        tehsil_id=tehsil_id,
        block_id=block_id,
        gram_panchayat_id=gram_panchayat_id,
        village_id=village_id,
        municipal_body_id=municipal_body_id,
        ward_id=ward_id,
        locality_id=locality_id,
    )

    db.add(citizen)
    db.commit()
    db.refresh(user)
    db.refresh(citizen)

    return user, citizen
