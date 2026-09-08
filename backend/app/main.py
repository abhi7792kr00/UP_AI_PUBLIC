from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ============================================================
# MASTER / LOCATION
# ============================================================

from app.api.v1.state import (
    router as state_router,
)

from app.api.v1.division import (
    router as division_router,
)

from app.api.v1.district import (
    router as district_router,
)

from app.api.v1.tehsil import (
    router as tehsil_router,
)

from app.api.v1.block import (
    router as block_router,
)

from app.api.v1.gram_panchayat import (
    router as gram_panchayat_router,
)

from app.api.v1.village import (
    router as village_router,
)

from app.api.v1.master.municipal_body import (
    router as municipal_body_router,
)

from app.api.v1.master.ward import (
    router as ward_router,
)

from app.api.v1.master.locality import (
    router as locality_router,
)


# ============================================================
# AUTHENTICATION / AUTHORIZATION
# ============================================================

from app.api.v1.auth.role import (
    router as role_router,
)

from app.api.v1.auth.user import (
    router as user_router,
)

from app.api.v1.login import (
    router as auth_router,
)

from app.api.v1.auth.citizen_registration import (
    router as citizen_registration_router,
)

from app.api.v1.auth.citizen_otp_registration import (
    router as citizen_otp_registration_router,
)

from app.api.v1.auth.recovery import (
    router as recovery_router,
)

from app.api.v1.protected import (
    router as protected_router,
)

from app.api.v1.admin import (
    router as admin_router,
)


# ============================================================
# CITIZEN
# ============================================================

from app.api.v1.citizen import (
    router as citizen_router,
)


# ============================================================
# GOVERNMENT / OFFICER MANAGEMENT
# ============================================================

from app.api.v1.government.department import (
    router as department_router,
)

from app.api.v1.government.designation import (
    router as designation_router,
)

from app.api.v1.government.officer import (
    router as officer_router,
)

from app.api.v1.government.office import (
    router as office_router,
)

from app.api.v1.government.posting import (
    router as posting_router,
)

from app.api.v1.government.transfer import (
    router as transfer_router,
)

from app.api.v1.government.promotion import (
    router as promotion_router,
)

from app.api.v1.government.leave import (
    router as leave_router,
)

from app.api.v1.government.suspension import (
    router as suspension_router,
)

from app.api.v1.government.retirement import (
    router as retirement_router,
)

from app.api.v1.government.training import (
    router as training_router,
)

from app.api.v1.government.dashboard import (
    router as dashboard_router,
)

from app.api.v1.government.service_history import (
    router as service_history_router,
)


# ============================================================
# COMPLAINT
# ============================================================

from app.api.v1.complaint import (
    router as complaint_router,
)


# ============================================================
# WORKFLOW
# ============================================================

from app.api.v1.workflow import (
    router as workflow_router,
)


# ============================================================
# OFFICER DASHBOARD / COMPLAINTS
# ============================================================

from app.api.v1.officer.officer_dashboard import (
    router as officer_dashboard_router,
)

from app.api.v1.officer.officer_complaints import (
    router as officer_complaints_router,
)


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="UP AI",
    version="0.5.0",
    description="Uttar Pradesh Government AI Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:5174",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# REGISTER ROUTERS
# ============================================================


# ------------------------------------------------------------
# Master / Location
# ------------------------------------------------------------

app.include_router(state_router)
app.include_router(division_router)
app.include_router(district_router)
app.include_router(tehsil_router)
app.include_router(block_router)
app.include_router(gram_panchayat_router)
app.include_router(village_router)

app.include_router(
    municipal_body_router,
)

app.include_router(
    ward_router,
)

app.include_router(
    locality_router,
)


# ------------------------------------------------------------
# Authentication / Authorization
# ------------------------------------------------------------

app.include_router(role_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(citizen_registration_router)
app.include_router(citizen_otp_registration_router)
app.include_router(recovery_router)
app.include_router(protected_router)
app.include_router(admin_router)


# ------------------------------------------------------------
# Citizen
# ------------------------------------------------------------

app.include_router(
    citizen_router,
)


# ------------------------------------------------------------
# Government
# ------------------------------------------------------------

app.include_router(department_router)
app.include_router(designation_router)
app.include_router(officer_router)
app.include_router(office_router)
app.include_router(posting_router)
app.include_router(transfer_router)
app.include_router(promotion_router)
app.include_router(leave_router)
app.include_router(suspension_router)
app.include_router(retirement_router)
app.include_router(training_router)

app.include_router(
    dashboard_router,
)

app.include_router(
    service_history_router,
)


# ------------------------------------------------------------
# Complaint
# ------------------------------------------------------------

app.include_router(
    complaint_router,
)


# ------------------------------------------------------------
# Workflow
# ------------------------------------------------------------

app.include_router(
    workflow_router,
)


# ------------------------------------------------------------
# Officer Dashboard
# ------------------------------------------------------------

app.include_router(
    officer_dashboard_router,
)

app.include_router(
    officer_complaints_router,
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to UP AI",
        "version": "0.5.0",
    }