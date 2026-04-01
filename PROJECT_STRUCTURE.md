# Project Structure - NTT Data Regulatory Reporting System

## 🎯 Overview

AI-Agentic Regulatory Reporting Platform with:
- **7 Hierarchical AI Agents** (1 Compliance + 3 Supervisors + 3 Workers)
- **2 Databases Only** (PostgreSQL + ChromaDB)
- **Local Filesystem Storage** (GraphRAG, embeddings, workflows)
- **Single Command Deployment** (`python app.py`)

---

## 📁 Complete Directory Structure

```
nttdata_regulatory_reporting_system/
│
├── frontend/                           # React Frontend Application
│   ├── public/
│   │   ├── index.html
│   │   └── assets/
│   │
│   ├── src/
│   │   ├── app/                       # App configuration
│   │   │   ├── App.tsx
│   │   │   ├── store.ts              # Redux store
│   │   │   └── router.tsx            # React Router config
│   │   │
│   │   ├── features/                  # Feature-based modules
│   │   │   ├── auth/
│   │   │   │   ├── components/
│   │   │   │   │   ├── LoginForm.tsx
│   │   │   │   │   ├── RegisterForm.tsx
│   │   │   │   │   └── ProfilePage.tsx
│   │   │   │   ├── hooks/
│   │   │   │   │   ├── useAuth.ts
│   │   │   │   │   └── usePermissions.ts
│   │   │   │   ├── slices/
│   │   │   │   │   └── authSlice.ts
│   │   │   │   ├── services/
│   │   │   │   │   └── authApi.ts
│   │   │   │   └── types/
│   │   │   │       └── auth.types.ts
│   │   │   │
│   │   │   ├── regulatory-updates/
│   │   │   │   ├── components/
│   │   │   │   │   ├── DocumentUpload.tsx
│   │   │   │   │   ├── DocumentViewer.tsx
│   │   │   │   │   ├── DocumentList.tsx
│   │   │   │   │   └── ProcessingStatus.tsx
│   │   │   │   ├── services/
│   │   │   │   │   └── documentsApi.ts
│   │   │   │   └── types/
│   │   │   │
│   │   │   ├── requirements/          # Business Analyst Features
│   │   │   │   ├── components/
│   │   │   │   │   ├── RequirementsList.tsx
│   │   │   │   │   ├── RequirementEditor.tsx
│   │   │   │   │   ├── GapAnalysis.tsx
│   │   │   │   │   ├── DataMapping.tsx
│   │   │   │   │   ├── ImpactMatrix.tsx
│   │   │   │   │   └── ApprovalWorkflow.tsx
│   │   │   │   ├── services/
│   │   │   │   │   └── requirementsApi.ts
│   │   │   │   └── types/
│   │   │   │
│   │   │   ├── development/           # Developer Features
│   │   │   │   ├── components/
│   │   │   │   │   ├── CodePreview.tsx
│   │   │   │   │   ├── SQLEditor.tsx
│   │   │   │   │   ├── PythonEditor.tsx
│   │   │   │   │   ├── LineageViewer.tsx
│   │   │   │   │   ├── TestCaseManager.tsx
│   │   │   │   │   ├── PipelineMonitor.tsx
│   │   │   │   │   └── SchemaViewer.tsx
│   │   │   │   ├── services/
│   │   │   │   │   └── developmentApi.ts
│   │   │   │   └── types/
│   │   │   │
│   │   │   ├── reporting/             # Analyst Features
│   │   │   │   ├── components/
│   │   │   │   │   ├── ReportGenerator.tsx
│   │   │   │   │   ├── ReportViewer.tsx
│   │   │   │   │   ├── ValidationDashboard.tsx
│   │   │   │   │   ├── AnomalyDetection.tsx
│   │   │   │   │   ├── VarianceExplainer.tsx
│   │   │   │   │   ├── AuditPackBuilder.tsx
│   │   │   │   │   └── SubmissionPortal.tsx
│   │   │   │   ├── services/
│   │   │   │   │   └── reportingApi.ts
│   │   │   │   └── types/
│   │   │   │
│   │   │   ├── workflow/              # Workflow monitoring
│   │   │   │   ├── components/
│   │   │   │   │   ├── WorkflowDesigner.tsx
│   │   │   │   │   ├── ApprovalQueue.tsx
│   │   │   │   │   ├── ProcessStatus.tsx
│   │   │   │   │   └── WorkflowHistory.tsx
│   │   │   │   └── services/
│   │   │   │
│   │   │   ├── admin/
│   │   │   │   ├── components/
│   │   │   │   │   ├── UserManagement.tsx
│   │   │   │   │   ├── RolePermissions.tsx
│   │   │   │   │   ├── SystemMonitoring.tsx
│   │   │   │   │   ├── AuditLogs.tsx
│   │   │   │   │   └── AgentConfiguration.tsx
│   │   │   │   └── services/
│   │   │   │
│   │   │   └── agents/                # Agent Monitoring Dashboard
│   │   │       ├── components/
│   │   │       │   ├── AgentDashboard.tsx
│   │   │       │   ├── ComplianceAgentView.tsx
│   │   │       │   ├── SupervisorAgentView.tsx
│   │   │       │   ├── WorkerAgentView.tsx
│   │   │       │   ├── AgentExecutionLog.tsx
│   │   │       │   └── AgentProgress.tsx
│   │   │       └── services/
│   │   │
│   │   ├── components/                # shadcn/ui components
│   │   │   ├── ui/                    # shadcn/ui component library
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── label.tsx
│   │   │   │   ├── select.tsx
│   │   │   │   ├── table.tsx
│   │   │   │   ├── tabs.tsx
│   │   │   │   ├── form.tsx
│   │   │   │   ├── toast.tsx
│   │   │   │   ├── dropdown-menu.tsx
│   │   │   │   ├── badge.tsx
│   │   │   │   ├── alert.tsx
│   │   │   │   ├── sheet.tsx
│   │   │   │   ├── separator.tsx
│   │   │   │   ├── scroll-area.tsx
│   │   │   │   └── skeleton.tsx
│   │   │   └── layout/
│   │   │       ├── Header.tsx
│   │   │       ├── Sidebar.tsx
│   │   │       └── Footer.tsx
│   │   │
│   │   ├── shared/                    # Shared resources
│   │   │   ├── components/
│   │   │   │   ├── ProtectedRoute.tsx
│   │   │   │   ├── PermissionGuard.tsx
│   │   │   │   └── ErrorBoundary.tsx
│   │   │   ├── hooks/
│   │   │   │   ├── useDebounce.ts
│   │   │   │   ├── useLocalStorage.ts
│   │   │   │   └── useWebSocket.ts
│   │   │   ├── utils/
│   │   │   │   ├── api.ts
│   │   │   │   ├── format.ts
│   │   │   │   └── validation.ts
│   │   │   ├── types/
│   │   │   │   ├── common.types.ts
│   │   │   │   └── api.types.ts
│   │   │   └── constants/
│   │   │       ├── routes.ts
│   │   │       ├── permissions.ts
│   │   │       └── config.ts
│   │   │
│   │   ├── lib/                       # Utility libraries
│   │   │   └── utils.ts              # cn() helper for Tailwind
│   │   │
│   │   ├── assets/                    # Static assets
│   │   │   ├── images/
│   │   │   ├── icons/
│   │   │   └── styles/
│   │   │
│   │   ├── styles/                    # Global styles
│   │   │   └── globals.css           # Tailwind directives + custom styles
│   │   │
│   │   ├── main.tsx                   # Entry point
│   │   └── vite-env.d.ts
│   │
│   ├── components.json                # shadcn/ui configuration
│   ├── tailwind.config.js             # Tailwind CSS configuration
│   ├── postcss.config.js              # PostCSS configuration
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── .env.example
│
├── backend/                            # FastAPI Backend Application
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── users.py
│   │   │   │   │   ├── roles.py
│   │   │   │   │   ├── permissions.py
│   │   │   │   │   ├── regulatory_updates.py
│   │   │   │   │   ├── requirements.py
│   │   │   │   │   ├── data_mappings.py
│   │   │   │   │   ├── development.py
│   │   │   │   │   ├── code_generation.py
│   │   │   │   │   ├── reports.py
│   │   │   │   │   ├── validation.py
│   │   │   │   │   ├── workflow.py
│   │   │   │   │   ├── agents.py
│   │   │   │   │   ├── knowledge_graph.py
│   │   │   │   │   └── admin.py
│   │   │   │   ├── api.py            # Router aggregation
│   │   │   │   └── websocket.py      # WebSocket endpoints
│   │   │   └── deps.py               # Dependencies
│   │   │
│   │   ├── core/
│   │   │   ├── config.py             # Settings
│   │   │   ├── security.py           # Auth & security
│   │   │   ├── rbac.py               # RBAC implementation
│   │   │   ├── logging.py            # Structured logging
│   │   │   └── exceptions.py         # Custom exceptions
│   │   │
│   │   ├── models/                   # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── role.py
│   │   │   ├── permission.py
│   │   │   ├── session.py            # JWT sessions
│   │   │   ├── cache.py              # Application cache
│   │   │   ├── rate_limit.py         # Rate limiting
│   │   │   ├── task_queue.py         # Background tasks
│   │   │   ├── regulatory_update.py
│   │   │   ├── requirement.py
│   │   │   ├── data_mapping.py
│   │   │   ├── generated_code.py
│   │   │   ├── test_case.py
│   │   │   ├── report.py
│   │   │   ├── workflow.py
│   │   │   ├── file_metadata.py      # Storage file tracking
│   │   │   └── audit_log.py
│   │   │
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── auth.py
│   │   │   ├── role.py
│   │   │   ├── permission.py
│   │   │   ├── regulatory_update.py
│   │   │   ├── requirement.py
│   │   │   ├── data_mapping.py
│   │   │   ├── code.py
│   │   │   ├── report.py
│   │   │   ├── workflow.py
│   │   │   └── agent.py
│   │   │
│   │   ├── services/                 # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── rbac_service.py
│   │   │   ├── regulatory_service.py
│   │   │   ├── requirement_service.py
│   │   │   ├── code_generation_service.py
│   │   │   ├── report_service.py
│   │   │   ├── validation_service.py
│   │   │   ├── workflow_service.py
│   │   │   ├── audit_service.py
│   │   │   ├── graphrag_storage.py       # GraphRAG persistence
│   │   │   ├── embedding_storage.py      # Embeddings & tiktoken
│   │   │   ├── workflow_storage.py       # Workflow tracking
│   │   │   └── notification_service.py
│   │   │
│   │   ├── agents/                   # MCP Agents (Hierarchical)
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py
│   │   │   │
│   │   │   ├── level_0/              # Master Orchestrator
│   │   │   │   └── compliance_agent.py      # Top-level compliance orchestrator
│   │   │   │
│   │   │   ├── level_1/              # Supervisor Agents
│   │   │   │   ├── ba_supervisor_agent.py   # BA team supervisor
│   │   │   │   ├── dev_supervisor_agent.py  # Dev team supervisor
│   │   │   │   └── qa_supervisor_agent.py   # QA team supervisor
│   │   │   │
│   │   │   ├── level_2/              # Worker Agents
│   │   │   │   ├── interpreter_agent.py     # BA worker
│   │   │   │   ├── architect_agent.py       # Developer worker
│   │   │   │   └── auditor_agent.py         # QA worker
│   │   │   │
│   │   │   └── config/
│   │   │       ├── prompts.py        # Agent prompts (all levels)
│   │   │       └── settings.py       # Agent settings
│   │   │
│   │   ├── sub_agents/               # Specialized sub-agents
│   │   │   ├── __init__.py
│   │   │   ├── document_parser.py
│   │   │   ├── chromadb_graph_rag_agent.py  # ChromaDB unified agent
│   │   │   ├── networkx_analyzer.py         # NetworkX graph analysis
│   │   │   ├── code_generator.py
│   │   │   ├── sql_generator.py
│   │   │   ├── test_generator.py
│   │   │   └── validator.py
│   │   │
│   │   ├── tools/                    # Agent tools
│   │   │   ├── __init__.py
│   │   │   ├── pdf_parser.py
│   │   │   ├── xml_parser.py
│   │   │   ├── sql_generator.py
│   │   │   ├── python_generator.py
│   │   │   ├── chromadb_query.py
│   │   │   ├── vector_search.py
│   │   │   └── data_lineage.py
│   │   │
│   │   ├── db/                       # Database connections
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── postgres.py           # PostgreSQL connection
│   │   │   └── chroma_db.py          # ChromaDB connection
│   │   │
│   │   ├── tasks/                    # Background tasks
│   │   │   ├── __init__.py
│   │   │   ├── cleanup_tasks.py      # DB cleanup scheduler
│   │   │   ├── document_processing.py
│   │   │   ├── agent_execution.py    # Task queue worker
│   │   │   ├── report_generation.py
│   │   │   └── notification.py
│   │   │
│   │   ├── utils/                    # Utilities
│   │   │   ├── __init__.py
│   │   │   ├── file_handler.py
│   │   │   ├── email.py
│   │   │   └── helpers.py
│   │   │
│   │   └── main.py                   # FastAPI app (imported by app.py)
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   │
│   ├── migrations/                   # Manual SQL migrations (no Alembic!)
│   │   ├── 001_initial_schema.sql    # Auto-generated reference
│   │   ├── 002_add_workflow_priority.sql  # Example migration
│   │   └── README.md                 # Migration tracking
│   │
│   ├── scripts/                      # Utility scripts
│   │   ├── init_db.py                # (called automatically by app.py)
│   │   ├── seed_data.py              # (called automatically by app.py)
│   │   ├── setup_storage.py          # (called automatically by app.py)
│   │   ├── create_admin.py
│   │   └── generate_schema_sql.py    # Generate initial schema SQL
│   │
│   ├── app.py                        # ⭐ MAIN ENTRY POINT - Run this!
│   ├── requirements.txt              # All dependencies (prod + dev)
│   ├── pyproject.toml
│   └── .env.example
│
├── storage/                            # Local Filesystem Storage
│   ├── documents/                      # Raw regulatory documents
│   │   ├── fca/
│   │   ├── pra/
│   │   └── boe/
│   │
│   ├── reports/                        # Generated reports
│   │   ├── submissions/
│   │   └── validation/
│   │
│   ├── audit_logs/                     # Daily audit log files
│   │   └── 2026/
│   │       ├── 01/
│   │       └── 02/
│   │
│   ├── generated_code/                 # Agent-generated code
│   │   ├── sql/
│   │   └── python/
│   │
│   ├── graphrag/                       # Microsoft GraphRAG outputs
│   │   ├── graphs/                     # NetworkX graphs (.gpickle, .json, .gexf)
│   │   ├── communities/                # Community detection results
│   │   ├── entities/                   # Extracted entities
│   │   └── analysis/                   # Centrality, paths, subgraphs
│   │
│   ├── embeddings/                     # Tiktoken & vector embeddings
│   │   ├── vectors/                    # Pre-computed embeddings (.npy)
│   │   ├── tiktoken_cache/             # Tokenization cache
│   │   └── indexes/                    # FAISS/HNSW indexes (backup)
│   │
│   ├── workflows/                      # Workflow execution data
│   │   ├── definitions/                # Workflow templates
│   │   ├── executions/                 # Workflow runs by month
│   │   ├── state/                      # Active workflow states
│   │   └── history/                    # Completed/failed workflows
│   │
│   ├── backups/                        # Automated backups
│   │   ├── daily/
│   │   ├── weekly/
│   │   └── monthly/
│   │
│   └── temp/                          # Temporary processing files
│       ├── uploads/
│       └── processing/
│
├── chroma_db/                         # ChromaDB persistent storage
│   └── (auto-generated by ChromaDB)
│
├── scripts/                           # Project scripts
│   ├── setup.sh
│   └── start-dev.sh
│
├── docs/                              # Additional documentation
│   ├── api/
│   ├── user-guide/
│   └── admin-guide/
│
├── project_docs/                      # Project requirements
│   ├── Barclays RegReporting POV.pptx
│   └── Requirement Analysis.docx
│
├── .gitignore
├── README.md                          # Quick start guide
├── ARCHITECTURE.md                    # Complete architecture documentation
└── PROJECT_STRUCTURE.md               # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 14+** (installed locally)
- **Git**

### Initial Setup

```bash
# 1. Install PostgreSQL locally (if not already installed)
# Windows: Download from https://www.postgresql.org/download/
# Linux: sudo apt-get install postgresql
# Mac: brew install postgresql

