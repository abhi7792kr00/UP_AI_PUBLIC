from sqlalchemy.orm import Session

from database.models.complaint.complaint_category import (
    ComplaintCategory,
)


DATA = [
    {
        "category_name": "Electricity",
        "category_code": "ELECTRICITY",
        "description": (
            "Electricity supply and power related complaints"
        ),
        "icon": "electricity",
        "color": "#FFC107",
    },
    {
        "category_name": "Roads",
        "category_code": "ROADS",
        "description": (
            "Road and public infrastructure complaints"
        ),
        "icon": "road",
        "color": "#795548",
    },
    {
        "category_name": "Water Supply",
        "category_code": "WATER",
        "description": (
            "Water supply and drinking water complaints"
        ),
        "icon": "water",
        "color": "#2196F3",
    },
    {
        "category_name": "Sanitation",
        "category_code": "SANITATION",
        "description": (
            "Sanitation and cleanliness complaints"
        ),
        "icon": "sanitation",
        "color": "#4CAF50",
    },
]


def seed_complaint_categories(db: Session):
    for item in DATA:

        exists = (
            db.query(ComplaintCategory)
            .filter(
                ComplaintCategory.category_code
                == item["category_code"]
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ Complaint category already exists: "
                f"{item['category_name']}"
            )
            continue

        category = ComplaintCategory(
            category_name=item["category_name"],
            category_code=item["category_code"],
            description=item["description"],
            icon=item["icon"],
            color=item["color"],
        )

        db.add(category)

        print(
            f"✓ Complaint category added: "
            f"{item['category_name']}"
        )

    db.commit()

    print(
        "✓ Complaint categories seeded successfully"
    )