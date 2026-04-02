# API Documentation

## Overview

The NTT Data Regulatory Reporting System provides a comprehensive RESTful API organized into logical groups for easy navigation and testing.

**Base URL**: `http://localhost:8000/api/v1`  
**API Documentation**: `http://localhost:8000/api/v1/docs` (Swagger UI)  
**Alternative Docs**: `http://localhost:8000/api/v1/redoc` (ReDoc)

---

## 🚨 IMPORTANT: User Management Model

### No Public Registration

**There is NO public registration endpoint.** Users cannot self-register.

### Admin Creation Process

1. **First Admin User**: Created via API endpoint (one-time setup)
   ```bash
   POST /api/v1/admin/setup/create-admin
   ```

2. **All Other Users**: Created by admin via:
   ```bash
   POST /api/v1/users/
   ```

### Workflow

```
1. Create Admin (API) → 2. Admin Logs In → 3. Admin Creates Users → 4. Users Log In
```

---

## API Groups

The API is organized into **10 logical groups** for easy navigation in Swagger:

### 1. 🔐 Authentication
- User login/logout
- Get current user info
- **No registration endpoint**

### 2. 👥 User Management (Admin Only)
- Create, read, update, delete users
- Activate/deactivate users
- Assign roles to users
- User statistics

### 3. 🎭 Roles & Permissions (Admin Only)
- Manage roles
- Manage permissions
- Assign permissions to roles

### 4. 📋 Regulatory Updates
- Upload regulatory documents
- Process documents
- List and search updates
- View processing status

### 5. 📝 Requirements
- Extract requirements
- Gap analysis
- Requirement dependencies
- Requirement validation

### 6. 🗺️ Data Mappings
- Create source-to-target mappings
- Transformation logic
- Validation rules

### 7. 💻 Code Generation & 🔧 Development Tools
- Generate SQL/Python code
- Code validation
- Data lineage tracking
- Test case generation

### 8. 📊 Report Generation & ✅ Validation
- Generate reports
- Validate data
- Submit reports
- Quality scoring

### 9. 🔄 Workflows
- Create and execute workflows
- Monitor workflow progress
- Approve/reject workflows
- View workflow history

### 10. 🤖 AI Agents & 🕸️ Knowledge Graph
- Execute agents
- Monitor agent tasks
- Query knowledge graph
- Semantic search

### 11. ⚙️ Administration
- System health monitoring
- System metrics
- Audit logs
- **Admin user setup**

---

## Authentication

### Login Flow

1. **Login**
   ```bash
   POST /api/v1/auth/login
   Content-Type: application/json

   {
     "username": "admin",
     "password": "your-password"
   }
   ```

   Response:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```

2. **Use Token**
   ```bash
   GET /api/v1/auth/me
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

3. **Logout**
   ```bash
   POST /api/v1/auth/logout
   Authorization: Bearer <token>
   ```

### Token Details

- **Type**: JWT (JSON Web Token)
- **Expiry**: 30 minutes (configurable)
- **Header**: `Authorization: Bearer <token>`
- **Storage**: Client-side (localStorage/sessionStorage)

---

## Admin Setup (First-Time Only)

### Step 1: Create Admin User

```bash
POST http://localhost:8000/api/v1/admin/setup/create-admin
Content-Type: application/json

{
  "username": "admin",
  "email": "admin@nttdata.com",
  "password": "SecurePass123!",
  "full_name": "System Administrator"
}
```

**Response:**
```json
{
  "message": "Admin user created successfully",
  "user_id": "uuid-here",
  "username": "admin",
  "email": "admin@nttdata.com",
  "next_steps": [
    "1. Login via POST /api/v1/auth/login",
    "2. Create other users via POST /api/v1/users/",
    "3. Manage roles and permissions via /api/v1/roles/ and /api/v1/permissions/"
  ]
}
```

