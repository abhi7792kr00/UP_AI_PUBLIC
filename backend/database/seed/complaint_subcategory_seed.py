from sqlalchemy.orm import Session

from database.models.complaint.complaint_category import (
    ComplaintCategory,
)

from database.models.complaint.complaint_subcategory import (
    ComplaintSubCategory,
)


DATA = [
    {
        "category_code": "ELECTRICITY",
        "subcategory_name": "Power Outage",
        "subcategory_code": "ELECTRICITY_OUTAGE",
        "description": "Electricity supply interruption complaint",
    },
    {
        "category_code": "ELECTRICITY",
        "subcategory_name": "Transformer Problem",
        "subcategory_code": "ELECTRICITY_TRANSFORMER",
        "description": "Transformer related complaint",
    },
    {
        "category_code": "ELECTRICITY",
        "subcategory_name": "Electric Pole Problem",
        "subcategory_code": "ELECTRICITY_POLE",
        "description": "Electric pole related complaint",
    },
    {
        "category_code": "ELECTRICITY",
        "subcategory_name": "Street Light",
        "subcategory_code": "ELECTRICITY_STREET_LIGHT",
        "description": "Street light related complaint",
    },
    {
        "category_code": "ROADS",
        "subcategory_name": "Road Damage",
        "subcategory_code": "ROADS_DAMAGE",
        "description": "Damaged road complaint",
    },
    {
        "category_code": "ROADS",
        "subcategory_name": "Pothole",
        "subcategory_code": "ROADS_POTHOLE",
        "description": "Pothole related complaint",
    },
    {
        "category_code": "WATER",
        "subcategory_name": "Water Supply",
        "subcategory_code": "WATER_SUPPLY",
        "description": "Water supply related complaint",
    },
    {
        "category_code": "WATER",
        "subcategory_name": "Water Pipeline Leakage",
        "subcategory_code": "WATER_PIPELINE_LEAK",
        "description": "Water pipeline leakage complaint",
    },
    {
        "category_code": "SANITATION",
        "subcategory_name": "Garbage Collection",
        "subcategory_code": "SANITATION_GARBAGE",
        "description": "Garbage collection complaint",
    },
    {
        "category_code": "SANITATION",
        "subcategory_name": "Drainage Problem",
        "subcategory_code": "SANITATION_DRAINAGE",
        "description": "Drainage related complaint",
    },
]


def seed_complaint_subcategories(db: Session):
    for item in DATA:

        category = (
            db.query(ComplaintCategory)
            .filter(
                ComplaintCategory.category_code
                == item["category_code"]
            )
            .first()
        )

        if category is None:
            raise RuntimeError(
                "Complaint category not found: "
                f"{item['category_code']}"
            )

        exists = (
            db.query(ComplaintSubCategory)
            .filter(
                ComplaintSubCategory.subcategory_code
                == item["subcategory_code"]
            )
            .first()
        )

        if exists:
            print(
                "⚠️ Complaint subcategory already exists: "
                f"{item['subcategory_name']}"
            )
            continue

        subcategory = ComplaintSubCategory(
            category_id=category.id,
            subcategory_name=item["subcategory_name"],
            subcategory_code=item["subcategory_code"],
            description=item["description"],
        )

        db.add(subcategory)

        print(
            "✓ Complaint subcategory added: "
            f"{item['subcategory_name']}"
        )

    db.commit()

    print(
        "✓ Complaint subcategories seeded successfully"
    )
