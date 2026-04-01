"""API v1 router aggregation"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Additional routers will be added here as they are implemented
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(regulatory_updates.router, prefix="/regulatory-updates", tags=["Regulatory Updates"])
# api_router.include_router(requirements.router, prefix="/requirements", tags=["Requirements"])
# etc.