# 2. Create database
createdb regulatory_reporting

# 3. Clone repository
git clone <repository-url>
cd nttdata_regulatory_reporting_system

# 4. Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration

# 5. Setup frontend (no database init needed!)
cd ../frontend
npm install
npx shadcn-ui@latest init
cp .env.example .env
# Edit .env: VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Running the Application

**Backend** (single command):
```bash
cd backend
python app.py
```

**What happens automatically on first run**:
- ✅ **Creates all database tables** (from SQLAlchemy models - no Alembic!)
- ✅ Creates storage directories (24 folders)
- ✅ Seeds initial data (admin user, 6 roles, 50+ permissions)
- ✅ Initializes ChromaDB collections
- ✅ Starts FastAPI server (port 8000)
- ✅ Starts background cleanup scheduler
- ✅ Starts task queue worker
- ✅ Enables WebSocket support

**Note**: Everything is automatic! No Alembic migrations, no manual database setup. Just run `python app.py`!

**Frontend**:

Development mode:
```bash
cd frontend
npm run dev
```

Production build:
```bash
cd frontend
npm run build
npm run preview
```

### Access Points
- **Frontend**: http://localhost:5173 (dev) or http://localhost:4173 (preview)
- **Backend API Docs**: http://localhost:8000/api/v1/docs
- **Backend ReDoc**: http://localhost:8000/api/v1/redoc
- **PostgreSQL**: localhost:5432

