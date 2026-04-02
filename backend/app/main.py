"""Main FastAPI application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Create FastAPI application
app = FastAPI(
    title="NTT Data Regulatory Reporting System",
    description="""
## AI-Powered Regulatory Compliance Automation Platform

### Features
- **Authentication & Authorization**: JWT-based authentication with RBAC
- **User Management**: Admin-managed user accounts (no public registration)
- **Regulatory Updates**: Automated processing of FCA, PRA, BOE regulations
- **Requirements Extraction**: AI-powered requirement analysis
- **Code Generation**: Automated SQL and Python code generation
- **Workflow Management**: Multi-step compliance workflow orchestration
- **AI Agents**: 14 specialized agents (7 hierarchical + 7 sub-agents)
- **Knowledge Graph**: GraphRAG with ChromaDB vector storage
- **Reporting**: Automated regulatory report generation and validation

### Admin User Setup
**IMPORTANT**: The first admin user must be created via API:
1. Use `POST /api/v1/admin/setup/create-admin` endpoint
2. Provide username, email, and password
3. This creates the initial superuser account
4. All other users are created by the admin via `POST /api/v1/users/`

### Authentication
All endpoints (except `/auth/login` and `/admin/setup/create-admin`) require JWT authentication:
1. Login via `POST /api/v1/auth/login`
2. Use returned token in Authorization header: `Bearer <token>`
3. Token expires in 30 minutes (configurable)

### API Organization
Endpoints are grouped by functionality:
- **🔐 Authentication**: Login, logout, current user info
- **👥 Users**: User CRUD (admin only)
- **🎭 Roles & Permissions**: RBAC management
- **📋 Regulatory Updates**: Document upload and processing
- **📝 Requirements**: Requirement extraction and gap analysis
- **🗺️ Data Mappings**: Source-to-target data mappings
- **💻 Code Generation**: SQL and Python code generation
- **🔧 Development**: Code management and data lineage
- **📊 Reports**: Report generation and submission
- **✅ Validation**: Data and report validation
- **🔄 Workflows**: Multi-step workflow execution
- **🤖 AI Agents**: Agent execution and monitoring
- **🕸️ Knowledge Graph**: GraphRAG and semantic search
- **⚙️ Administration**: System monitoring and management

### Version
1.0.0
    """,
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    contact={
        "name": "NTT Data",
        "url": "https://nttdata.com",
    },
    license_info={
        "name": "Proprietary",
    },
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "NTT Data Regulatory Reporting System API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/v1/docs"
    }


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
    }


# Import and include API routers
from app.api.v1.api import api_router
app.include_router(api_router, prefix="/api/v1")
