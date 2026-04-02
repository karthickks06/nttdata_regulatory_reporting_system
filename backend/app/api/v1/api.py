"""API v1 router aggregation"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    users,
    roles,
    permissions,
    regulatory_updates,
    requirements,
    data_mappings,
    code_generation,
    development,
    reports,
    validation,
    workflow,
    agents,
    knowledge_graph,
    admin
)

api_router = APIRouter()

# Authentication
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# User Management
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["Permissions"])

# Regulatory Compliance
api_router.include_router(
    regulatory_updates.router,
    prefix="/regulatory-updates",
    tags=["Regulatory Updates"]
)
api_router.include_router(
    requirements.router,
    prefix="/requirements",
    tags=["Requirements"]
)
api_router.include_router(
    data_mappings.router,
    prefix="/data-mappings",
    tags=["Data Mappings"]
)

# Development
api_router.include_router(
    code_generation.router,
    prefix="/code-generation",
    tags=["Code Generation"]
)
api_router.include_router(
    development.router,
    prefix="/development",
    tags=["Development"]
)

# Reporting & Validation
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(validation.router, prefix="/validation", tags=["Validation"])

# Workflow
api_router.include_router(workflow.router, prefix="/workflows", tags=["Workflows"])

# AI Agents
api_router.include_router(agents.router, prefix="/agents", tags=["AI Agents"])
api_router.include_router(
    knowledge_graph.router,
    prefix="/knowledge-graph",
    tags=["Knowledge Graph"]
)

# Administration
api_router.include_router(admin.router, prefix="/admin", tags=["Administration"])