### Default Admin Credentials
```
Email: admin@example.com
Password: admin123
```

---

## 🗄️ Database Structure

### PostgreSQL (All-in-One Database)

**Core Tables**:
- **Users & RBAC**: users, roles, permissions, user_roles, role_permissions
- **Sessions**: sessions (JWT token management)
- **Cache**: cache (application caching)
- **Rate Limits**: rate_limits (API throttling)
- **Task Queue**: task_queue (background jobs)
- **Core Data**: regulatory_updates, requirements, data_mappings, reports
- **File Metadata**: file_metadata (storage file tracking)
- **Audit**: audit_logs (PostgreSQL table + JSONL files)

### ChromaDB (Two Collections)

**Collection 1: regulatory_documents**
```python
{
    "documents": ["Document text chunks"],
    "metadatas": [{
        "document_id": "doc_001",
        "document_type": "FCA",
        "upload_date": "2026-01-01",
        "chunk_index": 0
    }]
}
```

**Collection 2: knowledge_graph**
```python
{
    "documents": ["Entity descriptions"],
    "metadatas": [{
        "entity_id": "req_001",
        "entity_type": "Requirement",
        "relates_to": ["field_001", "field_002"],
        "relationship_types": ["REQUIRES"],
        "community": 1,
        "centrality": {"betweenness": 0.35}
    }]
}
```

