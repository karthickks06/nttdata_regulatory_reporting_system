# NTT Data Regulatory Reporting System

An AI-Agentic Regulatory Reporting Platform powered by **React**, **FastAPI**, **Microsoft GraphRAG**, **NetworkX**, **ChromaDB**, and **shadcn/ui**.

## 🚀 Overview

This system transforms fragmented regulatory reporting into a unified, AI-powered ecosystem that automates requirement extraction, code generation, validation, and audit trail creation across FCA, PRA, and BOE regulations.

### Key Features

- **🤖 Hierarchical AI Agents**: 1 Compliance Agent → 3 Supervisor Agents → 3 Worker Agents (7 total)
- **🧠 Microsoft GraphRAG**: Knowledge graph with community detection
- **🔍 ChromaDB**: Unified vector + knowledge graph storage
- **📊 NetworkX**: Advanced graph analysis and lineage tracking
- **🎨 shadcn/ui**: Modern, accessible UI components
- **🎯 RBAC**: Comprehensive role-based access control
- **📈 Real-time Updates**: WebSocket for agent progress tracking
- **💰 Cost-Effective**: ChromaDB replaces both Neo4j and Pinecone

---

## 📋 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Complete system architecture, RBAC, agent implementation |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Directory structure, file organization, setup guide |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete API reference and testing guide |
| [STORAGE_STRUCTURE.md](STORAGE_STRUCTURE.md) | Centralized storage structure and file management |
| [STORAGE_MIGRATION.md](STORAGE_MIGRATION.md) | Storage centralization migration guide |
| [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md) | LLM setup guide (OpenAI & Azure OpenAI) |
| [ENV_SETUP_GUIDE.md](ENV_SETUP_GUIDE.md) | Environment configuration step-by-step |
| [VALIDATION_REPORT.md](VALIDATION_REPORT.md) | Complete validation report and production readiness |
| [backend/app/agents/config/prompts.py](backend/app/agents/config/prompts.py) | All AI agent prompts (7 hierarchical + 7 sub-agents) |

---

## 🛠️ Technology Stack

### Frontend
- **React 18** + **TypeScript** + **Vite**
- **shadcn/ui** + **Tailwind CSS** - Modern, accessible UI
- **Redux Toolkit** + **React Query** - State management
- **React Flow** - Data lineage visualization

### Backend
- **FastAPI** - High-performance Python API
- **SQLAlchemy** + **asyncpg** - Async database
- **Celery** + **RabbitMQ** - Task queue

### AI/ML
- **Microsoft GraphRAG** - Knowledge graph RAG with community detection
- **ChromaDB** - Unified vector database + knowledge graph storage
- **NetworkX** - Graph algorithms and analysis
- **LangChain** - LLM orchestration
- **OpenAI GPT-4** - Language model

### Databases (Simplified to 2)
- **PostgreSQL** - All-in-one: RBAC, users, sessions, cache, rate limits, task queue, metadata
- **ChromaDB** - Vector embeddings + knowledge graph (replaces Neo4j + Pinecone)
- **Local Filesystem** - Documents, reports, GraphRAG graphs, embeddings, workflows (`./storage/`)

---

## 🎯 User Personas

### 1. Regulatory Business Analyst
**Challenge**: Reading 500-page regulatory updates to identify changes

**AI Solution**: Interpreter Agent
- Extracts requirements automatically
- Generates gap analysis reports
- Maps to existing data dictionary
- Provides semantic reasoning

### 2. Data Engineer / Developer
**Challenge**: Writing complex SQL/Python transformations

**AI Solution**: Architect Agent
- Auto-generates SQL scripts
- Creates Python ETL code
- Produces lineage maps
- Generates test cases

### 3. Regulatory Reporting Analyst
**Challenge**: Manual validation and "stare and compare"

**AI Solution**: Auditor Agent
- Anomaly detection with explanations
- Cross-report reconciliation
- Natural language variance insights
- Audit pack generation

---

## 🚀 Quick Start

### Prerequisites
- **Node.js 18+**
- **Python 3.11+**
- **PostgreSQL 14+** (installed locally)
- **Git**

