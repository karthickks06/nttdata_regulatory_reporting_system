#!/usr/bin/env python3
"""Check ALL missing files from PROJECT_STRUCTURE.md"""

from pathlib import Path

# Backend files to check
backend_files = [
    "backend/app/api/v1/endpoints/auth.py",
    "backend/app/api/v1/endpoints/users.py",
    "backend/app/api/v1/endpoints/roles.py",
    "backend/app/api/v1/endpoints/permissions.py",
    "backend/app/api/v1/endpoints/regulatory_updates.py",
    "backend/app/api/v1/endpoints/requirements.py",
    "backend/app/api/v1/endpoints/data_mappings.py",
    "backend/app/api/v1/endpoints/development.py",
    "backend/app/api/v1/endpoints/code_generation.py",
    "backend/app/api/v1/endpoints/reports.py",
    "backend/app/api/v1/endpoints/validation.py",
    "backend/app/api/v1/endpoints/workflow.py",
    "backend/app/api/v1/endpoints/agents.py",
    "backend/app/api/v1/endpoints/knowledge_graph.py",
    "backend/app/api/v1/endpoints/admin.py",
]

# Frontend files to check
frontend_files = [
    "frontend/src/features/auth/components/LoginForm.tsx",
    "frontend/src/features/regulatory-updates/components/DocumentUpload.tsx",
    "frontend/src/features/requirements/components/RequirementsList.tsx",
    "frontend/src/features/development/components/CodePreview.tsx",
    "frontend/src/features/reporting/components/ReportGenerator.tsx",
    "frontend/src/features/workflow/components/WorkflowDesigner.tsx",
    "frontend/src/features/admin/components/UserManagement.tsx",
    "frontend/src/features/agents/components/AgentDashboard.tsx",
    "frontend/src/components/ui/button.tsx",
    "frontend/src/components/layout/Header.tsx",
]

print("Checking files...")
backend_missing = [f for f in backend_files if not Path(f).exists()]
frontend_missing = [f for f in frontend_files if not Path(f).exists()]

print(f"\nBackend: {len(backend_files) - len(backend_missing)}/{len(backend_files)} exist")
print(f"Frontend: {len(frontend_files) - len(frontend_missing)}/{len(frontend_files)} exist")

if backend_missing:
    print(f"\nMISSING BACKEND ({len(backend_missing)}):")
    for f in backend_missing:
        print(f"  - {f}")

if frontend_missing:
    print(f"\nMISSING FRONTEND ({len(frontend_missing)}):")
    for f in frontend_missing:
        print(f"  - {f}")
