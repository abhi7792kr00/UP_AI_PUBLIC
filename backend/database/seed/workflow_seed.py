from sqlalchemy.orm import Session

from core.database.session import SessionLocal

from database.models.workflow.workflow_definition import (
    WorkflowDefinition,
)

from database.models.workflow.workflow_step import (
    WorkflowStep,
)


def seed_workflow(db: Session):

    # ---------------------------------
    # Workflow Definition
    # ---------------------------------

    workflow = (
        db.query(WorkflowDefinition)
        .filter(
            WorkflowDefinition.workflow_code
            == "COMPLAINT_DEFAULT"
        )
        .first()
    )

    if workflow is None:

        workflow = WorkflowDefinition(
            workflow_name="Complaint Workflow",
            workflow_code="COMPLAINT_DEFAULT",
            module_name="COMPLAINT",
            description=(
                "Default workflow for complaint "
                "registration and resolution."
            ),
            version=1,
            is_default=True,
            is_active=True,
        )

        db.add(workflow)
        db.flush()

        print("✓ Complaint Workflow Created")

    else:

        print("⚠️ Complaint Workflow Already Exists")

    # ---------------------------------
    # Workflow Steps
    # ---------------------------------

    steps = [
        {
            "step_name": "Pending",
            "step_code": "PENDING",
            "step_order": 1,
            "description": "Complaint registered and pending processing.",
            "is_initial": True,
            "is_final": False,
            "requires_assignment": False,
            "allows_rejection": False,
        },
        {
            "step_name": "Assigned",
            "step_code": "ASSIGNED",
            "step_order": 2,
            "description": "Complaint assigned to responsible officer.",
            "is_initial": False,
            "is_final": False,
            "requires_assignment": True,
            "allows_rejection": False,
        },
        {
            "step_name": "In Progress",
            "step_code": "IN_PROGRESS",
            "step_order": 3,
            "description": "Complaint is being processed.",
            "is_initial": False,
            "is_final": False,
            "requires_assignment": True,
            "allows_rejection": False,
        },
        {
            "step_name": "Resolved",
            "step_code": "RESOLVED",
            "step_order": 4,
            "description": "Complaint has been resolved.",
            "is_initial": False,
            "is_final": False,
            "requires_assignment": True,
            "allows_rejection": False,
        },
        {
            "step_name": "Closed",
            "step_code": "CLOSED",
            "step_order": 5,
            "description": "Complaint lifecycle completed.",
            "is_initial": False,
            "is_final": True,
            "requires_assignment": False,
            "allows_rejection": False,
        },
        {
            "step_name": "Rejected",
            "step_code": "REJECTED",
            "step_order": 6,
            "description": "Complaint rejected after review.",
            "is_initial": False,
            "is_final": True,
            "requires_assignment": False,
            "allows_rejection": True,
        },
        {
            "step_name": "Escalated",
            "step_code": "ESCALATED",
            "step_order": 7,
            "description": "Complaint escalated to higher authority.",
            "is_initial": False,
            "is_final": False,
            "requires_assignment": True,
            "allows_rejection": False,
        },
        {
            "step_name": "Reopened",
            "step_code": "REOPENED",
            "step_order": 8,
            "description": "Previously resolved complaint reopened.",
            "is_initial": False,
            "is_final": False,
            "requires_assignment": True,
            "allows_rejection": False,
        },
    ]

    for item in steps:

        exists = (
            db.query(WorkflowStep)
            .filter(
                WorkflowStep.workflow_definition_id
                == workflow.id,
                WorkflowStep.step_code
                == item["step_code"],
            )
            .first()
        )

        if exists:
            print(
                f"⚠️ Step already exists: "
                f"{item['step_code']}"
            )
            continue

        step = WorkflowStep(
            workflow_definition_id=workflow.id,
            step_name=item["step_name"],
            step_code=item["step_code"],
            step_order=item["step_order"],
            description=item["description"],
            is_initial=item["is_initial"],
            is_final=item["is_final"],
            requires_assignment=item["requires_assignment"],
            allows_rejection=item["allows_rejection"],
        )

        db.add(step)

        print(
            f"✓ Workflow Step Added: "
            f"{item['step_code']}"
        )

    db.commit()

    print()
    print("======================================")
    print("       ✓ COMPLAINT WORKFLOW READY")
    print("======================================")


def main():

    db = SessionLocal()

    try:

        seed_workflow(db)

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()