### 1. Clone Repository
```bash
git clone <repository-url>
cd nttdata_regulatory_reporting_system
```

### 2. Setup PostgreSQL Database

**Install PostgreSQL locally**:

**Windows**:
```bash
# Download and install PostgreSQL from https://www.postgresql.org/download/windows/
# Or use chocolatey:
choco install postgresql

# Create database
psql -U postgres
CREATE DATABASE regulatory_reporting;
CREATE USER reg_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE regulatory_reporting TO reg_user;
\q
```

**Linux/Mac**:
```bash
# Install PostgreSQL
sudo apt-get install postgresql  # Ubuntu/Debian
brew install postgresql          # Mac

# Start PostgreSQL service
sudo service postgresql start    # Linux
brew services start postgresql   # Mac

# Create database
sudo -u postgres psql
CREATE DATABASE regulatory_reporting;
CREATE USER reg_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE regulatory_reporting TO reg_user;
\q
```

### 3. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration:
# - Database credentials
# - OpenAI API key
# - Storage path
```

**Run Backend** (single command - no other steps needed!):
```bash
python app.py
```

**What `app.py` does automatically on FIRST RUN**:
- ✅ Creates ALL database tables from SQLAlchemy models
- ✅ Creates storage directories (24 folders)
- ✅ Seeds initial data (admin user, roles, permissions)
- ✅ Initializes ChromaDB collections
- ✅ Starts FastAPI server (port 8000)
- ✅ Starts background cleanup scheduler
- ✅ Starts task queue worker
- ✅ Enables WebSocket connections

**No Alembic migrations needed!** Tables are created automatically.

**First run output**:
```
🏦 NTT Data Regulatory Reporting System
==================================================
🔧 Initializing system...
📁 Setting up storage directories...
✅ Created: storage/documents/fca
✅ Created: storage/reports/submissions
✅ Created: storage/graphrag/graphs
... (24 directories total)
✅ Storage structure created successfully!

🗄️  Initializing database...
✅ Database connection successful
📋 No tables found. Creating database schema...
✅ Created 18 database tables
👤 Seeding initial data...
✅ Initial data seeded successfully

🔍 Initializing ChromaDB...
✅ ChromaDB initialized (2 collections)
✅ System initialization complete!

Environment: development
API URL: http://0.0.0.0:8000
API Docs: http://0.0.0.0:8000/api/v1/docs
Storage: ./storage
==================================================
🚀 Starting background services...
✅ Cleanup scheduler started
✅ Task queue worker started
✅ All services started successfully!
```

**Subsequent runs** (after first time):
- Skips seeding (users already exist)
- Storage directories already created
- Just starts services

### 4. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Initialize shadcn/ui (first time only)
npx shadcn-ui@latest init

# Add shadcn/ui components (first time only)
npx shadcn-ui@latest add button card input label table dialog
npx shadcn-ui@latest add dropdown-menu select tabs form toast

# Create .env file
cp .env.example .env
# Edit .env:
# VITE_API_BASE_URL=http://localhost:8000/api/v1
```

**Run Frontend**:

**Development mode**:
```bash
npm run dev
```

**Production build**:
```bash
npm run build
npm run preview  # Preview production build
```

### 5. Access the Application
- **Frontend**: http://localhost:5173 (dev) or http://localhost:4173 (preview)
- **API Docs**: http://localhost:8000/api/v1/docs
- **API ReDoc**: http://localhost:8000/api/v1/redoc

### Default Admin Credentials
```
Email: admin@example.com
Password: admin123
```

---

## 📦 Installation - Backend Dependencies

**Single requirements file for everything** (production + development):

```bash
# Install all dependencies
pip install -r requirements.txt
```

**Includes**:
- **Core Framework**: FastAPI, Uvicorn, Pydantic, SQLAlchemy
- **Database**: asyncpg (PostgreSQL)
- **Authentication**: python-jose, passlib, bcrypt
- **AI/ML Stack**: OpenAI, LangChain, ChromaDB, GraphRAG, NetworkX
- **Document Processing**: PyPDF2, pdfplumber, python-docx, openpyxl
- **Development Tools**: pytest, black, flake8, mypy, isort, pylint
- **Utilities**: httpx, aiofiles, python-dotenv, tenacity

