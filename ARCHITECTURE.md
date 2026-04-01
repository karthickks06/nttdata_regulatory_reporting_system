# AI-Agentic Regulatory Reporting System - Architecture Design

## Table of Contents
1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Layers](#architecture-layers)
4. [RBAC Design](#rbac-design)
5. [Frontend Architecture](#frontend-architecture)
6. [Backend Architecture](#backend-architecture)
7. [AI/ML Components](#aiml-components)
8. [Database Design](#database-design)
9. [Security & Compliance](#security--compliance)
10. [Implementation Roadmap](#implementation-roadmap)

---

## System Overview

### High-Level Architecture (Simplified - PostgreSQL + Filesystem Only)

```
┌───────────────────────────────────────────────────────────────────────┐
│                           Frontend Layer                               │
│     React 18 + TypeScript + shadcn/ui + Tailwind CSS                  │
│     Redux Toolkit + React Query + React Flow + WebSocket              │
└───────────────────────────────────────────────────────────────────────┘
                                ↓ ↑ 
                        REST API / WebSocket
                                ↓ ↑
┌───────────────────────────────────────────────────────────────────────┐
│                        API Gateway Layer                               │
│          FastAPI + JWT Auth + Rate Limiting (PostgreSQL)              │
└───────────────────────────────────────────────────────────────────────┘
                                ↓ ↑
┌───────────────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │    RBAC     │  │  Workflow   │  │    Audit    │  │   Session   │ │
│  │  Service    │  │ Orchestrator│  │   Logger    │  │  Manager    │ │
│  │             │  │             │  │ (Filesystem)│  │ (PostgreSQL)│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
└───────────────────────────────────────────────────────────────────────┘
                                ↓ ↑
┌───────────────────────────────────────────────────────────────────────┐
│                  MCP Agent Layer (Hierarchical AI)                     │
│                                                                         │
│                     ┌─────────────────────────┐                        │
│                     │   Compliance Agent      │                        │
│                     │   (Master Orchestrator) │                        │
│                     │ • Workflow Coordination │                        │
│                     │ • Cross-team Oversight  │                        │
│                     │ • Final Approval        │                        │
│                     └───────────┬─────────────┘                        │
│                                 │                                       │
│                 ┌───────────────┼───────────────┐                      │
│                 │               │               │                      │
│       ┌─────────▼─────┐  ┌──────▼──────┐  ┌────▼──────────┐          │
│       │ BA Supervisor │  │ Dev Supervisor│  │ QA Supervisor │          │
│       │   Agent       │  │    Agent      │  │    Agent      │          │
│       │ • Task Assign │  │ • Task Assign │  │ • Task Assign │          │
│       │ • Quality     │  │ • Code Review │  │ • Test Plan   │          │
│       │ • Escalation  │  │ • Escalation  │  │ • Escalation  │          │
│       └───────┬───────┘  └───────┬───────┘  └───────┬───────┘          │
│               │                  │                  │                  │
│       ┌───────▼────────┐ ┌───────▼────────┐ ┌──────▼─────────┐       │
│       │  Interpreter   │ │  Architect     │ │  Auditor       │       │
│       │  Agent (BA)    │ │  Agent (Dev)   │ │  Agent (QA)    │       │
│       ├────────────────┤ ├────────────────┤ ├────────────────┤       │
│       │• Req Extract   │ │• Code Gen      │ │• Validation    │       │
│       │• Gap Analysis  │ │• SQL/Python    │ │• Anomaly Det   │       │
│       │• Impact Map    │ │• Lineage Map   │ │• Reconciliation│       │
│       │• GraphRAG      │ │• Test Cases    │ │• Audit Trail   │       │
│       └────────────────┘ └────────────────┘ └────────────────┘       │
└───────────────────────────────────────────────────────────────────────┘
                                ↓ ↑
┌───────────────────────────────────────────────────────────────────────┐
│                     Sub-Agent & Tool Layer                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │Document  │  │MS Graph  │  │ChromaDB  │  │  LLM     │             │
│  │Parser    │  │RAG Agent │  │Unified   │  │Orchestr. │             │
│  │(PDF/XML) │  │+NetworkX │  │Agent     │  │(GPT-4)   │             │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘             │
└───────────────────────────────────────────────────────────────────────┘
                                ↓ ↑
┌───────────────────────────────────────────────────────────────────────┐
│                           Data Layer                                   │
│ ┌──────────────────────────────────────────────────────────────────┐ │
│ │                    Simplified Storage                             │ │
│ │  ┌──────────────────────┐  ┌──────────────────────┐              │ │
│ │  │    PostgreSQL        │  │     ChromaDB         │              │ │
│ │  │    (All-in-One)      │  │  (Vectors + Graph)   │              │ │
│ │  ├──────────────────────┤  ├──────────────────────┤              │ │
│ │  │• Users & RBAC        │  │• Vector Embeddings   │              │ │
│ │  │• Sessions (Table)    │  │• Entity Metadata     │              │ │
│ │  │• Cache (Table)       │  │• Knowledge Graph     │              │ │
│ │  │• Rate Limits (Table) │  │• Semantic Search     │              │ │
│ │  │• Requirements        │  │• Communities         │              │ │
│ │  │• Reports Metadata    │  │                      │              │ │
│ │  │• Audit Logs (Table)  │  │                      │              │ │
│ │  │• Task Queue (Table)  │  │                      │              │ │
│ │  └──────────────────────┘  └──────────────────────┘              │ │
│ └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌──────────────────────────────────────────────────────────────────┐ │
│ │                   Local Filesystem Storage                        │ │
│ │  ┌────────────────────────────────────────────────────────────┐  │ │
│ │  │  ./storage/                                                 │  │ │
│ │  │  ├── documents/          # Raw uploaded PDFs, Word, Excel  │  │ │
│ │  │  │   ├── 2026/                                             │  │ │
│ │  │  │   │   ├── 01/                                           │  │ │
│ │  │  │   │   │   └── FCA_update_20260115.pdf                   │  │ │
│ │  │  │   │   └── 02/                                           │  │ │
│ │  │  ├── reports/            # Generated CSV, Excel reports    │  │ │
│ │  │  │   ├── PSD008/                                           │  │ │
│ │  │  │   │   └── PSD008_Q1_2026.csv                            │  │ │
│ │  │  │   └── COREP/                                            │  │ │
│ │  │  ├── audit_logs/         # Daily audit log files           │  │ │
│ │  │  │   ├── 2026-01-15.jsonl                                  │  │ │
│ │  │  │   └── 2026-01-16.jsonl                                  │  │ │
│ │  │  ├── backups/            # Database backups                │  │ │
│ │  │  └── temp/               # Temporary processing files      │  │ │
│ │  └────────────────────────────────────────────────────────────┘  │ │
│ └──────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────┘

Legend:
━━━━━  Data flow
✅ Only 2 databases: PostgreSQL + ChromaDB
✅ No Redis, No MongoDB, No MinIO, No RabbitMQ
✅ Local filesystem for all documents and logs
✅ PostgreSQL handles sessions, cache, rate limiting, task queue
```

---

## PostgreSQL Tables for Session, Cache, Rate Limiting & Task Queue

### Why PostgreSQL for All Storage?

This architecture uses **PostgreSQL only** (no Redis, MongoDB, or MinIO) for:
- **Session Management**: JWT tokens, user sessions
- **Caching**: LLM responses, frequent queries
- **Rate Limiting**: API request throttling
- **Task Queue**: Background agent execution
- **File Metadata**: Document references (files stored on local filesystem)

**Benefits**:
- ✅ **Single Database**: Easier to maintain, backup, and scale
- ✅ **ACID Compliance**: Guaranteed data consistency
- ✅ **No Additional Infrastructure**: No Redis, RabbitMQ, MongoDB containers
- ✅ **Cost-Effective**: One database license/deployment
- ✅ **Automatic Cleanup**: Use PostgreSQL scheduled jobs for expiry

### Database Schema

#### 1. **Sessions Table**

```sql
CREATE TABLE sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL UNIQUE,  -- Hashed JWT token
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_accessed TIMESTAMP DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

-- Index for fast lookups
CREATE INDEX idx_sessions_token_hash ON sessions(token_hash);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
```

**Usage**:
```python
# Store session
async def create_session(user_id: UUID, token: str, expires_at: datetime):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    await db.execute(
        "INSERT INTO sessions (user_id, token_hash, expires_at) VALUES ($1, $2, $3)",
        user_id, token_hash, expires_at
    )

# Validate session
async def validate_session(token: str) -> Optional[User]:
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    row = await db.fetchrow(
        "SELECT user_id FROM sessions WHERE token_hash = $1 AND expires_at > NOW()",
        token_hash
    )
    return row['user_id'] if row else None
```

#### 2. **Cache Table**

```sql
CREATE TABLE cache (
    cache_key VARCHAR(255) PRIMARY KEY,
    cache_value JSONB NOT NULL,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    hit_count INTEGER DEFAULT 0
);

-- Index for expiry cleanup
CREATE INDEX idx_cache_expires_at ON cache(expires_at);
```

**Usage**:
```python
# Cache LLM response
async def cache_set(key: str, value: dict, ttl_seconds: int = 86400):
    expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
    await db.execute(
        """
        INSERT INTO cache (cache_key, cache_value, expires_at) 
        VALUES ($1, $2, $3)
        ON CONFLICT (cache_key) DO UPDATE 
        SET cache_value = $2, expires_at = $3, created_at = NOW()
        """,
        key, json.dumps(value), expires_at
    )

# Get from cache
async def cache_get(key: str) -> Optional[dict]:
    row = await db.fetchrow(
        """
        UPDATE cache SET hit_count = hit_count + 1 
        WHERE cache_key = $1 AND (expires_at IS NULL OR expires_at > NOW())
        RETURNING cache_value
        """,
        key
    )
    return json.loads(row['cache_value']) if row else None
```

#### 3. **Rate Limits Table**

```sql
CREATE TABLE rate_limits (
    identifier VARCHAR(255) PRIMARY KEY,  -- IP address or user_id
    request_count INTEGER DEFAULT 0,
    window_start TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for cleanup
CREATE INDEX idx_rate_limits_window_start ON rate_limits(window_start);
```

**Usage**:
```python
# Rate limiting middleware
async def check_rate_limit(identifier: str, max_requests: int = 100, window_minutes: int = 1):
    window_start = datetime.now() - timedelta(minutes=window_minutes)
    
    row = await db.fetchrow(
        """
        INSERT INTO rate_limits (identifier, request_count, window_start) 
        VALUES ($1, 1, NOW())
        ON CONFLICT (identifier) DO UPDATE 
        SET request_count = CASE 
            WHEN rate_limits.window_start < $2 THEN 1
            ELSE rate_limits.request_count + 1
        END,
        window_start = CASE 
            WHEN rate_limits.window_start < $2 THEN NOW()
            ELSE rate_limits.window_start
        END
        RETURNING request_count
        """,
        identifier, window_start
    )
    
    if row['request_count'] > max_requests:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
```

#### 4. **Task Queue Table**

```sql
CREATE TABLE task_queue (
    task_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_name VARCHAR(255) NOT NULL,
    task_args JSONB,
    task_kwargs JSONB,
    status VARCHAR(50) DEFAULT 'pending',  -- pending, processing, completed, failed
    priority INTEGER DEFAULT 0,
    result JSONB,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    worker_id VARCHAR(100)
);

-- Indexes for queue operations
CREATE INDEX idx_task_queue_status ON task_queue(status);
CREATE INDEX idx_task_queue_priority ON task_queue(priority DESC, created_at ASC);
CREATE INDEX idx_task_queue_completed_at ON task_queue(completed_at);
```

**Usage**:
```python
# Enqueue task (instead of Celery)
async def enqueue_task(task_name: str, *args, **kwargs):
    task_id = await db.fetchval(
        """
        INSERT INTO task_queue (task_name, task_args, task_kwargs) 
        VALUES ($1, $2, $3) 
        RETURNING task_id
        """,
        task_name, json.dumps(args), json.dumps(kwargs)
    )
    return task_id

# Worker picks up task
async def worker_get_next_task():
    row = await db.fetchrow(
        """
        UPDATE task_queue 
        SET status = 'processing', started_at = NOW(), worker_id = $1
        WHERE task_id = (
            SELECT task_id FROM task_queue 
            WHERE status = 'pending' 
            ORDER BY priority DESC, created_at ASC 
            LIMIT 1
            FOR UPDATE SKIP LOCKED
        )
        RETURNING task_id, task_name, task_args, task_kwargs
        """,
        worker_id
    )
    return row

# Mark task complete
async def complete_task(task_id: UUID, result: dict):
    await db.execute(
        """
        UPDATE task_queue 
        SET status = 'completed', result = $2, completed_at = NOW()
        WHERE task_id = $1
        """,
        task_id, json.dumps(result)
    )
```

### Automated Cleanup (Application-Level)

**Since PostgreSQL extensions (pg_cron) are not available, use application-level scheduled cleanup**:

```python
# backend/app/tasks/cleanup_tasks.py
import asyncio
from datetime import datetime, timedelta
from app.db.postgres import get_db_pool

class CleanupScheduler:
    """Background task scheduler for database cleanup"""
    
    def __init__(self):
        self.running = False
    
    async def cleanup_expired_sessions(self):
        """Run every 5 minutes"""
        async with get_db_pool().acquire() as conn:
            deleted = await conn.execute(
                "DELETE FROM sessions WHERE expires_at < NOW()"
            )
            print(f"Cleaned up {deleted} expired sessions")
    
    async def cleanup_expired_cache(self):
        """Run every 10 minutes"""
        async with get_db_pool().acquire() as conn:
            deleted = await conn.execute(
                "DELETE FROM cache WHERE expires_at IS NOT NULL AND expires_at < NOW()"
            )
            print(f"Cleaned up {deleted} expired cache entries")
    
    async def cleanup_old_rate_limits(self):
        """Run every minute"""
        async with get_db_pool().acquire() as conn:
            deleted = await conn.execute(
                "DELETE FROM rate_limits WHERE window_start < NOW() - INTERVAL '10 minutes'"
            )
    
    async def cleanup_completed_tasks(self):
        """Run daily at midnight"""
        async with get_db_pool().acquire() as conn:
            deleted = await conn.execute(
                "DELETE FROM task_queue WHERE completed_at < NOW() - INTERVAL '7 days'"
            )
            print(f"Cleaned up {deleted} old completed tasks")
    
    async def run_cleanup_loop(self):
        """Main cleanup loop"""
        self.running = True
        last_daily_cleanup = datetime.now()
        
        while self.running:
            try:
                now = datetime.now()
                
                # Every minute: rate limits
                if now.second == 0:
                    await self.cleanup_old_rate_limits()
                
                # Every 5 minutes: sessions
                if now.minute % 5 == 0 and now.second == 0:
                    await self.cleanup_expired_sessions()
                
                # Every 10 minutes: cache
                if now.minute % 10 == 0 and now.second == 0:
                    await self.cleanup_expired_cache()
                
                # Daily at midnight: completed tasks
                if now.hour == 0 and now.minute == 0 and (now - last_daily_cleanup).days >= 1:
                    await self.cleanup_completed_tasks()
                    last_daily_cleanup = now
                
                await asyncio.sleep(1)  # Check every second
                
            except Exception as e:
                print(f"Cleanup error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    def stop(self):
        self.running = False

# Global instance
cleanup_scheduler = CleanupScheduler()

# Start in main.py
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_scheduler.run_cleanup_loop())

@app.on_event("shutdown")
async def shutdown_event():
    cleanup_scheduler.stop()
```

### Performance Considerations

**PostgreSQL optimizations for high-performance use cases**:

1. **Connection Pooling**: Use `asyncpg` with connection pool
   ```python
   pool = await asyncpg.create_pool(
       dsn=DATABASE_URL,
       min_size=10,
       max_size=50
   )
   ```

2. **Prepared Statements**: Automatically cached by asyncpg
   
3. **UNLOGGED Tables** (for cache only - no WAL overhead):
   ```sql
   CREATE UNLOGGED TABLE cache (...);  -- 2-3x faster writes
   ```

4. **Partitioning** (for large tables):
   ```sql
   CREATE TABLE audit_logs (...) PARTITION BY RANGE (created_at);
   ```

5. **Vacuum Strategy** (no extensions needed):
   ```sql
   -- Configure autovacuum for cleanup tables
   ALTER TABLE sessions SET (autovacuum_vacuum_scale_factor = 0.1);
   ALTER TABLE cache SET (autovacuum_vacuum_scale_factor = 0.1);
   ALTER TABLE rate_limits SET (autovacuum_vacuum_scale_factor = 0.05);
   ```

### Comparison: Redis vs PostgreSQL

| Feature | Redis | PostgreSQL (Optimized) |
|---------|-------|------------------------|
| **Session lookup** | <1ms | 2-5ms (with indexes) |
| **Cache read** | <1ms | 2-8ms (with UNLOGGED table) |
| **Rate limit check** | <1ms | 3-10ms |
| **Task queue** | Built-in | Custom implementation |
| **Persistence** | Optional | Always persisted |
| **ACID** | No | Yes |
| **Backup** | Separate | Single backup |
| **Maintenance** | Two systems | One system |

**Trade-off**: Slightly slower (~5-10ms vs <1ms) but **much simpler architecture**.

---

## Technology Stack

### Frontend
```json
{
  "core": ["React 18.x", "TypeScript 5.x", "Vite"],
  "state_management": ["Redux Toolkit", "React Query (TanStack Query)"],
  "ui_framework": ["shadcn/ui", "Radix UI", "Tailwind CSS v3.4+"],
  "ui_components": ["shadcn/ui components (Button, Card, Dialog, Form, Table, etc.)"],
  "styling": ["Tailwind CSS", "class-variance-authority", "tailwind-merge", "clsx"],
  "visualization": ["Recharts", "D3.js", "React Flow (for lineage)"],
  "forms": ["React Hook Form", "Zod (validation)"],
  "routing": ["React Router v6"],
  "realtime": ["Socket.IO Client", "WebSocket"],
  "file_upload": ["React Dropzone"],
  "pdf_viewer": ["react-pdf"],
  "code_editor": ["Monaco Editor (for SQL/Python preview)"],
  "icons": ["Lucide React"],
  "animations": ["Framer Motion"]
}
```

### Backend
```json
{
  "api": ["FastAPI 0.104+", "Pydantic 2.x"],
  "authentication": ["JWT", "OAuth2", "FastAPI-Users"],
  "async": ["asyncio", "aiohttp", "httpx"],
  "task_queue": ["Celery", "RabbitMQ/Redis"],
  "websocket": ["FastAPI WebSocket", "Socket.IO"],
  "validation": ["Pydantic", "python-multipart"]
}
```

### AI/ML Stack
```json
{
  "llm": ["OpenAI GPT-4/GPT-4-Turbo", "Azure OpenAI", "Anthropic Claude"],
  "frameworks": ["LangChain", "LlamaIndex"],
  "mcp": ["MCP SDK (Model Context Protocol)", "Custom MCP Servers"],
  "graph_rag": ["Microsoft GraphRAG", "NetworkX"],
  "graph_analysis": ["NetworkX (graph algorithms, community detection, centrality)"],
  "vector_db": ["ChromaDB (unified vector + knowledge graph storage)"],
  "embeddings": ["OpenAI Embeddings", "Sentence Transformers"],
  "rag": ["Microsoft GraphRAG", "LlamaIndex", "LangChain RAG"],
  "agents": ["LangGraph", "AutoGen", "CrewAI"],
  "document_processing": ["PyPDF2", "pdfplumber", "python-docx", "lxml"]
}
```

### Databases
```json
{
  "relational": "PostgreSQL 15+ (RBAC, Users, Metadata)",
  "vector_and_graph": "ChromaDB (Vector embeddings + Knowledge graph storage)",
  "document": "MongoDB (Regulatory Documents, Audit Logs)",
  "cache": "Redis (Session, Rate Limiting, Task Results)",
  "object_storage": "MinIO/S3 (PDF uploads, CSV reports)"
}
```

**Note**: ChromaDB serves dual purpose:
- **Vector Database**: Semantic search with embeddings
- **Knowledge Graph Storage**: Using metadata and relationships

### DevOps & Infrastructure
```json
{
  "containerization": ["Docker", "Docker Compose"],
  "orchestration": "Kubernetes (optional for production)",
  "ci_cd": "GitHub Actions / GitLab CI",
  "monitoring": ["Prometheus", "Grafana", "ELK Stack"],
  "tracing": "OpenTelemetry",
  "api_gateway": "Traefik / NGINX"
}
```

---

## Architecture Layers

### Layer 1: Presentation Layer (Frontend)

**Technology**: React 18 + TypeScript + shadcn/ui + Tailwind CSS

**Responsibilities**:
- User interface rendering
- State management (Redux Toolkit)
- Server state caching (React Query)
- Real-time updates (WebSocket)
- Route protection (RBAC)

**Key Features**:
- Feature-based architecture
- shadcn/ui components (customizable, accessible)
- Tailwind CSS utility-first styling
- Role-based UI rendering

### Layer 2: API Gateway Layer (FastAPI)

**Responsibilities**:
- RESTful API endpoints
- Request validation (Pydantic)
- Authentication (JWT)
- Authorization (RBAC middleware)
- Rate limiting
- WebSocket connections

### Layer 3: Business Logic Layer

**Services**:
- **RBAC Service**: Role and permission management
- **Workflow Orchestrator**: Multi-step process coordination
- **Audit Logger**: Complete activity tracking
- **Notification Service**: Email/WebSocket notifications
- **Validation Service**: Data quality checks

### Layer 4: MCP Agent Layer (Hierarchical Structure)

**Agent Hierarchy**:

```
                    Compliance Agent (Level 0 - Master)
                              |
        ┌─────────────────────┼─────────────────────┐
        |                     |                     |
  BA Supervisor         Dev Supervisor        QA Supervisor
    (Level 1)              (Level 1)             (Level 1)
        |                     |                     |
  Interpreter Agent     Architect Agent       Auditor Agent
    (Level 2)              (Level 2)             (Level 2)
```

#### **Level 0: Compliance Agent** (Master Orchestrator)

**Role**: Top-level orchestrator that coordinates all supervisor agents and ensures regulatory compliance.

**Responsibilities**:
- **Workflow Orchestration**: Assigns work to BA, Dev, QA supervisors
- **Cross-Team Coordination**: Ensures BA → Dev → QA handoffs are smooth
- **Final Approval**: Reviews and approves all outputs before submission
- **Compliance Verification**: Validates adherence to regulatory standards
- **Escalation Management**: Handles conflicts between supervisor agents
- **Progress Monitoring**: Tracks overall project completion
- **Risk Assessment**: Identifies compliance risks across all teams

**Capabilities**:
```python
class ComplianceAgent:
    """Master orchestrator for all regulatory reporting workflows"""
    
    async def orchestrate_workflow(self, document_id: str):
        # Step 1: Assign to BA Supervisor
        ba_result = await self.ba_supervisor.assign_task({
            "task": "extract_requirements",
            "document_id": document_id
        })
        
        # Step 2: Review BA output
        if not self.validate_requirements(ba_result):
            return await self.ba_supervisor.rework(ba_result, feedback)
        
        # Step 3: Assign to Dev Supervisor
        dev_result = await self.dev_supervisor.assign_task({
            "task": "generate_code",
            "requirements": ba_result["requirements"]
        })
        
        # Step 4: Assign to QA Supervisor
        qa_result = await self.qa_supervisor.assign_task({
            "task": "validate_implementation",
            "code": dev_result["code"],
            "requirements": ba_result["requirements"]
        })
        
        # Step 5: Final approval
        return await self.final_approval({
            "ba": ba_result,
            "dev": dev_result,
            "qa": qa_result
        })
    
    def validate_requirements(self, ba_result):
        """Validate BA output meets compliance standards"""
        pass
    
    async def final_approval(self, results):
        """Final review before submission"""
        pass
```

---

#### **Level 1: Supervisor Agents**

##### **1. BA Supervisor Agent** (Business Analysis Supervisor)

**Role**: Manages Interpreter Agent and ensures quality of requirement extraction.

**Responsibilities**:
- **Task Assignment**: Delegates document analysis to Interpreter Agent
- **Quality Review**: Reviews extracted requirements for completeness
- **Gap Analysis Validation**: Ensures gap analysis is accurate
- **Escalation to Compliance**: Reports issues to Compliance Agent
- **Rework Management**: Sends tasks back to Interpreter Agent if quality is insufficient

**Workflow**:
```python
class BASupervisorAgent:
    async def assign_task(self, task_details):
        # Assign to Interpreter Agent
        result = await self.interpreter_agent.execute(task_details)
        
        # Quality check
        if self.quality_score(result) < 0.85:
            # Request rework
            result = await self.interpreter_agent.rework(result, feedback)
        
        # Escalate to Compliance Agent
        return await self.escalate_to_compliance(result)
    
    def quality_score(self, result):
        """Calculate quality score (0-1)"""
        # Check completeness, accuracy, format
        pass
```

##### **2. Dev Supervisor Agent** (Development Supervisor)

**Role**: Manages Architect Agent and ensures code quality.

**Responsibilities**:
- **Task Assignment**: Delegates code generation to Architect Agent
- **Code Review**: Reviews generated SQL/Python for correctness
- **Test Validation**: Ensures test cases cover all scenarios
- **Lineage Verification**: Validates data lineage is accurate
- **Escalation to Compliance**: Reports completion to Compliance Agent

**Workflow**:
```python
class DevSupervisorAgent:
    async def assign_task(self, task_details):
        # Assign to Architect Agent
        result = await self.architect_agent.execute(task_details)
        
        # Code review
        review = await self.review_code(result["code"])
        if not review["approved"]:
            result = await self.architect_agent.fix_issues(review["issues"])
        
        # Validate tests
        if not await self.validate_tests(result["tests"]):
            result = await self.architect_agent.generate_more_tests(result)
        
        return await self.escalate_to_compliance(result)
    
    async def review_code(self, code):
        """Automated code review"""
        # Check syntax, best practices, performance
        pass
```

##### **3. QA Supervisor Agent** (Quality Assurance Supervisor)

**Role**: Manages Auditor Agent and ensures validation quality.

**Responsibilities**:
- **Task Assignment**: Delegates validation to Auditor Agent
- **Test Plan Review**: Ensures test coverage is comprehensive
- **Anomaly Investigation**: Reviews flagged anomalies
- **Reconciliation Verification**: Validates cross-report reconciliation
- **Escalation to Compliance**: Reports validation results to Compliance Agent

**Workflow**:
```python
class QASupervisorAgent:
    async def assign_task(self, task_details):
        # Assign to Auditor Agent
        result = await self.auditor_agent.execute(task_details)
        
        # Review validation results
        if result["anomalies_found"]:
            # Investigate each anomaly
            for anomaly in result["anomalies"]:
                investigation = await self.investigate_anomaly(anomaly)
                if investigation["critical"]:
                    # Escalate to Dev Supervisor for fix
                    await self.dev_supervisor.fix_issue(investigation)
        
        # Final sign-off
        return await self.escalate_to_compliance(result)
    
    async def investigate_anomaly(self, anomaly):
        """Deep dive into anomalies"""
        pass
```

---

#### **Level 2: Worker Agents**

##### **1. Interpreter Agent** (Business Analyst Worker)
   - Parses regulatory documents (PDF/XML)
   - Extracts requirements using LLM
   - Maps to existing data dictionary
   - Generates gap analysis
   - Provides semantic reasoning
   - **Reports to**: BA Supervisor Agent

##### **2. Architect Agent** (Developer Worker)
   - Generates SQL transformations
   - Creates Python ETL code
   - Builds data lineage maps
   - Auto-corrects mapping logic
   - Generates test cases
   - **Reports to**: Dev Supervisor Agent

##### **3. Auditor Agent** (QA Analyst Worker)
   - Performs anomaly detection
   - Provides natural language explanations
   - Cross-report reconciliation
   - Data integrity verification
   - Audit trail generation
   - **Reports to**: QA Supervisor Agent

---

### Agent Communication Flow

```
1. User uploads regulatory document
        ↓
2. Compliance Agent receives request
        ↓
3. Compliance Agent → BA Supervisor: "Extract requirements"
        ↓
4. BA Supervisor → Interpreter Agent: "Parse document"
        ↓
5. Interpreter Agent processes document
        ↓
6. BA Supervisor reviews output (quality check)
        ↓
7. BA Supervisor → Compliance Agent: "Requirements ready"
        ↓
8. Compliance Agent validates requirements
        ↓
9. Compliance Agent → Dev Supervisor: "Generate code"
        ↓
10. Dev Supervisor → Architect Agent: "Create SQL/Python"
        ↓
11. Architect Agent generates code
        ↓
12. Dev Supervisor reviews code (code review)
        ↓
13. Dev Supervisor → Compliance Agent: "Code ready"
        ↓
14. Compliance Agent → QA Supervisor: "Validate implementation"
        ↓
15. QA Supervisor → Auditor Agent: "Run tests and validations"
        ↓
16. Auditor Agent validates everything
        ↓
17. QA Supervisor reviews validation results
        ↓
18. QA Supervisor → Compliance Agent: "Validation complete"
        ↓
19. Compliance Agent performs final approval
        ↓
20. Compliance Agent → User: "Workflow complete, ready for submission"
```

---

### Benefits of Hierarchical Agent Structure

1. **Clear Chain of Command**: Each agent knows who to report to
2. **Quality Gates**: Supervisors ensure quality before escalation
3. **Separation of Concerns**: Workers focus on execution, supervisors on quality
4. **Scalability**: Can add more worker agents under each supervisor
5. **Compliance Oversight**: Compliance Agent has full visibility
6. **Error Isolation**: Issues caught at supervisor level before reaching Compliance
7. **Audit Trail**: Clear record of who approved what at each level

### Layer 5: Data Layer

**Databases** (Simplified to 2):
- **PostgreSQL** (All-in-One): 
  - Users & RBAC (users, roles, permissions)
  - Sessions (table)
  - Cache (table)
  - Rate Limits (table)
  - Task Queue (table)
  - Requirements, Reports Metadata
  - Audit Logs (table)
- **ChromaDB**: Vector embeddings + knowledge graph (via metadata)
- **Local Filesystem** (`./storage/`): Raw documents, reports, audit log files

---

## RBAC Design

### Role Hierarchy

```
System Administrator (Super Admin)
    ├── Full system access
    ├── User management
    ├── Role/Permission management
    └── System configuration

Compliance Manager
    ├── Approve workflows
    ├── View all reports
    ├── Audit trail access
    └── Quality oversight

Regulatory Business Analyst
    ├── Upload regulatory documents
    ├── Review AI-generated requirements
    ├── Edit/approve requirements
    ├── Create data mappings
    └── View gap analysis

Data Engineer / Developer
    ├── View requirements
    ├── Review generated code
    ├── Edit/test SQL/Python
    ├── Execute pipelines
    └── View lineage maps

Regulatory Reporting Analyst
    ├── Generate reports
    ├── View validation results
    ├── Download audit packs
    ├── View anomaly detection
    └── Submit to regulators

Read-Only User (Auditor/Viewer)
    ├── View reports
    ├── View audit trails
    └── Export data
```

### Permission System

```python
# Core Permissions Structure
PERMISSIONS = {
    # Document Management
    "documents.upload": "Upload regulatory documents",
    "documents.view": "View documents",
    "documents.delete": "Delete documents",
    
    # Requirements
    "requirements.view": "View requirements",
    "requirements.create": "Create requirements",
    "requirements.edit": "Edit requirements",
    "requirements.approve": "Approve requirements",
    "requirements.delete": "Delete requirements",
    
    # Development
    "code.view": "View generated code",
    "code.edit": "Edit code",
    "code.execute": "Execute pipelines",
    "code.deploy": "Deploy to production",
    
    # Reports
    "reports.view": "View reports",
    "reports.generate": "Generate reports",
    "reports.submit": "Submit to regulators",
    "reports.download": "Download reports",
    
    # Agents
    "agents.trigger": "Trigger AI agents",
    "agents.view_results": "View agent results",
    "agents.configure": "Configure agent settings",
    
    # Admin
    "users.manage": "Manage users",
    "roles.manage": "Manage roles",
    "permissions.manage": "Manage permissions",
    "system.configure": "Configure system",
    "audit.view": "View audit logs",
    
    # Workflow
    "workflow.view": "View workflows",
    "workflow.approve": "Approve workflow steps",
    "workflow.manage": "Manage workflow definitions"
}
```

---

## Frontend Architecture

### Feature-Based Structure

```
frontend/src/
├── features/
│   ├── auth/                    # Authentication
│   ├── regulatory-updates/      # Document management
│   ├── requirements/            # BA Dashboard
│   ├── development/             # Developer Dashboard
│   ├── reporting/               # Analyst Dashboard
│   ├── admin/                   # Admin Panel
│   └── workflow/                # Workflow Management
│
├── components/ui/               # shadcn/ui components
├── shared/                      # Shared utilities
└── lib/                         # Utility functions (cn helper)
```

### Key Frontend Features

#### 1. Business Analyst Dashboard
- Document upload with drag-and-drop
- AI-generated requirements viewer
- Gap analysis matrix
- Data mapping interface
- Impact assessment visualization

#### 2. Developer Dashboard
- Generated code preview (Monaco Editor)
- Interactive lineage viewer (React Flow)
- Test case manager
- Pipeline execution monitor
- Schema viewer

#### 3. Reporting Analyst Dashboard
- Report generator with templates
- Validation dashboard
- Anomaly detection viewer
- Audit pack builder
- Submission portal

---

## Backend Architecture

### FastAPI Application Structure

```python
backend/app/
├── api/v1/endpoints/          # API routes
├── core/                      # Config, security, RBAC
├── models/                    # SQLAlchemy models
├── schemas/                   # Pydantic schemas
├── services/                  # Business logic
├── agents/                    # MCP Agents
├── sub_agents/                # Specialized sub-agents
├── tools/                     # Agent tools
├── db/                        # Database connections
└── tasks/                     # Celery tasks
```

### Database Models

**PostgreSQL Tables**:
- users, roles, permissions (RBAC)
- regulatory_updates
- requirements
- data_mappings
- generated_code
- test_cases
- reports
- workflows
- audit_logs
- agent_execution_logs

---

## AI/ML Components

### ChromaDB as Unified Storage

ChromaDB serves **dual purpose** in this architecture:

#### 1. Vector Database (Traditional Use)
```python
# Semantic search for similar documents
collection.query(
    query_texts=["liquidity coverage ratio"],
    n_results=5,
    where={"document_type": "FCA"}
)
```

#### 2. Knowledge Graph Storage (Enhanced Use)
```python
# Store entity relationships using metadata
collection.add(
    documents=["Entity description"],
    metadatas=[{
        "entity_id": "req_001",
        "entity_type": "Requirement",
        "relates_to": ["field_001", "field_002"],
        "relationship_type": "REQUIRES",
        "community": "psd008_group"
    }]
)

# Query knowledge graph
results = collection.query(
    query_texts=["Find all requirements related to PSD008"],
    where={
        "$and": [
            {"entity_type": "Requirement"},
            {"community": "psd008_group"}
        ]
    },
    include=["metadatas", "documents"]
)
```

### Microsoft GraphRAG with ChromaDB

**Architecture**:
```
Microsoft GraphRAG
    ↓
Entity Extraction → Store in ChromaDB with relationship metadata
    ↓
Community Detection (NetworkX) → Update ChromaDB metadata
    ↓
Local/Global Search → Query ChromaDB with filters
```

**Implementation**:

```python
# backend/app/sub_agents/chromadb_graph_rag_agent.py
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
import networkx as nx
from typing import Dict, List, Any
import community as community_louvain

class ChromaDBGraphRAGAgent:
    """
    Unified ChromaDB agent for both vector search and knowledge graph
    
    Features:
    - Vector embeddings for semantic search
    - Metadata-based knowledge graph
    - Community detection with NetworkX
    - Local and global search patterns
    """
    
    def __init__(self):
        # Initialize ChromaDB
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
        
        self.embeddings = OpenAIEmbeddings()
        
        # Collections
        self.doc_collection = self.client.get_or_create_collection(
            name="regulatory_documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.entity_collection = self.client.get_or_create_collection(
            name="knowledge_graph",
            metadata={"hnsw:space": "cosine"}
        )
        
        # NetworkX graph for analysis
        self.nx_graph = nx.MultiDiGraph()
    
    async def index_regulatory_document(self, content: str, metadata: Dict):
        """
        Index document with entity extraction and relationship building
        
        Steps:
        1. Chunk and embed document
        2. Extract entities using LLM
        3. Build relationships
        4. Detect communities
        5. Store in ChromaDB with rich metadata
        """
        # Step 1: Chunk document
        chunks = self._chunk_document(content)
        
        # Step 2: Store document chunks
        doc_ids = [f"doc_{metadata['id']}_chunk_{i}" for i in range(len(chunks))]
        self.doc_collection.add(
            documents=chunks,
            metadatas=[metadata] * len(chunks),
            ids=doc_ids
        )
        
        # Step 3: Extract entities
        entities = await self._extract_entities(content)
        
        # Step 4: Build NetworkX graph
        for entity in entities:
            self.nx_graph.add_node(
                entity['id'],
                type=entity['type'],
                description=entity['description']
            )
        
        # Step 5: Extract relationships
        relationships = await self._extract_relationships(content, entities)
        for rel in relationships:
            self.nx_graph.add_edge(
                rel['source'],
                rel['target'],
                type=rel['type']
            )
        
        # Step 6: Community detection
        communities = self._detect_communities()
        
        # Step 7: Store entities in ChromaDB with relationship metadata
        entity_docs = [e['description'] for e in entities]
        entity_metas = [
            {
                "entity_id": e['id'],
                "entity_type": e['type'],
                "document_id": metadata['id'],
                "relates_to": [rel['target'] for rel in relationships if rel['source'] == e['id']],
                "relationship_types": [rel['type'] for rel in relationships if rel['source'] == e['id']],
                "community": communities.get(e['id'], -1),
                "centrality": self._calculate_centrality(e['id'])
            }
            for e in entities
        ]
        entity_ids = [e['id'] for e in entities]
        
        self.entity_collection.add(
            documents=entity_docs,
            metadatas=entity_metas,
            ids=entity_ids
        )
        
        return {
            "entities": len(entities),
            "relationships": len(relationships),
            "communities": len(set(communities.values()))
        }
    
    async def local_search(self, query: str, entity_id: str = None, k: int = 5) -> Dict:
        """
        Local search: Find specific entity neighborhood
        
        Uses ChromaDB metadata filtering to traverse relationships
        """
        if entity_id:
            # Find entity and its direct relationships
            entity_result = self.entity_collection.get(
                ids=[entity_id],
                include=["metadatas", "documents"]
            )
            
            if not entity_result['ids']:
                return {"error": "Entity not found"}
            
            # Get related entities
            related_ids = entity_result['metadatas'][0].get('relates_to', [])
            
            if related_ids:
                related_results = self.entity_collection.get(
                    ids=related_ids,
                    include=["metadatas", "documents"]
                )
            else:
                related_results = {"ids": [], "documents": [], "metadatas": []}
            
            return {
                "entity": entity_result,
                "related_entities": related_results,
                "neighborhood_size": len(related_ids)
            }
        else:
            # Semantic search first
            results = self.entity_collection.query(
                query_texts=[query],
                n_results=k,
                include=["metadatas", "documents", "distances"]
            )
            return results
    
    async def global_search(self, query: str, k: int = 10) -> Dict:
        """
        Global search: Query across all communities
        
        Uses community metadata for broad context retrieval
        """
        # Get all communities
        all_entities = self.entity_collection.get(
            include=["metadatas"]
        )
        
        communities = set(m.get('community', -1) for m in all_entities['metadatas'])
        communities.discard(-1)
        
        # Search each community
        community_results = {}
        for comm in communities:
            results = self.entity_collection.query(
                query_texts=[query],
                n_results=k,
                where={"community": comm},
                include=["metadatas", "documents", "distances"]
            )
            community_results[f"community_{comm}"] = results
        
        return {
            "query": query,
            "total_communities": len(communities),
            "results_by_community": community_results
        }
    
    async def semantic_search(self, query: str, k: int = 5, filters: Dict = None) -> List[Dict]:
        """
        Pure semantic search on documents
        """
        where_filter = filters if filters else None
        
        results = self.doc_collection.query(
            query_texts=[query],
            n_results=k,
            where=where_filter,
            include=["metadatas", "documents", "distances"]
        )
        
        return [
            {
                "content": doc,
                "metadata": meta,
                "score": 1 - dist  # Convert distance to similarity
            }
            for doc, meta, dist in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )
        ]
    
    async def analyze_lineage(self, entity_id: str) -> Dict:
        """
        Analyze data lineage using NetworkX
        """
        if entity_id not in self.nx_graph:
            return {"error": "Entity not found in graph"}
        
        # Find all paths from source entities
        source_nodes = [n for n, d in self.nx_graph.in_degree() if d == 0]
        
        all_paths = []
        for source in source_nodes:
            try:
                paths = list(nx.all_simple_paths(
                    self.nx_graph,
                    source,
                    entity_id,
                    cutoff=10
                ))
                all_paths.extend(paths)
            except nx.NetworkXNoPath:
                continue
        
        # Find shortest path
        shortest_path = None
        if all_paths:
            shortest_path = min(all_paths, key=len)
        
        return {
            "entity_id": entity_id,
            "all_paths_count": len(all_paths),
            "shortest_path": shortest_path,
            "max_depth": max(len(p) for p in all_paths) if all_paths else 0
        }
    
    def _detect_communities(self) -> Dict:
        """
        Detect communities using Louvain algorithm
        """
        undirected = self.nx_graph.to_undirected()
        
        if len(undirected.nodes()) == 0:
            return {}
        
        communities = community_louvain.best_partition(undirected)
        return communities
    
    def _calculate_centrality(self, entity_id: str) -> Dict:
        """
        Calculate centrality measures for entity
        """
        if entity_id not in self.nx_graph:
            return {}
        
        try:
            betweenness = nx.betweenness_centrality(self.nx_graph)
            pagerank = nx.pagerank(self.nx_graph)
            
            return {
                "betweenness": betweenness.get(entity_id, 0),
                "pagerank": pagerank.get(entity_id, 0)
            }
        except:
            return {}
    
    def _chunk_document(self, document: str, chunk_size: int = 1000) -> List[str]:
        """Split document into overlapping chunks"""
        chunks = []
        overlap = 200
        
        for i in range(0, len(document), chunk_size - overlap):
            chunk = document[i:i + chunk_size]
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    async def _extract_entities(self, content: str) -> List[Dict]:
        """Extract entities using LLM - simplified for example"""
        # In production, use proper LLM entity extraction
        # This is a placeholder
        return [
            {"id": "entity_1", "type": "Requirement", "description": "Sample requirement"},
            {"id": "entity_2", "type": "DataField", "description": "Sample data field"}
        ]
    
    async def _extract_relationships(self, content: str, entities: List[Dict]) -> List[Dict]:
        """Extract relationships between entities"""
        # In production, use LLM for relationship extraction
        return [
            {"source": "entity_1", "target": "entity_2", "type": "REQUIRES"}
        ]
```

### NetworkX Integration

```python
# backend/app/sub_agents/networkx_analyzer.py
import networkx as nx
import community as community_louvain
from typing import Dict, List

class NetworkXAnalyzer:
    """
    Advanced graph analysis using NetworkX
    
    Works with ChromaDB-stored graph data
    """
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
    
    def build_from_chromadb(self, entity_collection):
        """
        Build NetworkX graph from ChromaDB entity collection
        """
        all_entities = entity_collection.get(include=["metadatas"])
        
        # Add nodes
        for entity_id, metadata in zip(all_entities['ids'], all_entities['metadatas']):
            self.graph.add_node(
                entity_id,
                type=metadata.get('entity_type'),
                community=metadata.get('community')
            )
        
        # Add edges
        for entity_id, metadata in zip(all_entities['ids'], all_entities['metadatas']):
            related_to = metadata.get('relates_to', [])
            rel_types = metadata.get('relationship_types', [])
            
            for target, rel_type in zip(related_to, rel_types):
                if target in self.graph:
                    self.graph.add_edge(entity_id, target, type=rel_type)
    
    def detect_communities(self) -> Dict:
        """Community detection using Louvain"""
        undirected = self.graph.to_undirected()
        return community_louvain.best_partition(undirected)
    
    def calculate_importance(self) -> Dict:
        """Calculate node importance metrics"""
        return {
            "betweenness": nx.betweenness_centrality(self.graph),
            "pagerank": nx.pagerank(self.graph),
            "in_degree": dict(self.graph.in_degree()),
            "out_degree": dict(self.graph.out_degree())
        }
    
    def find_critical_paths(self, source: str, target: str) -> List:
        """Find all paths between two entities"""
        try:
            return list(nx.all_simple_paths(self.graph, source, target, cutoff=10))
        except nx.NetworkXNoPath:
            return []
```

---

## Database Design

### PostgreSQL Schema (RBAC + Core Data)

```sql
-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Roles
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Permissions
CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    resource VARCHAR(50),
    action VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- User-Role Mapping
CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, role_id)
);

-- Role-Permission Mapping
CREATE TABLE role_permissions (
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,
    granted_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (role_id, permission_id)
);

-- Regulatory Updates
CREATE TABLE regulatory_updates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    source VARCHAR(50),
    document_url TEXT,
    document_type VARCHAR(50),
    upload_date TIMESTAMP DEFAULT NOW(),
    effective_date DATE,
    status VARCHAR(50),
    uploaded_by UUID REFERENCES users(id),
    chromadb_doc_id VARCHAR(255),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Requirements
CREATE TABLE requirements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    regulatory_update_id UUID REFERENCES regulatory_updates(id),
    requirement_text TEXT NOT NULL,
    requirement_type VARCHAR(100),
    priority VARCHAR(20),
    status VARCHAR(50),
    data_fields JSONB,
    validation_rules JSONB,
    frequency VARCHAR(50),
    effective_date DATE,
    chromadb_entity_id VARCHAR(255),
    created_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Reports
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_type VARCHAR(100),
    report_period VARCHAR(50),
    status VARCHAR(50),
    file_url TEXT,
    validation_results JSONB,
    anomalies JSONB,
    generated_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    submitted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Audit Logs
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100),
    resource_type VARCHAR(50),
    resource_id UUID,
    changes JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### ChromaDB Collections Structure

```python
# Collection 1: Document Storage (Vector Search)
{
    "name": "regulatory_documents",
    "metadata": {
        "hnsw:space": "cosine"
    },
    "documents": [
        "Document text chunks..."
    ],
    "metadatas": [
        {
            "document_id": "doc_001",
            "document_type": "FCA",
            "upload_date": "2026-01-01",
            "source": "PRA",
            "chunk_index": 0
        }
    ]
}

# Collection 2: Knowledge Graph (Entity + Relationships)
{
    "name": "knowledge_graph",
    "metadata": {
        "hnsw:space": "cosine"
    },
    "documents": [
        "Entity description embeddings..."
    ],
    "metadatas": [
        {
            "entity_id": "req_001",
            "entity_type": "Requirement",
            "document_id": "doc_001",
            "relates_to": ["field_001", "field_002"],
            "relationship_types": ["REQUIRES", "REQUIRES"],
            "community": 1,
            "centrality": {
                "betweenness": 0.35,
                "pagerank": 0.12
            }
        }
    ]
}
```

---

## Local Filesystem Storage

### Why Local Filesystem?

Instead of using **MongoDB** (for documents) and **MinIO/S3** (for object storage), this architecture uses **local filesystem** for:
- Raw document storage (PDF, Word, Excel)
- Generated reports (CSV, Excel)
- Audit log files (JSONL format)
- Temporary files

**Benefits**:
- ✅ **Simpler Architecture**: No separate object storage service
- ✅ **Cost-Effective**: No cloud storage fees
- ✅ **Fast Access**: Local disk reads
- ✅ **Easy Backup**: Standard filesystem backup tools
- ✅ **Version Control**: Git-friendly for some file types

**Trade-offs**:
- ❌ Not ideal for multi-server deployments (use NFS or cloud storage if scaling)
- ❌ No built-in replication (use backup strategy)

### Directory Structure

```
./storage/
├── documents/                  # Raw regulatory documents
│   ├── fca/
│   │   ├── 2026/
│   │   │   ├── PSD008_2026-01-15.pdf
│   │   │   └── metadata.json
│   │   └── 2025/
│   ├── pra/
│   └── boe/
│
├── reports/                    # Generated reports
│   ├── submissions/
│   │   ├── 2026-01/
│   │   │   ├── LCR_2026-01-31.xlsx
│   │   │   └── metadata.json
│   │   └── 2026-02/
│   └── validation/
│       ├── anomaly_report_001.csv
│       └── variance_analysis_002.xlsx
│
├── audit_logs/                 # Daily audit log files
│   ├── 2026/
│   │   ├── 01/
│   │   │   ├── audit_2026-01-01.jsonl
│   │   │   ├── audit_2026-01-02.jsonl
│   │   │   └── ...
│   │   └── 02/
│   └── indexes/
│       └── audit_index_2026-01.db  # SQLite index for fast search
│
├── generated_code/             # Agent-generated code
│   ├── sql/
│   │   ├── requirement_001_v1.sql
│   │   └── requirement_001_v2.sql
│   └── python/
│       ├── etl_pipeline_001.py
│       └── validation_rules_002.py
│
├── graphrag/                   # Microsoft GraphRAG graphs
│   ├── graphs/                 # Serialized NetworkX graphs
│   │   ├── document_001_graph.gpickle
│   │   ├── document_001_graph.json
│   │   └── community_graph.gexf
│   ├── communities/            # Community detection results
│   │   ├── communities_2026-01.json
│   │   └── community_hierarchy.json
│   ├── entities/               # Extracted entities
│   │   ├── entities_doc_001.json
│   │   └── entity_relationships.json
│   └── analysis/               # Graph analysis results
│       ├── centrality_metrics.json
│       ├── critical_paths.json
│       └── subgraph_analysis.json
│
├── embeddings/                 # Tiktoken embeddings & caches
│   ├── vectors/                # Pre-computed embeddings
│   │   ├── doc_001_embeddings.npy
│   │   ├── doc_001_metadata.json
│   │   └── requirement_embeddings.npy
│   ├── tiktoken_cache/         # Tiktoken tokenization cache
│   │   ├── tokenizer_cache.db
│   │   └── token_counts.json
│   └── indexes/                # FAISS/HNSW indexes (backup)
│       ├── document_index.faiss
│       └── entity_index.faiss
│
├── workflows/                  # Workflow execution data
│   ├── definitions/            # Workflow templates
│   │   ├── ba_workflow.json
│   │   ├── dev_workflow.json
│   │   └── qa_workflow.json
│   ├── executions/             # Workflow runs
│   │   ├── 2026-01/
│   │   │   ├── workflow_run_001.json
│   │   │   ├── workflow_run_002.json
│   │   │   └── ...
│   │   └── 2026-02/
│   ├── state/                  # Current workflow states
│   │   ├── active_workflows.json
│   │   └── workflow_001_state.json
│   └── history/                # Historical workflow data
│       ├── completed_workflows.jsonl
│       └── failed_workflows.jsonl
│
├── backups/                    # Automated backups
│   ├── daily/
│   ├── weekly/
│   └── monthly/
│
└── temp/                       # Temporary processing files
    ├── uploads/
    └── processing/
```

### File Metadata Storage

**PostgreSQL table for file metadata**:

```sql
CREATE TABLE file_metadata (
    file_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_path VARCHAR(500) NOT NULL UNIQUE,  -- Relative path from ./storage/
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,  -- pdf, xlsx, csv, docx
    file_size BIGINT NOT NULL,       -- Bytes
    mime_type VARCHAR(100),
    category VARCHAR(50) NOT NULL,    -- document, report, audit_log, code
    subcategory VARCHAR(50),          -- fca, pra, boe, submission, validation
    uploaded_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB,                   -- Custom metadata
    checksum VARCHAR(64)              -- SHA-256 for integrity
);

-- Indexes
CREATE INDEX idx_file_metadata_category ON file_metadata(category);
CREATE INDEX idx_file_metadata_created_at ON file_metadata(created_at);
CREATE INDEX idx_file_metadata_uploaded_by ON file_metadata(uploaded_by);
```

### File Operations

#### 1. **Upload Document**

```python
import aiofiles
import hashlib
from pathlib import Path

async def upload_document(
    file: UploadFile,
    category: str,
    subcategory: str,
    user_id: UUID
) -> UUID:
    # Generate file path
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_filename = f"{timestamp}_{file.filename}"
    relative_path = f"documents/{subcategory}/{datetime.now().year}/{safe_filename}"
    full_path = Path("./storage") / relative_path
    
    # Ensure directory exists
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Calculate checksum while saving
    hasher = hashlib.sha256()
    async with aiofiles.open(full_path, 'wb') as f:
        while chunk := await file.read(8192):
            hasher.update(chunk)
            await f.write(chunk)
    
    checksum = hasher.hexdigest()
    file_size = full_path.stat().st_size
    
    # Save metadata to PostgreSQL
    file_id = await db.fetchval(
        """
        INSERT INTO file_metadata 
        (file_path, file_name, file_type, file_size, category, subcategory, 
         uploaded_by, checksum, mime_type)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        RETURNING file_id
        """,
        relative_path, file.filename, Path(file.filename).suffix[1:],
        file_size, category, subcategory, user_id, checksum, file.content_type
    )
    
    return file_id
```

#### 2. **Retrieve Document**

```python
from fastapi.responses import FileResponse

async def download_document(file_id: UUID, user: User):
    # Get metadata from PostgreSQL
    row = await db.fetchrow(
        "SELECT file_path, file_name FROM file_metadata WHERE file_id = $1",
        file_id
    )
    
    if not row:
        raise HTTPException(404, "File not found")
    
    # Check permissions (RBAC)
    if not has_permission(user, "documents.download"):
        raise HTTPException(403, "Permission denied")
    
    full_path = Path("./storage") / row['file_path']
    
    if not full_path.exists():
        raise HTTPException(404, "File not found on disk")
    
    return FileResponse(
        path=full_path,
        filename=row['file_name'],
        media_type='application/octet-stream'
    )
```

#### 3. **Audit Logging to JSONL Files**

```python
import aiofiles
import json

async def log_audit_event(event: dict):
    # Daily log file
    date_str = datetime.now().strftime("%Y-%m-%d")
    year_month = datetime.now().strftime("%Y/%m")
    log_path = Path(f"./storage/audit_logs/{year_month}/audit_{date_str}.jsonl")
    
    # Ensure directory exists
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Append to JSONL file
    async with aiofiles.open(log_path, 'a') as f:
        await f.write(json.dumps(event) + '\n')
    
    # Also store in PostgreSQL for fast queries
    await db.execute(
        """
        INSERT INTO audit_logs 
        (user_id, action, resource, details, created_at)
        VALUES ($1, $2, $3, $4, $5)
        """,
        event['user_id'], event['action'], event['resource'],
        json.dumps(event['details']), event['timestamp']
    )
```

#### 4. **Generated Report Storage**

```python
async def save_generated_report(
    report_data: pd.DataFrame,
    report_type: str,
    user_id: UUID
) -> UUID:
    # Generate file path
    year_month = datetime.now().strftime("%Y-%m")
    filename = f"{report_type}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    relative_path = f"reports/submissions/{year_month}/{filename}"
    full_path = Path("./storage") / relative_path
    
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save Excel file
    report_data.to_excel(full_path, index=False)
    
    file_size = full_path.stat().st_size
    
    # Save metadata
    file_id = await db.fetchval(
        """
        INSERT INTO file_metadata 
        (file_path, file_name, file_type, file_size, category, subcategory, uploaded_by)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING file_id
        """,
        relative_path, filename, 'xlsx', file_size, 'report', 'submission', user_id
    )
    
    return file_id
```

#### 5. **GraphRAG Graph Storage**

Microsoft GraphRAG generates knowledge graphs from documents. Store these graphs locally for fast retrieval.

```python
# backend/app/sub_agents/graphrag_storage.py
import json
import pickle
import networkx as nx
from pathlib import Path
from typing import Dict, List
import numpy as np

class GraphRAGStorage:
    """Manage GraphRAG graph storage on local filesystem"""
    
    def __init__(self, base_path: str = "./storage/graphrag"):
        self.base_path = Path(base_path)
        self.graphs_path = self.base_path / "graphs"
        self.communities_path = self.base_path / "communities"
        self.entities_path = self.base_path / "entities"
        self.analysis_path = self.base_path / "analysis"
        
        # Ensure directories exist
        for path in [self.graphs_path, self.communities_path, 
                     self.entities_path, self.analysis_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    async def save_graph(self, document_id: str, graph: nx.Graph):
        """Save NetworkX graph in multiple formats"""
        
        # 1. Pickle format (fastest, preserves all data)
        pickle_path = self.graphs_path / f"{document_id}_graph.gpickle"
        with open(pickle_path, 'wb') as f:
            pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)
        
        # 2. JSON format (human-readable, for debugging)
        json_path = self.graphs_path / f"{document_id}_graph.json"
        graph_data = nx.node_link_data(graph)
        with open(json_path, 'w') as f:
            json.dump(graph_data, f, indent=2)
        
        # 3. GEXF format (for visualization tools like Gephi)
        gexf_path = self.graphs_path / f"{document_id}_graph.gexf"
        nx.write_gexf(graph, gexf_path)
        
        return {
            "pickle": str(pickle_path),
            "json": str(json_path),
            "gexf": str(gexf_path)
        }
    
    async def load_graph(self, document_id: str) -> nx.Graph:
        """Load NetworkX graph from pickle (fastest)"""
        pickle_path = self.graphs_path / f"{document_id}_graph.gpickle"
        
        if not pickle_path.exists():
            raise FileNotFoundError(f"Graph not found: {document_id}")
        
        with open(pickle_path, 'rb') as f:
            return pickle.load(f)
    
    async def save_communities(self, document_id: str, communities: Dict):
        """Save community detection results"""
        timestamp = datetime.now().strftime("%Y-%m")
        communities_file = self.communities_path / f"communities_{timestamp}.json"
        
        # Load existing communities
        if communities_file.exists():
            with open(communities_file, 'r') as f:
                all_communities = json.load(f)
        else:
            all_communities = {}
        
        # Add new document communities
        all_communities[document_id] = {
            "timestamp": datetime.now().isoformat(),
            "communities": communities,
            "num_communities": len(set(communities.values()))
        }
        
        # Save back
        with open(communities_file, 'w') as f:
            json.dump(all_communities, f, indent=2)
    
    async def save_entities(self, document_id: str, entities: List[Dict]):
        """Save extracted entities"""
        entities_file = self.entities_path / f"entities_{document_id}.json"
        
        with open(entities_file, 'w') as f:
            json.dump({
                "document_id": document_id,
                "timestamp": datetime.now().isoformat(),
                "entities": entities,
                "count": len(entities)
            }, f, indent=2)
    
    async def save_analysis(self, document_id: str, analysis_type: str, results: Dict):
        """Save graph analysis results (centrality, paths, etc.)"""
        analysis_file = self.analysis_path / f"{analysis_type}_{document_id}.json"
        
        with open(analysis_file, 'w') as f:
            json.dump({
                "document_id": document_id,
                "analysis_type": analysis_type,
                "timestamp": datetime.now().isoformat(),
                "results": results
            }, f, indent=2)
    
    async def get_graph_stats(self) -> Dict:
        """Get statistics about stored graphs"""
        graphs = list(self.graphs_path.glob("*.gpickle"))
        
        return {
            "total_graphs": len(graphs),
            "storage_size_mb": sum(g.stat().st_size for g in graphs) / (1024**2),
            "latest_graph": max(graphs, key=lambda x: x.stat().st_mtime).name if graphs else None
        }


# Example usage in GraphRAG agent
async def process_document_with_graphrag(document_id: str, content: str):
    """Process document and store all GraphRAG outputs"""
    storage = GraphRAGStorage()
    
    # 1. Build knowledge graph using Microsoft GraphRAG
    from graphrag import build_knowledge_graph
    graph = await build_knowledge_graph(content)
    
    # 2. Save graph to filesystem
    await storage.save_graph(document_id, graph)
    
    # 3. Detect communities
    from community import community_louvain
    communities = community_louvain.best_partition(graph)
    await storage.save_communities(document_id, communities)
    
    # 4. Extract entities
    entities = [
        {
            "id": node,
            "type": graph.nodes[node].get('type'),
            "community": communities[node]
        }
        for node in graph.nodes()
    ]
    await storage.save_entities(document_id, entities)
    
    # 5. Calculate centrality
    centrality = nx.betweenness_centrality(graph)
    await storage.save_analysis(document_id, "centrality", 
                                 {node: float(score) for node, score in centrality.items()})
    
    return {
        "graph_saved": True,
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "num_communities": len(set(communities.values()))
    }
```

#### 6. **Embeddings & Tiktoken Storage**

Store pre-computed embeddings and tiktoken caches to avoid re-computation.

```python
# backend/app/services/embedding_storage.py
import json
import numpy as np
from pathlib import Path
from typing import List, Dict
import hashlib

class EmbeddingStorage:
    """Manage embeddings and tiktoken cache on local filesystem"""
    
    def __init__(self, base_path: str = "./storage/embeddings"):
        self.base_path = Path(base_path)
        self.vectors_path = self.base_path / "vectors"
        self.tiktoken_cache_path = self.base_path / "tiktoken_cache"
        self.indexes_path = self.base_path / "indexes"
        
        # Ensure directories exist
        for path in [self.vectors_path, self.tiktoken_cache_path, self.indexes_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    async def save_embeddings(
        self, 
        document_id: str, 
        embeddings: np.ndarray,
        metadata: Dict
    ):
        """Save embeddings as numpy array"""
        
        # Save embeddings
        embeddings_file = self.vectors_path / f"{document_id}_embeddings.npy"
        np.save(embeddings_file, embeddings)
        
        # Save metadata
        metadata_file = self.vectors_path / f"{document_id}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump({
                "document_id": document_id,
                "timestamp": datetime.now().isoformat(),
                "shape": embeddings.shape,
                "dtype": str(embeddings.dtype),
                "metadata": metadata
            }, f, indent=2)
        
        return {
            "embeddings_file": str(embeddings_file),
            "metadata_file": str(metadata_file),
            "size_mb": embeddings_file.stat().st_size / (1024**2)
        }
    
    async def load_embeddings(self, document_id: str) -> np.ndarray:
        """Load pre-computed embeddings"""
        embeddings_file = self.vectors_path / f"{document_id}_embeddings.npy"
        
        if not embeddings_file.exists():
            raise FileNotFoundError(f"Embeddings not found: {document_id}")
        
        return np.load(embeddings_file)
    
    async def cache_tiktoken_tokens(self, text: str, tokens: List[int], model: str):
        """Cache tiktoken tokenization results"""
        
        # Create hash of text for cache key
        text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
        
        cache_file = self.tiktoken_cache_path / "tokenizer_cache.json"
        
        # Load existing cache
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                cache = json.load(f)
        else:
            cache = {}
        
        # Add to cache
        cache[text_hash] = {
            "model": model,
            "token_count": len(tokens),
            "tokens": tokens[:100],  # Store first 100 tokens for debugging
            "timestamp": datetime.now().isoformat()
        }
        
        # Save cache (keep only last 10000 entries)
        if len(cache) > 10000:
            # Keep most recent 10000
            cache = dict(sorted(cache.items(), key=lambda x: x[1]['timestamp'])[-10000:])
        
        with open(cache_file, 'w') as f:
            json.dump(cache, f)
    
    async def get_cached_tokens(self, text: str) -> Dict:
        """Retrieve cached tokenization"""
        text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
        
        cache_file = self.tiktoken_cache_path / "tokenizer_cache.json"
        
        if not cache_file.exists():
            return None
        
        with open(cache_file, 'r') as f:
            cache = json.load(f)
        
        return cache.get(text_hash)
    
    async def save_token_counts(self, counts: Dict[str, int]):
        """Save token count statistics"""
        counts_file = self.tiktoken_cache_path / "token_counts.json"
        
        with open(counts_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "counts": counts,
                "total_tokens": sum(counts.values())
            }, f, indent=2)
    
    async def get_embedding_stats(self) -> Dict:
        """Get statistics about stored embeddings"""
        embeddings = list(self.vectors_path.glob("*_embeddings.npy"))
        
        total_size = sum(e.stat().st_size for e in embeddings)
        
        return {
            "total_embeddings": len(embeddings),
            "storage_size_mb": total_size / (1024**2),
            "avg_size_kb": (total_size / len(embeddings) / 1024) if embeddings else 0
        }


# Example usage
async def embed_document(document_id: str, chunks: List[str]):
    """Embed document chunks and cache results"""
    storage = EmbeddingStorage()
    
    # Generate embeddings using OpenAI
    from openai import AsyncOpenAI
    client = AsyncOpenAI()
    
    embeddings = []
    for chunk in chunks:
        # Check cache first
        cached = await storage.get_cached_tokens(chunk)
        if cached:
            print(f"Cache hit: {cached['token_count']} tokens")
        
        # Generate embedding
        response = await client.embeddings.create(
            model="text-embedding-ada-002",
            input=chunk
        )
        embeddings.append(response.data[0].embedding)
        
        # Cache tiktoken tokens
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode(chunk)
        await storage.cache_tiktoken_tokens(chunk, tokens, "text-embedding-ada-002")
    
    # Save all embeddings
    embeddings_array = np.array(embeddings)
    await storage.save_embeddings(document_id, embeddings_array, {
        "num_chunks": len(chunks),
        "model": "text-embedding-ada-002",
        "dimensions": 1536
    })
    
    return embeddings_array
```

#### 7. **Workflow Storage**

Store workflow definitions, execution states, and history.

```python
# backend/app/services/workflow_storage.py
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from enum import Enum

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

class WorkflowStorage:
    """Manage workflow data on local filesystem"""
    
    def __init__(self, base_path: str = "./storage/workflows"):
        self.base_path = Path(base_path)
        self.definitions_path = self.base_path / "definitions"
        self.executions_path = self.base_path / "executions"
        self.state_path = self.base_path / "state"
        self.history_path = self.base_path / "history"
        
        # Ensure directories exist
        for path in [self.definitions_path, self.executions_path, 
                     self.state_path, self.history_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    async def save_workflow_definition(self, workflow_name: str, definition: Dict):
        """Save workflow template/definition"""
        definition_file = self.definitions_path / f"{workflow_name}_workflow.json"
        
        with open(definition_file, 'w') as f:
            json.dump({
                "name": workflow_name,
                "version": definition.get("version", "1.0"),
                "created_at": datetime.now().isoformat(),
                "definition": definition
            }, f, indent=2)
    
    async def start_workflow(
        self, 
        workflow_id: str,
        workflow_name: str,
        input_data: Dict
    ) -> Dict:
        """Create new workflow execution"""
        
        year_month = datetime.now().strftime("%Y-%m")
        execution_dir = self.executions_path / year_month
        execution_dir.mkdir(parents=True, exist_ok=True)
        
        execution_file = execution_dir / f"workflow_run_{workflow_id}.json"
        
        workflow_data = {
            "workflow_id": workflow_id,
            "workflow_name": workflow_name,
            "status": WorkflowStatus.RUNNING.value,
            "input_data": input_data,
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "current_step": 1,
            "total_steps": input_data.get("total_steps", 5),
            "steps": [],
            "agents": {
                "compliance": {"status": "pending", "result": None},
                "ba_supervisor": {"status": "pending", "result": None},
                "dev_supervisor": {"status": "pending", "result": None},
                "qa_supervisor": {"status": "pending", "result": None}
            }
        }
        
        with open(execution_file, 'w') as f:
            json.dump(workflow_data, f, indent=2)
        
        # Update active workflows state
        await self._add_to_active_workflows(workflow_id, workflow_data)
        
        return workflow_data
    
    async def update_workflow_step(
        self,
        workflow_id: str,
        step_name: str,
        step_data: Dict
    ):
        """Update workflow with step completion"""
        
        # Find workflow file
        workflow_file = await self._find_workflow_file(workflow_id)
        
        if not workflow_file:
            raise FileNotFoundError(f"Workflow not found: {workflow_id}")
        
        # Load workflow
        with open(workflow_file, 'r') as f:
            workflow_data = json.load(f)
        
        # Add step
        workflow_data["steps"].append({
            "step_name": step_name,
            "timestamp": datetime.now().isoformat(),
            "data": step_data
        })
        workflow_data["current_step"] += 1
        
        # Save updated workflow
        with open(workflow_file, 'w') as f:
            json.dump(workflow_data, f, indent=2)
        
        # Update state
        await self._update_workflow_state(workflow_id, workflow_data)
    
    async def complete_workflow(
        self,
        workflow_id: str,
        status: WorkflowStatus,
        final_result: Dict
    ):
        """Mark workflow as completed"""
        
        workflow_file = await self._find_workflow_file(workflow_id)
        
        with open(workflow_file, 'r') as f:
            workflow_data = json.load(f)
        
        workflow_data["status"] = status.value
        workflow_data["completed_at"] = datetime.now().isoformat()
        workflow_data["final_result"] = final_result
        
        # Save updated workflow
        with open(workflow_file, 'w') as f:
            json.dump(workflow_data, f, indent=2)
        
        # Remove from active workflows
        await self._remove_from_active_workflows(workflow_id)
        
        # Add to history
        await self._add_to_history(workflow_data)
    
    async def get_active_workflows(self) -> List[Dict]:
        """Get all currently active workflows"""
        active_file = self.state_path / "active_workflows.json"
        
        if not active_file.exists():
            return []
        
        with open(active_file, 'r') as f:
            return json.load(f).get("workflows", [])
    
    async def _find_workflow_file(self, workflow_id: str) -> Path:
        """Find workflow file by ID"""
        for year_month_dir in self.executions_path.iterdir():
            if year_month_dir.is_dir():
                workflow_file = year_month_dir / f"workflow_run_{workflow_id}.json"
                if workflow_file.exists():
                    return workflow_file
        return None
    
    async def _add_to_active_workflows(self, workflow_id: str, workflow_data: Dict):
        """Add workflow to active list"""
        active_file = self.state_path / "active_workflows.json"
        
        if active_file.exists():
            with open(active_file, 'r') as f:
                active = json.load(f)
        else:
            active = {"workflows": []}
        
        active["workflows"].append({
            "workflow_id": workflow_id,
            "workflow_name": workflow_data["workflow_name"],
            "started_at": workflow_data["started_at"],
            "current_step": workflow_data["current_step"]
        })
        
        with open(active_file, 'w') as f:
            json.dump(active, f, indent=2)
    
    async def _remove_from_active_workflows(self, workflow_id: str):
        """Remove workflow from active list"""
        active_file = self.state_path / "active_workflows.json"
        
        with open(active_file, 'r') as f:
            active = json.load(f)
        
        active["workflows"] = [
            w for w in active["workflows"] 
            if w["workflow_id"] != workflow_id
        ]
        
        with open(active_file, 'w') as f:
            json.dump(active, f, indent=2)
    
    async def _update_workflow_state(self, workflow_id: str, workflow_data: Dict):
        """Update workflow state file"""
        state_file = self.state_path / f"workflow_{workflow_id}_state.json"
        
        with open(state_file, 'w') as f:
            json.dump({
                "workflow_id": workflow_id,
                "status": workflow_data["status"],
                "current_step": workflow_data["current_step"],
                "total_steps": workflow_data["total_steps"],
                "last_updated": datetime.now().isoformat()
            }, f, indent=2)
    
    async def _add_to_history(self, workflow_data: Dict):
        """Add completed workflow to history"""
        history_file = self.history_path / f"{workflow_data['status']}_workflows.jsonl"
        
        # Append to JSONL file
        with open(history_file, 'a') as f:
            f.write(json.dumps(workflow_data) + '\n')


# Example usage in Compliance Agent
async def orchestrate_regulatory_workflow(document_id: str):
    """Full workflow orchestration with storage"""
    workflow_storage = WorkflowStorage()
    workflow_id = str(uuid.uuid4())
    
    # Start workflow
    await workflow_storage.start_workflow(
        workflow_id=workflow_id,
        workflow_name="regulatory_document_processing",
        input_data={"document_id": document_id, "total_steps": 5}
    )
    
    try:
        # Step 1: BA Supervisor
        ba_result = await ba_supervisor.process(document_id)
        await workflow_storage.update_workflow_step(
            workflow_id, "ba_processing", ba_result
        )
        
        # Step 2: Dev Supervisor
        dev_result = await dev_supervisor.process(ba_result)
        await workflow_storage.update_workflow_step(
            workflow_id, "dev_processing", dev_result
        )
        
        # Step 3: QA Supervisor
        qa_result = await qa_supervisor.process(dev_result)
        await workflow_storage.update_workflow_step(
            workflow_id, "qa_processing", qa_result
        )
        
        # Complete workflow
        await workflow_storage.complete_workflow(
            workflow_id,
            WorkflowStatus.COMPLETED,
            {"ba": ba_result, "dev": dev_result, "qa": qa_result}
        )
        
    except Exception as e:
        await workflow_storage.complete_workflow(
            workflow_id,
            WorkflowStatus.FAILED,
            {"error": str(e)}
        )
```

### Backup Strategy

**Daily automated backup script**:

```python
import shutil
import tarfile
from datetime import datetime

async def backup_storage():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(f"./storage/backups/daily/backup_{timestamp}.tar.gz")
    
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create compressed archive (all important directories)
    with tarfile.open(backup_path, "w:gz") as tar:
        tar.add("./storage/documents", arcname="documents")
        tar.add("./storage/reports", arcname="reports")
        tar.add("./storage/audit_logs", arcname="audit_logs")
        tar.add("./storage/graphrag", arcname="graphrag")           # GraphRAG graphs
        tar.add("./storage/embeddings", arcname="embeddings")       # Embeddings & tiktoken
        tar.add("./storage/workflows", arcname="workflows")         # Workflow data
        tar.add("./storage/generated_code", arcname="generated_code")
    
    # Keep only last 7 daily backups
    backups = sorted(backup_path.parent.glob("backup_*.tar.gz"))
    for old_backup in backups[:-7]:
        old_backup.unlink()
```

**Cron job** (Linux/Mac):
```bash
# Add to crontab
0 2 * * * python /path/to/backup_script.py
```

### Storage Monitoring

```python
import shutil

async def get_storage_stats():
    storage_path = Path("./storage")
    total, used, free = shutil.disk_usage(storage_path)
    
    # Calculate directory sizes
    def get_dir_size(path: Path) -> int:
        return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
    
    directories = {
        "documents": storage_path / "documents",
        "reports": storage_path / "reports",
        "audit_logs": storage_path / "audit_logs",
        "graphrag": storage_path / "graphrag",
        "embeddings": storage_path / "embeddings",
        "workflows": storage_path / "workflows",
        "generated_code": storage_path / "generated_code",
        "backups": storage_path / "backups"
    }
    
    dir_sizes = {}
    for name, path in directories.items():
        if path.exists():
            size_bytes = get_dir_size(path)
            dir_sizes[name] = {
                "size_mb": size_bytes / (1024**2),
                "size_gb": size_bytes / (1024**3)
            }
    
    return {
        "disk": {
            "total_gb": total / (1024**3),
            "used_gb": used / (1024**3),
            "free_gb": free / (1024**3),
            "usage_percent": (used / total) * 100
        },
        "directories": dir_sizes,
        "total_application_storage_gb": sum(
            d["size_gb"] for d in dir_sizes.values()
        )
    }
```

### When to Scale to Cloud Storage

**Use local filesystem when**:
- Single-server deployment
- Storage < 500GB
- Low concurrent uploads

**Migrate to S3/MinIO when**:
- Multi-server deployment (use NFS or S3)
- Storage > 1TB
- High concurrent uploads (100+/sec)
- Need CDN distribution

---

## Application Entry Point (`app.py`)

### Single Command Startup

The entire backend runs with a single command: `python app.py`

This eliminates the need for Docker, Celery workers, or multiple terminal windows.

### Implementation

**`backend/app.py`**:
```python
#!/usr/bin/env python3
"""
Main application entry point for NTT Data Regulatory Reporting System.

Run this file to start the entire backend:
- FastAPI server
- Background cleanup scheduler
- Task queue worker
- WebSocket support

Usage:
    python app.py
"""

import asyncio
import sys
import signal
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from app.main import app
from app.tasks.cleanup_tasks import CleanupScheduler
from app.core.config import settings


class ApplicationRunner:
    """Manages all application services in a single process"""
    
    def __init__(self):
        self.cleanup_scheduler = CleanupScheduler()
        self.running = True
    
    def initialize_system(self):
        """Run initialization tasks on first startup"""
        print("🔧 Initializing system...")
        
        # 1. Setup storage directories
        print("📁 Setting up storage directories...")
        from scripts.setup_storage import setup_storage
        setup_storage()
        
        # 2. Initialize database and create tables
        print("🗄️  Initializing database...")
        try:
            from app.db.postgres import engine, Base
            from sqlalchemy import text, inspect
            
            # Test connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✅ Database connection successful")
            
            # Check if tables exist
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            if len(existing_tables) == 0:
                print("📋 No tables found. Creating database schema...")
                
                # Import all models to register them with Base
                from app.models import (
                    user, role, permission, session, cache, rate_limit,
                    task_queue, regulatory_update, requirement, data_mapping,
                    generated_code, test_case, report, workflow,
                    file_metadata, audit_log
                )
                
                # Create all tables
                Base.metadata.create_all(bind=engine)
                print(f"✅ Created {len(Base.metadata.tables)} database tables")
                
                # Run initial data seeding
                print("👤 Seeding initial data...")
                from scripts.seed_data import seed_data
                seed_data()
                print("✅ Initial data seeded successfully")
            else:
                print(f"✅ Found {len(existing_tables)} existing tables")
                
                # Check if admin user exists
                with engine.connect() as conn:
                    result = conn.execute(text("SELECT COUNT(*) FROM users"))
                    user_count = result.scalar()
                    
                    if user_count == 0:
                        print("👤 No users found. Running seed_data...")
                        from scripts.seed_data import seed_data
                        seed_data()
                        print("✅ Initial data seeded successfully")
                    else:
                        print(f"✅ Found {user_count} users in database")
                    
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            print("\n📝 Please ensure:")
            print("  1. PostgreSQL is running")
            print("  2. Database 'regulatory_reporting' exists")
            print("  3. Database user has CREATE TABLE permissions")
            sys.exit(1)
        
        # 3. Setup ChromaDB
        print("🔍 Initializing ChromaDB...")
        try:
            from app.db.chroma_db import get_chroma_client
            client = get_chroma_client()
            collections = client.list_collections()
            print(f"✅ ChromaDB initialized ({len(collections)} collections)")
        except Exception as e:
            print(f"⚠️  ChromaDB warning: {e}")
        
        print("✅ System initialization complete!\n")
        
    async def start_background_services(self):
        """Start all background services"""
        print("🚀 Starting background services...")
        
        # Start cleanup scheduler
        asyncio.create_task(self.cleanup_scheduler.run_cleanup_loop())
        print("✅ Cleanup scheduler started")
        
        # Start task queue worker
        from app.tasks.agent_execution import TaskQueueWorker
        self.task_worker = TaskQueueWorker()
        asyncio.create_task(self.task_worker.run())
        print("✅ Task queue worker started")
        
    def setup_signal_handlers(self):
        """Setup graceful shutdown"""
        def signal_handler(sig, frame):
            print("\n⚠️  Shutting down gracefully...")
            self.running = False
            self.cleanup_scheduler.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def run(self):
        """Run the application"""
        self.setup_signal_handlers()
        
        print("=" * 60)
        print("🏦 NTT Data Regulatory Reporting System")
        print("=" * 60)
        
        # Run initialization
        self.initialize_system()
        
        print(f"Environment: {settings.ENVIRONMENT}")
        print(f"API URL: http://{settings.HOST}:{settings.PORT}")
        print(f"API Docs: http://{settings.HOST}:{settings.PORT}/api/v1/docs")
        print(f"Storage: {settings.STORAGE_PATH}")
        print("=" * 60)
        
        # Configure uvicorn
        config = uvicorn.Config(
            app=app,
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level="info",
            access_log=True,
        )
        
        server = uvicorn.Server(config)
        
        # Start background services on startup
        @app.on_event("startup")
        async def startup_event():
            await self.start_background_services()
            print("✅ All services started successfully!")
        
        @app.on_event("shutdown")
        async def shutdown_event():
            print("⚠️  Shutting down services...")
            self.cleanup_scheduler.stop()
        
        # Run the server
        server.run()


if __name__ == "__main__":
    runner = ApplicationRunner()
    runner.run()
```

### What `app.py` Does Automatically

#### **Initialization (First Time)**

1. **Storage Setup**
   - Creates all storage directories (`./storage/`)
   - Sets up: documents/, reports/, graphrag/, embeddings/, workflows/, etc.
   - Runs automatically from `scripts/setup_storage.py`

2. **Database Check**
   - Verifies PostgreSQL connection
   - Checks if tables exist (requires `alembic upgrade head`)
   - Counts existing users

3. **Seed Data**
   - If no users found, automatically runs `scripts/seed_data.py`
   - Creates admin user and default roles/permissions
   - Sets up initial RBAC structure

4. **ChromaDB Initialization**
   - Initializes ChromaDB client
   - Creates collections if needed

#### **Services Started (Every Time)**

1. **FastAPI Server**
   - Port: 8000 (configurable via .env)
   - Auto-reload in development mode
   - API documentation at `/api/v1/docs`

2. **Background Cleanup Scheduler**
   - Runs every 1-10 minutes
   - Cleans up expired sessions, cache, rate limits
   - No PostgreSQL extensions required

3. **Task Queue Worker**
   - Processes background tasks from PostgreSQL task_queue table
   - Handles document processing, agent execution, reports
   - No Celery or RabbitMQ required

4. **WebSocket Support**
   - Real-time agent progress updates
   - Workflow status notifications
   - Built into FastAPI

### Prerequisites for Running `app.py`

**Zero manual steps!** Just run:
```bash
python app.py
```

**What happens automatically**:
- ✅ Creates all database tables (using SQLAlchemy models)
- ✅ Creates storage directories
- ✅ Seeds initial data (admin user, roles, permissions)
- ✅ Initializes ChromaDB
- ✅ Starts all services

**No Alembic migrations needed** - Tables are created directly from SQLAlchemy models!

### Configuration

**`.env` file**:
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
```

### Setup Scripts

**`backend/scripts/setup_storage.py`**:
```python
"""Create storage directory structure"""
from pathlib import Path

STORAGE_DIRS = [
    "storage/documents/fca",
    "storage/documents/pra",
    "storage/documents/boe",
    "storage/reports/submissions",
    "storage/reports/validation",
    "storage/audit_logs",
    "storage/generated_code/sql",
    "storage/generated_code/python",
    "storage/graphrag/graphs",
    "storage/graphrag/communities",
    "storage/graphrag/entities",
    "storage/graphrag/analysis",
    "storage/embeddings/vectors",
    "storage/embeddings/tiktoken_cache",
    "storage/embeddings/indexes",
    "storage/workflows/definitions",
    "storage/workflows/executions",
    "storage/workflows/state",
    "storage/workflows/history",
    "storage/backups/daily",
    "storage/backups/weekly",
    "storage/backups/monthly",
    "storage/temp/uploads",
    "storage/temp/processing",
]

def setup_storage():
    """Create all storage directories"""
    for dir_path in STORAGE_DIRS:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {dir_path}")
    
    print(f"\n✅ Storage structure created successfully!")
    print(f"Total directories: {len(STORAGE_DIRS)}")

if __name__ == "__main__":
    setup_storage()
```

### Database Migrations (Manual SQL Files)

**No Alembic** - Instead, use manual SQL migration files for schema changes.

#### Creating a Migration

When you need to modify the database schema:

1. **Update the SQLAlchemy model** in `backend/app/models/`

2. **Create a migration SQL file** in `backend/migrations/`:

**`backend/migrations/`** directory structure:
```
backend/migrations/
├── 001_initial_schema.sql         # Auto-generated on first run
├── 002_add_workflow_priority.sql   # Example migration
├── 003_add_agent_logs_table.sql   # Example migration
└── README.md                       # Migration instructions
```

3. **Migration file format**:

**`backend/migrations/002_add_workflow_priority.sql`**:
```sql
-- Migration: Add priority field to workflows table
-- Date: 2026-01-15
-- Author: Developer Name

-- Add column
ALTER TABLE workflows 
ADD COLUMN priority INTEGER DEFAULT 0;

-- Create index
CREATE INDEX idx_workflows_priority ON workflows(priority DESC);

-- Update existing records
UPDATE workflows SET priority = 0 WHERE priority IS NULL;

-- Add comment
COMMENT ON COLUMN workflows.priority IS 'Workflow priority (0=normal, 1=high, 2=critical)';
```

4. **Apply migration manually**:
```bash
# Connect to PostgreSQL
psql -U reg_user -d regulatory_reporting

# Run migration file
\i backend/migrations/002_add_workflow_priority.sql

# Verify
\d workflows
```

5. **Document in migrations/README.md**:
```markdown
# Database Migrations

## Applied Migrations
- [x] 001_initial_schema.sql (2026-01-01) - Initial database schema
- [x] 002_add_workflow_priority.sql (2026-01-15) - Add workflow priority

## Pending Migrations
- [ ] 003_add_agent_logs_table.sql

## How to Apply
1. Review the SQL file
2. Test on dev database first
3. Backup production database
4. Apply: `psql -U user -d db < migrations/XXX_name.sql`
5. Mark as applied in this README
```

#### Auto-generating Initial Schema

**`backend/scripts/generate_schema_sql.py`**:
```python
"""Generate SQL schema from SQLAlchemy models"""
from sqlalchemy.schema import CreateTable
from app.db.postgres import engine, Base
from app.models import *  # Import all models

def generate_schema():
    """Generate CREATE TABLE statements"""
    output_file = "migrations/001_initial_schema.sql"
    
    with open(output_file, 'w') as f:
        f.write("-- Initial Database Schema\n")
        f.write("-- Auto-generated from SQLAlchemy models\n")
        f.write(f"-- Date: {datetime.now().isoformat()}\n\n")
        
        for table in Base.metadata.sorted_tables:
            create_stmt = str(CreateTable(table).compile(engine))
            f.write(f"{create_stmt};\n\n")
        
        print(f"✅ Schema generated: {output_file}")

if __name__ == "__main__":
    generate_schema()
```

Run after first startup:
```bash
python scripts/generate_schema_sql.py
```

This creates `migrations/001_initial_schema.sql` as a reference.

#### Migration Best Practices

1. **Always Backward Compatible**: Don't drop columns immediately
2. **Test First**: Run on dev database before production
3. **Backup**: Always backup before migration
4. **Rollback Plan**: Include rollback SQL in comments
5. **Document**: Update migrations/README.md

#### Example Rollback

```sql
-- Migration: 002_add_workflow_priority.sql

-- Forward migration
ALTER TABLE workflows ADD COLUMN priority INTEGER DEFAULT 0;

-- Rollback (commented):
-- ALTER TABLE workflows DROP COLUMN priority;
```

### Running the Application

**Development**:
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python app.py
```

**Production**:
```bash
cd backend
source venv/bin/activate
python app.py
```

Or use a process manager like **systemd** or **supervisor**:

**systemd service** (`/etc/systemd/system/regulatory-reporting.service`):
```ini
[Unit]
Description=NTT Data Regulatory Reporting System
After=network.target postgresql.service

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/nttdata_regulatory_reporting_system/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable regulatory-reporting
sudo systemctl start regulatory-reporting
sudo systemctl status regulatory-reporting
```

### Benefits of Single Entry Point

✅ **Automatic Setup**: Runs `setup_storage.py` and `seed_data.py` automatically
✅ **Simplified Deployment**: No Docker, no Celery, no RabbitMQ
✅ **Single Command**: `python app.py` starts everything
✅ **Easy Debugging**: All logs in one place
✅ **Graceful Shutdown**: Signal handlers for clean shutdown
✅ **Resource Efficient**: Single Python process instead of multiple containers
✅ **Development Friendly**: Auto-reload in debug mode
✅ **Zero Manual Steps**: Only need to run `alembic upgrade head` once

---

## Security & Compliance

### Security Measures

1. **Authentication**: JWT tokens with refresh mechanism
2. **Authorization**: RBAC with permission-based access
3. **Data Encryption**: At rest (database) and in transit (TLS/SSL)
4. **Input Validation**: Pydantic schemas
5. **Rate Limiting**: PostgreSQL-based per user/IP tracking
6. **Audit Logging**: All user actions tracked (PostgreSQL + JSONL files)
7. **Secure File Storage**: Local filesystem with OS-level permissions and checksums

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- Infrastructure setup (PostgreSQL, ChromaDB, storage directories)
- `app.py` entry point with background services
- Core RBAC & authentication
- User management APIs and UI

### Phase 2: Document Processing & BA Agent (Weeks 5-8)
- Document upload system
- Interpreter Agent implementation
- ChromaDB document indexing
- BA dashboard (shadcn/ui)

### Phase 3: Knowledge Graph & RAG (Weeks 9-12)
- ChromaDB knowledge graph structure
- Microsoft GraphRAG integration
- NetworkX analysis tools
- Entity extraction and relationship building

### Phase 4: Developer Tools & Architect Agent (Weeks 13-16)
- Code generation (SQL/Python)
- Architect Agent implementation
- Developer dashboard
- Lineage visualization (React Flow)

### Phase 5: Reporting & Auditor Agent (Weeks 17-20)
- Report generation engine
- Auditor Agent implementation
- Validation dashboard
- Anomaly detection

### Phase 6: Workflow & Orchestration (Weeks 21-24)
- Workflow engine
- Agent orchestration
- Real-time progress tracking (WebSocket)

### Phase 7-8: Testing & Deployment (Weeks 25-30)
- Comprehensive testing
- Performance optimization
- Production deployment
- Documentation and training

---

## Benefits of ChromaDB-Only Approach

### 1. Simplified Architecture
- Single vector database instead of Neo4j + Pinecone
- Reduced infrastructure complexity
- Easier maintenance

### 2. Cost Savings
- No Neo4j licensing costs
- No Pinecone subscription
- Single database to manage

### 3. Unified Data Model
- Vectors and graph data in one place
- Consistent querying interface
- Simplified backup/restore

### 4. Performance
- ChromaDB is optimized for both use cases
- Fast HNSW indexing
- Persistent storage with DuckDB

### 5. Flexibility
- Metadata-based relationships
- Rich filtering capabilities
- Easy to extend

---

## Summary

This architecture provides:

1. **Modern UI**: shadcn/ui + Tailwind CSS
2. **Powerful AI**: Microsoft GraphRAG + ChromaDB + NetworkX
3. **Simplified Stack**: ChromaDB for both vectors and knowledge graph
4. **Complete RBAC**: 6 roles, 50+ permissions
5. **Production-Ready**: Full audit trail, security, scalability

**Key Innovation**: Using ChromaDB's metadata capabilities to store knowledge graph relationships alongside vector embeddings, eliminating the need for a separate graph database.