### Local Filesystem (`./storage/`)

**Automatically created by `app.py`**:
```
./storage/
├── documents/          # Raw regulatory documents (PDF, Word, Excel)
│   ├── fca/, pra/, boe/
├── reports/            # Generated reports (CSV, Excel)
│   ├── submissions/, validation/
├── audit_logs/         # Daily .jsonl files
├── generated_code/     # SQL, Python code
├── graphrag/           # Knowledge graphs, communities, entities
│   ├── graphs/, communities/, entities/, analysis/
├── embeddings/         # Pre-computed vectors, tiktoken cache
│   ├── vectors/, tiktoken_cache/, indexes/
├── workflows/          # Workflow execution tracking
│   ├── definitions/, executions/, state/, history/
├── backups/            # Automated backups
│   ├── daily/, weekly/, monthly/
└── temp/              # Temporary processing
    ├── uploads/, processing/
```

### File Metadata (PostgreSQL)
- **Table**: `file_metadata` - Stores file paths, sizes, checksums, upload info

---

## 🤖 Hierarchical Agent Structure

### Agent Hierarchy (7 Agents)

```
                    Compliance Agent (Level 0)
                    Master Orchestrator
                              |
        ┌─────────────────────┼─────────────────────┐
        |                     |                     |
  BA Supervisor         Dev Supervisor        QA Supervisor
    (Level 1)              (Level 1)             (Level 1)
        |                     |                     |
  Interpreter Agent     Architect Agent       Auditor Agent
    (Level 2)              (Level 2)             (Level 2)
```