**No separate requirements-dev.txt** - everything in one file!

---

## 📦 Installation - Frontend Dependencies

```bash
# Core
npm install react react-dom react-router-dom
npm install @reduxjs/toolkit react-redux @tanstack/react-query
npm install react-hook-form zod @hookform/resolvers/zod axios

# shadcn/ui + Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npm install tailwindcss-animate class-variance-authority clsx tailwind-merge
npm install lucide-react framer-motion

# Charts & Visualization
npm install recharts react-flow-renderer

# Initialize shadcn/ui
npx shadcn-ui@latest init
```

---

## 📁 Project Structure

```
nttdata_regulatory_reporting_system/
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/ui/     # shadcn/ui components
│   │   ├── features/          # Feature modules
│   │   ├── shared/            # Shared utilities
│   │   └── lib/               # Utils (cn helper)
│   └── tailwind.config.js
│
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── agents/            # AI agents
│   │   ├── sub_agents/        # ChromaDB, NetworkX agents
│   │   ├── api/               # API endpoints
│   │   ├── core/              # Config, security, RBAC
│   │   └── db/                # Database connections
│   └── requirements.txt
│
├── chroma_db/                  # ChromaDB storage
├── docker-compose.yml
├── ARCHITECTURE.md
├── PROJECT_STRUCTURE.md
└── README.md
```

---

## 🤖 AI Agent Architecture

### ChromaDB Unified Storage

ChromaDB serves **dual purpose**:

1. **Vector Database**: Semantic search with embeddings
2. **Knowledge Graph**: Entity relationships via metadata

```python
# Store entities with relationships
chroma_collection.add(
    documents=["Requirement description"],
    metadatas=[{
        "entity_id": "req_001",
        "entity_type": "Requirement",
        "relates_to": ["field_001", "field_002"],
        "relationship_types": ["REQUIRES"],
        "community": 1,  # From NetworkX
        "centrality": {"betweenness": 0.35}
    }]
)

# Semantic search
results = chroma_collection.query(
    query_texts=["liquidity coverage ratio"],
    n_results=5,
    where={"document_type": "FCA"}
)

# Graph traversal
graph_results = chroma_collection.query(
    where={
        "$and": [
            {"entity_type": "Requirement"},
            {"community": {"$eq": 1}}
        ]
    }
)
```

### Hierarchical Agent Structure (7 Agents)

**Agent Hierarchy**:
```
            Compliance Agent (Level 0)
                    |
    ┌───────────────┼───────────────┐
    |               |               |
BA Supervisor  Dev Supervisor  QA Supervisor (Level 1)
    |               |               |
Interpreter    Architect       Auditor (Level 2)
  Agent          Agent          Agent
```

**Level 0 - Master Orchestrator**:
- **Compliance Agent**: Top-level coordinator, final approval, compliance oversight

**Level 1 - Supervisor Agents**:
- **BA Supervisor Agent**: Manages Interpreter Agent, quality review, escalates to Compliance
- **Dev Supervisor Agent**: Manages Architect Agent, code review, escalates to Compliance
- **QA Supervisor Agent**: Manages Auditor Agent, test validation, escalates to Compliance

**Level 2 - Worker Agents**:
- **Interpreter Agent** (Business Analyst): Document parsing, requirement extraction, gap analysis
- **Architect Agent** (Developer): SQL/Python code generation, data lineage, test cases
- **Auditor Agent** (QA Analyst): Anomaly detection, cross-report reconciliation, audit trail

**Benefits**:
- ✅ Clear chain of command
- ✅ Quality gates at supervisor level
- ✅ Compliance oversight across all teams
- ✅ Scalable (add more workers per supervisor)
- ✅ Error isolation before reaching top level

---

## 🔐 RBAC System

