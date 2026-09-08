from sqlalchemy.orm import Session

from database.models.citizen.citizen import Citizen
from database.models.complaint.complaint import Complaint

from app.repositories.complaint.complaint_repository import (
    complaint_repository,
)

from app.bootstrap.complaint import (
    complaint_registration_engine,
)

from app.dto.complaint.complaint_request import (
    ComplaintRequest,
)

class CitizenComplaintService:

    def get_my_complaints(
        self,
        db: Session,
        user_id: int,
    ) -> list[Complaint]:

        citizen = (
            db.query(Citizen)
            .filter(
                Citizen.user_id == user_id,
                Citizen.is_active == True,
            )
            .first()
        )

        if citizen is None:
            raise ValueError(
                "Citizen profile not found."
            )

        return complaint_repository.get_by_citizen(
            db,
            citizen.id,
        )

    def get_my_complaint(
        self,
        db: Session,
        user_id: int,
        complaint_number: str,
    ) -> Complaint:

        citizen = (
            db.query(Citizen)
            .filter(
                Citizen.user_id == user_id,
                Citizen.is_active == True,
            )
            .first()
        )

        if citizen is None:
            raise ValueError(
                "Citizen profile not found."
            )

        complaint = (
            complaint_repository.get_by_complaint_number(
                db,
                complaint_number,
            )
        )

        if complaint is None:
            raise ValueError(
                "Complaint not found."
            )

        if complaint.citizen_id != citizen.id:
            raise ValueError(
                "You are not authorized to access this complaint."
            )

        return complaint

    def create_complaint(
        self,
        db: Session,
        user_id: int,
        request,
    ):

        citizen = (
            db.query(Citizen)
            .filter(
                Citizen.user_id == user_id,
                Citizen.is_active == True,
            )
            .first()
        )

        if citizen is None:
            raise ValueError(
                "Citizen profile not found."
            )

        complaint_request = ComplaintRequest(
            citizen_id=citizen.id,

            category_id=request.category_id,
            subcategory_id=request.subcategory_id,

            subject=request.subject,
            description=request.description,

            priority_id=request.priority_id,

            state_id=request.state_id,
            division_id=request.division_id,
            district_id=request.district_id,

            tehsil_id=request.tehsil_id,
            block_id=request.block_id,
            gram_panchayat_id=request.gram_panchayat_id,
            village_id=request.village_id,

            municipal_body_id=request.municipal_body_id,
            ward_id=request.ward_id,
            locality_id=request.locality_id,

            address=request.address,

            latitude=request.latitude,
            longitude=request.longitude,

            pincode=request.pincode,

            mobile_number=request.mobile_number,
            email=request.email,

            has_attachment=request.has_attachment,

            source=request.source,
            language=request.language,

            visibility=request.visibility,
        )

        return complaint_registration_engine.register_complaint(
            db=db,
            request=complaint_request,
        )
citizen_complaint_service = CitizenComplaintService()