### Agent Files

**Level 0 - Master**:
- `backend/app/agents/level_0/compliance_agent.py`

**Level 1 - Supervisors**:
- `backend/app/agents/level_1/ba_supervisor_agent.py`
- `backend/app/agents/level_1/dev_supervisor_agent.py`
- `backend/app/agents/level_1/qa_supervisor_agent.py`

**Level 2 - Workers**:
- `backend/app/agents/level_2/interpreter_agent.py`
- `backend/app/agents/level_2/architect_agent.py`
- `backend/app/agents/level_2/auditor_agent.py`

### Workflow Flow

1. User uploads document
2. Compliance Agent receives request
3. Compliance Agent → BA Supervisor → Interpreter Agent
4. BA Supervisor reviews → Compliance Agent approves
5. Compliance Agent → Dev Supervisor → Architect Agent
6. Dev Supervisor reviews → Compliance Agent approves
7. Compliance Agent → QA Supervisor → Auditor Agent
8. QA Supervisor reviews → Compliance Agent final approval
9. Compliance Agent → User: Workflow complete

---

## 📦 Dependencies (requirements.txt)

### Single Requirements File

**All dependencies in one file** - no separate dev requirements!

**`backend/requirements.txt`** includes:

#### Core Framework (6 packages)
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- pydantic==2.5.0
- pydantic[email]==2.5.0
- pydantic-settings==2.1.0