### Roles
- **System Administrator** - Full system access
- **Compliance Manager** - Workflow approval, audit access
- **Regulatory Business Analyst** - Requirements management
- **Data Engineer / Developer** - Code generation, pipeline execution
- **Regulatory Reporting Analyst** - Report generation, validation
- **Read-Only User** - View-only access

### Permission System
```python
# Endpoint protection
@router.get("/requirements")
@require_permissions(["requirements.view"])
async def get_requirements(current_user: User = Depends(get_current_user)):
    pass

# UI permission guard
<PermissionGuard permissions={["requirements.edit"]}>
  <EditRequirementButton />
</PermissionGuard>
```

---

## 📊 Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- Infrastructure setup
- Core RBAC & authentication
- User management

### Phase 2: Document Processing & BA Agent (Weeks 5-8)
- Document upload system
- Interpreter Agent
- ChromaDB document indexing
- BA dashboard

### Phase 3: Knowledge Graph & RAG (Weeks 9-12)
- ChromaDB knowledge graph structure
- Microsoft GraphRAG integration
- NetworkX analysis tools

### Phase 4: Developer Tools (Weeks 13-16)
- Code generation
- Architect Agent
- Developer dashboard

### Phase 5: Reporting & Auditor Agent (Weeks 17-20)
- Report generation engine
- Auditor Agent
- Validation dashboard

### Phase 6: Workflow & Orchestration (Weeks 21-24)
- Workflow engine
- Agent orchestration
- Real-time tracking

### Phase 7-8: Testing & Deployment (Weeks 25-30)
- Comprehensive testing
- Performance optimization
- Production deployment

---

## 💡 Why Only 2 Databases?

### Simplified Architecture Benefits

| Feature | Traditional Approach | Simplified Approach |
|---------|---------------------|---------------------|
| **Databases** | PostgreSQL + Neo4j + MongoDB + Redis + Pinecone (5) | PostgreSQL + ChromaDB (2) |
| **Cost** | Multiple licenses/subscriptions | Free, open-source only |
| **Complexity** | Five databases to maintain | Two databases |
| **Backup** | Five backup strategies | Two backups |
| **Deployment** | Multiple containers | Minimal containers |
| **Storage** | Separate object storage (MinIO/S3) | Local filesystem |

### Why PostgreSQL for Everything?

**PostgreSQL replaces**:
- **Redis**: Sessions, cache, rate limits (PostgreSQL tables)
- **MongoDB**: Document metadata (PostgreSQL JSONB)
- **RabbitMQ**: Task queue (PostgreSQL table with row locking)
- **MinIO/S3**: File metadata (PostgreSQL) + local filesystem for files

### Why ChromaDB Only?

**ChromaDB replaces**:
- **Neo4j**: Knowledge graph (via metadata fields)
- **Pinecone**: Vector embeddings (built-in)

### How It Works

1. **Vector Embeddings**: Store document chunks with semantic embeddings
2. **Entity Metadata**: Store entity relationships in metadata fields
3. **NetworkX Analysis**: Build in-memory graphs for analysis
4. **Community Detection**: Calculate communities and store back in metadata
5. **Unified Queries**: Query both vectors and graph structure together

```python
# Example: Find requirements in same community with high centrality
results = chroma_collection.query(
    query_texts=["PSD008 requirements"],
    where={
        "$and": [
            {"community": {"$eq": 1}},
            {"centrality.betweenness": {"$gt": 0.3}}
        ]
    },
    n_results=10
)
```

---

## 📁 Local Filesystem Storage

### Storage Structure

All data is stored locally in `./storage/` with the following organization:

