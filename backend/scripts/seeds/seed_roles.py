from sqlalchemy.orm import Session

from core.database.session import SessionLocal
from database.models.auth.role import Role


DEFAULT_ROLES = [
    {
        "role_name": "Super Admin",
        "description": "Full system access"
    },
    {
        "role_name": "State Admin",
        "description": "State level administrator"
    },
    {
        "role_name": "Division Admin",
        "description": "Division level administrator"
    },
    {
        "role_name": "District Admin",
        "description": "District level administrator"
    },
    {
        "role_name": "Tehsil Admin",
        "description": "Tehsil level administrator"
    },
    {
        "role_name": "Block Admin",
        "description": "Block level administrator"
    },
    {
        "role_name": "Gram Panchayat Admin",
        "description": "Gram Panchayat administrator"
    },
    {
        "role_name": "Department Officer",
        "description": "Government Officer"
    },
    {
        "role_name": "Citizen",
        "description": "General Citizen"
    }
]


def seed_roles():
    db: Session = SessionLocal()

    try:
        for item in DEFAULT_ROLES:

            role = db.query(Role).filter(
                Role.role_name == item["role_name"]
            ).first()

            if not role:
                db.add(
                    Role(
                        role_name=item["role_name"],
                        description=item["description"]
                    )
                )

        db.commit()

        print("✅ Default Roles Seeded Successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_roles()