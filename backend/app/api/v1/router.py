from fastapi import APIRouter

# ----------------------------
# Authentication
# ----------------------------

from app.api.v1.auth import (
    router as auth_router,
)

# ----------------------------
# Government
# ----------------------------

from app.api.v1.government import (
    router as government_router,
)

# ----------------------------
# Citizen
# ----------------------------

from app.api.v1.citizen import (
    router as citizen_router,
)

# ----------------------------
# Complaint
# ----------------------------

from app.api.v1.complaint import (
    router as complaint_router,
)

from app.api.v1.login import router as login_router
from app.api.v1.auth.citizen_registration import (
    router as citizen_registration_router,
)
from app.api.v1.protected import router as protected_router
from app.api.v1.admin import router as admin_router
# ----------------------------
# Master APIs
# ----------------------------

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

# ----------------------------
# Workflow
# ----------------------------

from app.api.v1.workflow import (
    router as workflow_router,
)
api_router = APIRouter()

# ----------------------------
# Master
# ----------------------------

api_router.include_router(state_router)
api_router.include_router(division_router)
api_router.include_router(district_router)
api_router.include_router(tehsil_router)
api_router.include_router(block_router)
api_router.include_router(gram_panchayat_router)
api_router.include_router(village_router)

# ----------------------------
# Auth
# ----------------------------

api_router.include_router(auth_router)

# ----------------------------
# Citizen
# ----------------------------

api_router.include_router(citizen_router)

# ----------------------------
# Government
# ----------------------------

api_router.include_router(government_router)

# ----------------------------
# Complaint
# ----------------------------

api_router.include_router(complaint_router)

api_router.include_router(login_router)
api_router.include_router(citizen_registration_router)
api_router.include_router(protected_router)
api_router.include_router(admin_router)

# ----------------------------
# Workflow
# ----------------------------

api_router.include_router(workflow_router)