```
./storage/
├── documents/       - Raw regulatory documents (PDF, Word, Excel)
├── reports/         - Generated reports (CSV, Excel)
├── audit_logs/      - Daily audit logs (.jsonl format)
├── generated_code/  - AI-generated SQL & Python code
├── graphrag/        - Microsoft GraphRAG knowledge graphs
│   ├── graphs/      - NetworkX graphs (.gpickle, .json, .gexf)
│   ├── communities/ - Community detection results
│   ├── entities/    - Extracted entities & relationships
│   └── analysis/    - Centrality metrics, critical paths
├── embeddings/      - Vector embeddings & tiktoken cache
│   ├── vectors/     - Pre-computed embeddings (.npy)
│   ├── tiktoken_cache/ - Tokenization cache (avoid re-computation)
│   └── indexes/     - FAISS/HNSW index backups
├── workflows/       - Workflow execution tracking
│   ├── definitions/ - Workflow templates (BA, Dev, QA)
│   ├── executions/  - Active workflow runs (by month)
│   ├── state/       - Current workflow states
│   └── history/     - Completed/failed workflow logs
├── backups/         - Automated daily/weekly/monthly backups
└── temp/           - Temporary upload & processing files
```

### Why Local Filesystem?

**Benefits**:
- ✅ **GraphRAG Persistence**: Store NetworkX graphs for fast retrieval
- ✅ **Embedding Cache**: Avoid re-computing expensive embeddings
- ✅ **Workflow Tracking**: Complete audit trail of agent orchestration
- ✅ **Cost-Effective**: No cloud storage fees ($20-50/month savings)
- ✅ **Fast Access**: Local disk reads (< 10ms)
- ✅ **Simple Backup**: Standard tar.gz compression

**Key Features**:
1. **GraphRAG Graphs**: Stored in 3 formats (.gpickle, .json, .gexf) for flexibility
2. **Tiktoken Cache**: Cached tokenization results to save API costs
3. **Workflow State**: Real-time tracking of Compliance → Supervisor → Worker agent flows
4. **Automated Cleanup**: Old files automatically archived after 30 days

---

## 🎨 UI Components (shadcn/ui)

### Example Usage

```typescript
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Table } from '@/components/ui/table'

<Card>
  <CardHeader>
    <CardTitle>Requirements</CardTitle>
  </CardHeader>
  <CardContent>
    <Table>
      {/* Table content */}
    </Table>
    <Button variant="default" size="lg">
      Generate Report
    </Button>
  </CardContent>
</Card>
```

All components are **fully customizable** and live in your codebase.

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

## 📚 API Documentation

Once the backend is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

---

## 🎯 Key Benefits

### Day 1 (Semi-Automated)
- **70-80% efficiency gain**
- AI generates code, humans review
- Manual execution and validation

### Day 2 (Fully Autonomous)
- **Hands-free execution** - Digital concierge
- **100% audit shield** - Continuous assurance
- **Self-explaining numbers** - Natural language insights

### Cost Savings
- **No Neo4j**: Save $50-100/month (graph database eliminated)
- **No Pinecone**: Save $70-100/month (vector DB eliminated)
- **No MongoDB**: Save $20-50/month (document DB eliminated)
- **No Redis**: Save $10-30/month (cache eliminated)
- **No MinIO/S3**: Save $20-50/month (object storage eliminated)
- **Total Savings**: $170-330/month per environment

### Technical Benefits
- **2 Databases Only**: PostgreSQL + ChromaDB (down from 5)
- **Single Backup Strategy**: PostgreSQL dump + ChromaDB persist dir + filesystem tar
- **Simpler Deployment**: Fewer containers, easier scaling
- **Local Filesystem**: Fast access, no cloud storage costs
- **PostgreSQL All-in-One**: Sessions, cache, rate limits, task queue in one DB
- **NetworkX Integration**: Powerful graph algorithms without persistent graph DB

---

## 📖 Additional Resources