#### Database & ORM (2 packages)
- sqlalchemy[asyncio]==2.0.23
- asyncpg==0.29.0
- ~~alembic~~ (removed - not needed!)

#### Authentication & Security (4 packages)
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- bcrypt==4.0.1
- python-multipart==0.0.6

#### AI/ML Stack (8 packages)
- openai==1.3.0
- langchain==0.1.0
- langchain-openai==0.0.2
- langchain-core==0.1.0
- langchain-community==0.0.10
- chromadb==0.4.18
- graphrag==0.1.0
- tiktoken==0.5.2

#### Graph & Data Analysis (5 packages)
- networkx==3.2.1
- python-louvain==0.16
- scikit-learn==1.3.2
- numpy==1.26.2
- pandas==2.1.4

#### Document Processing (6 packages)
- python-docx==1.1.0
- PyPDF2==3.0.1
- pdfplumber==0.10.3
- openpyxl==3.1.2
- python-pptx==0.6.23
- lxml==4.9.3

#### HTTP & WebSocket (3 packages)
- httpx==0.25.2
- python-socketio==5.10.0
- websockets==12.0

#### File Operations (1 package)
- aiofiles==23.2.1

#### Utilities (2 packages)
- python-dotenv==1.0.0
- tenacity==8.2.3

#### Monitoring & Logging (2 packages)
- prometheus-client==0.19.0
- python-json-logger==2.0.7

#### Development Tools (3 packages)
- ipython==8.18.1
- ipdb==0.13.13
- jupyter==1.0.0

#### Testing (5 packages)
- pytest==7.4.3
- pytest-asyncio==0.21.1
- pytest-cov==4.1.0
- pytest-mock==3.12.0
- faker==20.1.0

#### Code Quality (5 packages)
- black==23.12.0
- flake8==6.1.0
- mypy==1.7.1
- isort==5.13.0
- pylint==3.0.3

#### Type Stubs (2 packages)
- types-redis==4.6.0.11
- types-requests==2.31.0.10

#### Documentation (2 packages)
- mkdocs==1.5.3
- mkdocs-material==9.5.2

#### Task Monitoring (1 package)
- flower==2.0.1

**Total: 60+ packages** (production + development)

### Installation

```bash
cd backend
pip install -r requirements.txt
```

That's it! One command installs everything.

---

## 📦 Environment Variables

