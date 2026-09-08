from core.database.session import SessionLocal

from database.seed.administrative_level_seed import (
    seed_administrative_levels,
)

from database.seed.state_seed import (
    seed_states,
)

from database.seed.division_seed import (
    seed_divisions,
)

from database.seed.district_seed import (
    seed_districts,
)

from database.seed.tehsil_seed import (
    seed_tehsils,
)

from database.seed.block_seed import (
    seed_blocks,
)

from database.seed.gram_panchayat_seed import (
    seed_gram_panchayats,
)

from database.seed.village_seed import (
    seed_villages,
)

from database.seed.department_seed import (
    seed_departments,
)

from database.seed.complaint_category_seed import (
    seed_complaint_categories,
)

from database.seed.complaint_priority_seed import (
    seed_complaint_priorities,
)

from database.seed.complaint_status_seed import (
    seed_complaint_statuses,
)

from database.seed.complaint_subcategory_seed import (
    seed_complaint_subcategories,
)

def seed_all():
    db = SessionLocal()

    try:
        print()
        print("======================================")
        print("        UP AI MASTER DATA SEED")
        print("======================================")
        print()

        print("[1/13] Administrative Levels")
        seed_administrative_levels(db)

        print("[2/13] States")
        seed_states(db)

        print("[3/13] Divisions")
        seed_divisions(db)

        print("[4/13] Districts")
        seed_districts(db)

        print("[5/13] Tehsils")
        seed_tehsils(db)

        print("[6/13] Blocks")
        seed_blocks(db)

        print("[7/13] Gram Panchayats")
        seed_gram_panchayats(db)

        print("[8/13] Villages")
        seed_villages(db)

        print("[9/13] Departments")
        seed_departments(db)

        print("[10/13] Complaint Categories")
        seed_complaint_categories(db)

        print("[11/13] Complaint Subcategories")
        seed_complaint_subcategories(db)

        print("[1/13] Complaint Priorities")
        seed_complaint_priorities(db)

        print("[13/13] Complaint Statuses")
        seed_complaint_statuses(db)

        print()
        print("======================================")
        print("       ✓ MASTER DATA SEEDED")
        print("======================================")
        print()

    except Exception:
        db.rollback()

        print()
        print("❌ MASTER DATA SEED FAILED")
        print()

        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_all()