- **Microsoft GraphRAG**: [GitHub](https://github.com/microsoft/graphrag)
- **ChromaDB**: [Documentation](https://docs.trychroma.com/)
- **NetworkX**: [Documentation](https://networkx.org/)
- **shadcn/ui**: [Components](https://ui.shadcn.com/)
- **Tailwind CSS**: [Documentation](https://tailwindcss.com/)
- **FastAPI**: [Documentation](https://fastapi.tiangolo.com/)

---

## 🚀 Deployment

### Development Deployment

**Backend**:
```bash
cd backend
python app.py
```

**Frontend**:
```bash
cd frontend
npm run dev
```

### Production Deployment

#### Option 1: systemd Service (Linux)

**Backend Service** (`/etc/systemd/system/regulatory-reporting.service`):
```ini
[Unit]
Description=NTT Data Regulatory Reporting System
After=network.target postgresql.service

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl enable regulatory-reporting
sudo systemctl start regulatory-reporting
```

**Frontend Build**:
```bash
cd frontend
npm run build

# Serve with nginx
sudo cp -r dist/* /var/www/regulatory-reporting/
```

#### Option 2: PM2 (Cross-platform)

**Backend**:
```bash
cd backend
pm2 start app.py --name regulatory-reporting --interpreter python
pm2 save
pm2 startup
```

**Frontend**:
```bash
cd frontend
npm run build
pm2 serve dist 4173 --name frontend --spa
```

#### Option 3: Windows Service

Use **NSSM** (Non-Sucking Service Manager):
```cmd
nssm install RegulatoryReporting "C:\path\to\venv\Scripts\python.exe" "C:\path\to\backend\app.py"
nssm start RegulatoryReporting
```

### Nginx Configuration

**`/etc/nginx/sites-available/regulatory-reporting`**:
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    # Frontend
    location / {
        root /var/www/regulatory-reporting;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # WebSocket
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/regulatory-reporting /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Environment Variables

**Production `.env`** (backend):
```bash
ENVIRONMENT=production
DEBUG=False
HOST=0.0.0.0
PORT=8000
SECRET_KEY=<strong-random-key>

POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=reg_user
POSTGRES_PASSWORD=<strong-password>
POSTGRES_DB=regulatory_reporting

CHROMADB_PERSIST_DIRECTORY=/var/lib/regulatory-reporting/chroma_db
STORAGE_PATH=/var/lib/regulatory-reporting/storage

OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=<strong-jwt-secret>
```

**Production `.env`** (frontend):
```bash
VITE_API_BASE_URL=https://yourdomain.com/api/v1
```

### Database Backup

**Automated daily backup**:
```bash
# Create backup script
cat > /usr/local/bin/backup-regulatory-reporting.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/regulatory-reporting"
DATE=$(date +%Y%m%d_%H%M%S)

# PostgreSQL backup
pg_dump regulatory_reporting > "$BACKUP_DIR/postgres_$DATE.sql"

# ChromaDB backup
tar -czf "$BACKUP_DIR/chromadb_$DATE.tar.gz" /var/lib/regulatory-reporting/chroma_db/

# Storage backup
tar -czf "$BACKUP_DIR/storage_$DATE.tar.gz" /var/lib/regulatory-reporting/storage/

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
EOF

chmod +x /usr/local/bin/backup-regulatory-reporting.sh

# Add to crontab
echo "0 2 * * * /usr/local/bin/backup-regulatory-reporting.sh" | crontab -
```

### SSL/TLS with Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
sudo systemctl reload nginx
```

### Monitoring

**Health Check Endpoint**:
```python
# Already included in app.py
GET /health
```

**Monitor with systemctl** (Linux):
```bash
sudo systemctl status regulatory-reporting
sudo journalctl -u regulatory-reporting -f
```

### Scaling Considerations

**Single Server** (Current Setup):
- ✅ 1-100 concurrent users
- ✅ Up to 10,000 documents
- ✅ Storage < 500GB

**Multi-Server** (Future):
- Use NFS or S3 for shared storage
- Add load balancer (nginx)
- Scale PostgreSQL with read replicas
- Consider managed ChromaDB (Chroma Cloud)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

[Specify your license here]

---

## 📞 Support

For questions or issues:
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for setup
- Create an issue in the repository

---

## 🌟 Acknowledgments

Based on requirements from:
- Barclays RegReporting POV
- NTT Data Requirement Analysis
- FCA/PRA/BOE regulatory frameworks

Built with modern technologies to transform regulatory reporting from manual, fragmented processes into an intelligent, automated system.

---

**Key Innovation**: Using ChromaDB's rich metadata capabilities to store knowledge graph relationships alongside vector embeddings, **eliminating the need for separate Neo4j and Pinecone databases** while maintaining full functionality.

---

**Made with ❤️ for Regulatory Excellence**