### Backend (`.env`)
```bash
# Application
APP_NAME="Regulatory Reporting System"
ENVIRONMENT=development
DEBUG=True
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your-secret-key-here

# Database
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=reg_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=regulatory_reporting

# ChromaDB
CHROMADB_PERSIST_DIRECTORY=./chroma_db

# Storage
STORAGE_PATH=./storage

# AI/ML
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo

# JWT
JWT_SECRET_KEY=your-jwt-secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=["http://localhost:5173"]
```

### Frontend (`.env`)
```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENVIRONMENT=development
```

---

## 🛠️ File Naming Conventions

### Frontend
- **Components**: PascalCase (e.g., `UserManagement.tsx`)
- **Hooks**: camelCase with 'use' prefix (e.g., `useAuth.ts`)
- **Services**: camelCase with 'Api' suffix (e.g., `authApi.ts`)
- **Types**: camelCase with '.types' suffix (e.g., `auth.types.ts`)
- **shadcn/ui**: lowercase with hyphens (e.g., `button.tsx`, `dropdown-menu.tsx`)

### Backend
- **Models**: snake_case (e.g., `user.py`, `regulatory_update.py`)
- **Services**: snake_case with '_service' suffix (e.g., `auth_service.py`)
- **Endpoints**: snake_case (e.g., `regulatory_updates.py`)
- **Agents**: snake_case with '_agent' suffix (e.g., `compliance_agent.py`)
- **Tests**: 'test_' prefix (e.g., `test_auth.py`)

---

## 🎯 Key Benefits

### Simplified Architecture
- ✅ **2 Databases Only**: PostgreSQL + ChromaDB (down from 5)
- ✅ **No Docker**: Direct Python/npm commands
- ✅ **Single Command**: `python app.py` starts everything
- ✅ **Automatic Setup**: Runs initialization scripts automatically

### Hierarchical Agents
- ✅ **Clear Chain of Command**: Compliance → Supervisors → Workers
- ✅ **Quality Gates**: Supervisors review before escalation
- ✅ **Full Audit Trail**: Every step tracked in workflows/

### Local Storage
- ✅ **GraphRAG Persistence**: Graphs saved for fast retrieval
- ✅ **Embedding Cache**: Avoid re-computing expensive embeddings
- ✅ **Workflow Tracking**: Complete orchestration history

### Cost Savings
- 💰 **$170-330/month saved**: No Neo4j, Pinecone, MongoDB, Redis, MinIO
- 💰 **Reduced API costs**: Cached embeddings and tokenization

---

## 📚 Additional Resources

- **[README.md](README.md)** - Quick start guide and overview
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete system architecture
- **Microsoft GraphRAG**: [GitHub](https://github.com/microsoft/graphrag)
- **ChromaDB**: [Documentation](https://docs.trychroma.com/)
- **NetworkX**: [Documentation](https://networkx.org/)
- **shadcn/ui**: [Components](https://ui.shadcn.com/)
- **FastAPI**: [Documentation](https://fastapi.tiangolo.com/)

---

## 🔄 Development Workflow

### Daily Development

```bash
# Start backend (Terminal 1)
cd backend
source venv/bin/activate
python app.py

# Start frontend (Terminal 2)
cd frontend
npm run dev
```

### Making Changes

**Backend**:
1. Modify code in `backend/app/`
2. FastAPI auto-reloads (if DEBUG=True)
3. Test at http://localhost:8000/api/v1/docs

**Frontend**:
1. Modify code in `frontend/src/`
2. Vite auto-reloads
3. Test at http://localhost:5173

**Database Schema Changes**:

No Alembic! Use manual SQL migration files:

1. Update SQLAlchemy model in `backend/app/models/`
2. Create migration SQL file in `backend/migrations/`
3. Apply manually: `psql -U user -d db < migrations/XXX_name.sql`

Example migration file structure:
```
backend/migrations/
├── 001_initial_schema.sql
├── 002_add_workflow_priority.sql
└── README.md
```

See [ARCHITECTURE.md](ARCHITECTURE.md#database-migrations-manual-sql-files) for details.

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test

# E2E tests
npm run test:e2e
```

---

**Built with ❤️ for Regulatory Excellence**