**Important Notes:**
- ✅ This endpoint only works when NO superuser exists
- ✅ Use this ONCE to create the first admin
- ✅ After creation, this endpoint returns 403 Forbidden
- ✅ All other users must be created via `/api/v1/users/`

### Step 2: Login as Admin

```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "SecurePass123!"
}
```

### Step 3: Create Other Users

```bash
POST http://localhost:8000/api/v1/users/
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "username": "john.doe",
  "email": "john.doe@nttdata.com",
  "password": "UserPass123!",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false
}
```

---

## User Management Endpoints

All user management endpoints require admin/superuser access.

### Create User

```bash
POST /api/v1/users/
Authorization: Bearer <admin-token>

{
  "username": "jane.smith",
  "email": "jane.smith@nttdata.com",
  "password": "Pass123!",
  "full_name": "Jane Smith"
}
```

### List Users

```bash
GET /api/v1/users/?skip=0&limit=100
Authorization: Bearer <admin-token>

# With filters
GET /api/v1/users/?is_active=true&search=john
```

### Get User by ID

```bash
GET /api/v1/users/{user_id}
Authorization: Bearer <admin-token>
```

### Update User

```bash
PUT /api/v1/users/{user_id}
Authorization: Bearer <admin-token>

{
  "email": "new.email@nttdata.com",
  "full_name": "Updated Name",
  "is_active": true
}
```

### Deactivate User (Recommended)

```bash
POST /api/v1/users/{user_id}/deactivate
Authorization: Bearer <admin-token>
```

### Activate User

```bash
POST /api/v1/users/{user_id}/activate
Authorization: Bearer <admin-token>
```

### Delete User (Hard Delete)

```bash
DELETE /api/v1/users/{user_id}
Authorization: Bearer <admin-token>
```

**Warning**: This permanently deletes the user. Consider deactivation instead.

### Assign Role to User

```bash
POST /api/v1/users/{user_id}/roles/{role_id}
Authorization: Bearer <admin-token>
```

### Remove Role from User

```bash
DELETE /api/v1/users/{user_id}/roles/{role_id}
Authorization: Bearer <admin-token>
```

### User Statistics

```bash
GET /api/v1/users/stats/summary
Authorization: Bearer <admin-token>
```

---

## Swagger UI Organization

The Swagger UI (`/api/v1/docs`) organizes endpoints into collapsible sections:

### 1. Setup Section
- **🔐 Authentication**: Login, logout, current user
- **⚙️ Administration**: Includes the `/admin/setup/create-admin` endpoint

### 2. User Management (Admin Only)
- **👥 User Management**: User CRUD operations
- **🎭 Roles & Permissions**: Role and permission management

### 3. Regulatory Compliance
- **📋 Regulatory Updates**: Document processing
- **📝 Requirements**: Requirement extraction
- **🗺️ Data Mappings**: Data mapping management

### 4. Development & Code
- **💻 Code Generation**: SQL/Python code generation
- **🔧 Development Tools**: Code management and lineage

### 5. Reporting & Quality
- **📊 Report Generation**: Report creation and management
- **✅ Validation**: Data and report validation

### 6. Automation
- **🔄 Workflows**: Workflow orchestration
- **🤖 AI Agents**: Agent execution
- **🕸️ Knowledge Graph**: GraphRAG and semantic search

### 7. Administration
- **⚙️ Administration**: System monitoring and management

---

## Testing in Swagger UI

### 1. Open Swagger UI

Navigate to: `http://localhost:8000/api/v1/docs`

### 2. Create Admin (First Time)

1. Expand **⚙️ Administration** section
2. Find `POST /api/v1/admin/setup/create-admin`
3. Click "Try it out"
4. Fill in the request body:
   ```json
   {
     "username": "admin",
     "email": "admin@nttdata.com",
     "password": "Admin123!",
     "full_name": "System Admin"
   }
   ```
5. Click "Execute"
6. Check response (should be 201 Created)

### 3. Login

