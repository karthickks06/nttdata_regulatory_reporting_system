# API Documentation

## Overview

The NTT Data Regulatory Reporting System provides a comprehensive RESTful API built with FastAPI.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API endpoints (except `/auth/login` and `/auth/register`) require JWT authentication.

### Getting a Token

```bash
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

Response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Using the Token

Include the token in the Authorization header:

```
Authorization: Bearer eyJ...
```

## API Endpoints

### Authentication (`/auth`)

- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout user
- `GET /auth/me` - Get current user

### Users (`/users`)

- `GET /users` - List users
- `GET /users/{user_id}` - Get user
- `POST /users` - Create user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Roles (`/roles`)

- `GET /roles` - List roles
- `GET /roles/{role_id}` - Get role
- `POST /roles` - Create role
- `PUT /roles/{role_id}` - Update role
- `DELETE /roles/{role_id}` - Delete role

### Permissions (`/permissions`)

- `GET /permissions` - List permissions
- `GET /permissions/{permission_id}` - Get permission
- `POST /permissions` - Create permission

### Regulatory Updates (`/regulatory-updates`)

- `GET /regulatory-updates` - List updates
- `GET /regulatory-updates/{update_id}` - Get update
- `POST /regulatory-updates` - Upload document
- `PUT /regulatory-updates/{update_id}` - Update
- `DELETE /regulatory-updates/{update_id}` - Delete update

### Requirements (`/requirements`)

- `GET /requirements` - List requirements
- `GET /requirements/{requirement_id}` - Get requirement
- `POST /requirements` - Create requirement
- `PUT /requirements/{requirement_id}` - Update requirement
- `DELETE /requirements/{requirement_id}` - Delete requirement
- `POST /requirements/{requirement_id}/approve` - Approve requirement

### Data Mappings (`/data-mappings`)

- `GET /data-mappings` - List mappings
- `GET /data-mappings/{mapping_id}` - Get mapping
- `POST /data-mappings` - Create mapping
- `PUT /data-mappings/{mapping_id}` - Update mapping
- `DELETE /data-mappings/{mapping_id}` - Delete mapping

### Development (`/development`)

- `POST /development/code/generate` - Generate code
- `GET /development/code/{code_id}` - Get code
- `PUT /development/code/{code_id}` - Update code
- `DELETE /development/code/{code_id}` - Delete code
- `POST /development/code/{code_id}/validate` - Validate code
- `POST /development/tests/generate` - Generate tests
- `POST /development/tests/{test_id}/execute` - Execute test
- `GET /development/lineage/{entity_type}/{entity_id}` - Get lineage

### Reports (`/reports`)

- `GET /reports` - List reports
- `GET /reports/{report_id}` - Get report
- `POST /reports` - Create report
- `PUT /reports/{report_id}` - Update report
- `DELETE /reports/{report_id}` - Delete report
- `POST /reports/{report_id}/validate` - Validate report
- `POST /reports/{report_id}/submit` - Submit report

### Validation (`/validation`)

- `POST /validation/validate/report/{report_id}` - Validate report
- `POST /validation/validate/data-mapping/{mapping_id}` - Validate mapping
- `POST /validation/validate/code/{code_id}` - Validate code
- `POST /validation/validate/data-quality` - Check data quality
- `POST /validation/validate/anomaly-detection` - Detect anomalies

### Workflows (`/workflows`)

- `GET /workflows` - List workflows
- `GET /workflows/{workflow_id}` - Get workflow
- `POST /workflows` - Create workflow
- `PUT /workflows/{workflow_id}` - Update workflow
- `POST /workflows/{workflow_id}/start` - Start workflow
- `POST /workflows/{workflow_id}/cancel` - Cancel workflow

### Agents (`/agents`)

- `GET /agents` - List agents
- `GET /agents/{agent_id}` - Get agent
- `POST /agents/{agent_id}/execute` - Execute agent task
- `GET /agents/{agent_id}/logs` - Get agent logs

### Knowledge Graph (`/knowledge-graph`)

- `POST /knowledge-graph/search` - Search knowledge graph
- `POST /knowledge-graph/entities/add` - Add entity
- `POST /knowledge-graph/relationships/add` - Add relationship
- `GET /knowledge-graph/entities/{entity_id}` - Get entity
- `GET /knowledge-graph/graph/communities` - Get communities
- `GET /knowledge-graph/graph/centrality` - Calculate centrality

### Admin (`/admin`)

- `GET /admin/system/health` - System health
- `GET /admin/system/metrics` - System metrics
- `GET /admin/audit/logs` - Audit logs
- `GET /admin/audit/statistics` - Audit statistics
- `POST /admin/audit/cleanup` - Cleanup old logs
- `POST /admin/workflows/cleanup` - Cleanup workflows
- `GET /admin/cache/stats` - Cache statistics
- `POST /admin/cache/clear` - Clear cache

## Interactive Documentation

Visit `http://localhost:8000/api/v1/docs` for interactive Swagger UI documentation.

Visit `http://localhost:8000/api/v1/redoc` for ReDoc documentation.

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Rate Limiting

API requests are rate limited to prevent abuse. Limits vary by endpoint and user role.

## Pagination

List endpoints support pagination:

```
GET /endpoint?skip=0&limit=100
```

## Filtering

Many endpoints support filtering via query parameters:

```
GET /regulatory-updates?source=FCA&status=completed
```

## WebSocket

Real-time updates available via WebSocket:

```
ws://localhost:8000/ws
```
