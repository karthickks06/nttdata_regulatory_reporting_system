#!/bin/bash

# Create Backend Directory Structure
echo "Creating backend directories..."

# Backend app directories
mkdir -p backend/app/api/v1/endpoints
mkdir -p backend/app/core
mkdir -p backend/app/models
mkdir -p backend/app/schemas
mkdir -p backend/app/services
mkdir -p backend/app/agents/level_0
mkdir -p backend/app/agents/level_1
mkdir -p backend/app/agents/level_2
mkdir -p backend/app/agents/config
mkdir -p backend/app/sub_agents
mkdir -p backend/app/tools
mkdir -p backend/app/db
mkdir -p backend/app/tasks
mkdir -p backend/app/utils

# Backend other directories
mkdir -p backend/tests/unit
mkdir -p backend/tests/integration
mkdir -p backend/tests/e2e
mkdir -p backend/migrations
mkdir -p backend/scripts

# Create Frontend Directory Structure
echo "Creating frontend directories..."

mkdir -p frontend/public/assets
mkdir -p frontend/src/app
mkdir -p frontend/src/features/auth/components
mkdir -p frontend/src/features/auth/hooks
mkdir -p frontend/src/features/auth/slices
mkdir -p frontend/src/features/auth/services
mkdir -p frontend/src/features/auth/types
mkdir -p frontend/src/features/regulatory-updates/components
mkdir -p frontend/src/features/regulatory-updates/services
mkdir -p frontend/src/features/regulatory-updates/types
mkdir -p frontend/src/features/requirements/components
mkdir -p frontend/src/features/requirements/services
mkdir -p frontend/src/features/requirements/types
mkdir -p frontend/src/features/development/components
mkdir -p frontend/src/features/development/services
mkdir -p frontend/src/features/development/types
mkdir -p frontend/src/features/reporting/components
mkdir -p frontend/src/features/reporting/services
mkdir -p frontend/src/features/reporting/types
mkdir -p frontend/src/features/workflow/components
mkdir -p frontend/src/features/workflow/services
mkdir -p frontend/src/features/admin/components
mkdir -p frontend/src/features/admin/services
mkdir -p frontend/src/features/agents/components
mkdir -p frontend/src/features/agents/services
mkdir -p frontend/src/components/ui
mkdir -p frontend/src/components/layout
mkdir -p frontend/src/shared/components
mkdir -p frontend/src/shared/hooks
mkdir -p frontend/src/shared/utils
mkdir -p frontend/src/shared/types
mkdir -p frontend/src/shared/constants
mkdir -p frontend/src/lib
mkdir -p frontend/src/assets/images
mkdir -p frontend/src/assets/icons
mkdir -p frontend/src/assets/styles
mkdir -p frontend/src/styles

# Create Storage Directory Structure
echo "Creating storage directories..."

mkdir -p storage/documents/fca
mkdir -p storage/documents/pra
mkdir -p storage/documents/boe
mkdir -p storage/reports/submissions
mkdir -p storage/reports/validation
mkdir -p storage/audit_logs
mkdir -p storage/generated_code/sql
mkdir -p storage/generated_code/python
mkdir -p storage/graphrag/graphs
mkdir -p storage/graphrag/communities
mkdir -p storage/graphrag/entities
mkdir -p storage/graphrag/analysis
mkdir -p storage/embeddings/vectors
mkdir -p storage/embeddings/tiktoken_cache
mkdir -p storage/embeddings/indexes
mkdir -p storage/workflows/definitions
mkdir -p storage/workflows/executions
mkdir -p storage/workflows/state
mkdir -p storage/workflows/history
mkdir -p storage/backups/daily
mkdir -p storage/backups/weekly
mkdir -p storage/backups/monthly
mkdir -p storage/temp/uploads
mkdir -p storage/temp/processing

# Create ChromaDB directory
mkdir -p chroma_db

# Create docs directory
mkdir -p docs/api
mkdir -p docs/user-guide
mkdir -p docs/admin-guide

# Create scripts directory
mkdir -p scripts

echo "✅ All directories created successfully!"