1. Expand **🔐 Authentication** section
2. Find `POST /api/v1/auth/login`
3. Click "Try it out"
4. Fill in:
   ```json
   {
     "username": "admin",
     "password": "Admin123!"
   }
   ```
5. Click "Execute"
6. **Copy the `access_token`** from response

### 4. Authorize

1. Click **"Authorize"** button (top right with lock icon)
2. In the "Value" field, enter: `Bearer <paste-token-here>`
3. Click "Authorize"
4. Click "Close"

Now all endpoints will include the Authorization header!

### 5. Test Endpoints

Try creating a user:
1. Expand **👥 User Management** section
2. Find `POST /api/v1/users/`
3. Click "Try it out"
4. Fill in user data
5. Click "Execute"
6. Check response

---

## Example Workflows

### Workflow 1: Admin Creates User

```bash
# 1. Admin logs in
POST /api/v1/auth/login
{
  "username": "admin",
  "password": "Admin123!"
}

# 2. Admin creates user
POST /api/v1/users/
Authorization: Bearer <token>
{
  "username": "analyst1",
  "email": "analyst1@nttdata.com",
  "password": "Analyst123!",
  "full_name": "Regulatory Analyst"
}

# 3. Admin assigns role
POST /api/v1/users/{user_id}/roles/{analyst_role_id}
Authorization: Bearer <token>

# 4. User can now log in
POST /api/v1/auth/login
{
  "username": "analyst1",
  "password": "Analyst123!"
}
```

### Workflow 2: Process Regulatory Update

```bash
# 1. Upload document
POST /api/v1/regulatory-updates/upload
Authorization: Bearer <token>
# Upload PDF file

# 2. Extract requirements
POST /api/v1/requirements/extract
Authorization: Bearer <token>
{
  "update_id": "uuid-here"
}

# 3. Generate mappings
POST /api/v1/data-mappings/
Authorization: Bearer <token>
{
  "requirement_id": "uuid-here",
  "source_table": "transactions",
  "target_field": "report_field"
}

# 4. Generate code
POST /api/v1/code-generation/generate-sql
Authorization: Bearer <token>
{
  "mapping_ids": ["uuid1", "uuid2"]
}
```

---

## Error Responses

All endpoints return consistent error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 409 Conflict
```json
{
  "detail": "Username already exists"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Rate limiting is enabled by default:

- **Limit**: 60 requests per minute per user
- **Header**: `X-RateLimit-Remaining` shows remaining requests
- **Response**: 429 Too Many Requests when exceeded

Configure in `.env`:
```bash
RATE_LIMIT_ENABLED=True
MAX_REQUESTS_PER_MINUTE=60
```

---

## CORS Configuration

Allowed origins (configured in `main.py`):
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (React dev server)

For production, update CORS origins in `main.py`.

---

## Security Best Practices

### 1. Password Requirements
- Minimum 8 characters
- Mix of letters, numbers, symbols recommended

### 2. Token Management
- Store tokens securely (httpOnly cookies or secure storage)
- Clear tokens on logout
- Implement token refresh if needed

### 3. Permission Checks
- All endpoints check authentication
- Admin endpoints check superuser status
- RBAC enforced on all operations

### 4. Audit Logging
- All admin actions are logged
- User creation/modification logged
- Access logs available via `/api/v1/admin/audit/logs`

---

## Development vs Production

### Development
```bash
ENVIRONMENT=development
DEBUG=True
# Detailed error messages in responses
```

### Production
```bash
ENVIRONMENT=production
DEBUG=False
# Generic error messages
# Enable HTTPS
# Configure proper CORS origins
# Use strong SECRET_KEY
# Enable rate limiting
```

---

## Related Documentation

- [ENV_SETUP_GUIDE.md](ENV_SETUP_GUIDE.md) - Environment configuration
- [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md) - LLM setup
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [VALIDATION_REPORT.md](VALIDATION_REPORT.md) - System validation

---

**API Version**: 1.0.0  
**Last Updated**: 2026-04-02  
**Status**: ✅ Production Ready
