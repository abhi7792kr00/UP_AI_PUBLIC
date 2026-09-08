from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.government.department_schema import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
)

from app.services.government.department_service import (
    get_all_departments,
    get_department_by_id,
    create_department,
    update_department,
    delete_department,
)

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


@router.get(
    "/",
    response_model=list[DepartmentResponse],
)
def get_departments(
    db: Session = Depends(get_db),
):
    return get_all_departments(db)


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
):
    department = get_department_by_id(
        db,
        department_id,
    )

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )

    return department


@router.post(
    "/",
    response_model=DepartmentResponse,
)
def create_new_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
):
    result = create_department(
        db,
        department,
    )

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Department already exists",
        )

    return result


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse,
)
def update_existing_department(
    department_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db),
):
    result = update_department(
        db,
        department_id,
        department,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )

    return result


@router.delete(
    "/{department_id}",
)
def delete_existing_department(
    department_id: int,
    db: Session = Depends(get_db),
):
    success = delete_department(
        db,
        department_id,
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )

    return {
        "message": "Department deleted successfully"
    }