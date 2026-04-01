#!/bin/bash

echo "=== MISSING BACKEND FILES CHECK ==="
echo ""

# Agent config files
echo "Agent Config:"
[ -f "backend/app/agents/config/prompts.py" ] && echo "  ✓ prompts.py" || echo "  ✗ prompts.py MISSING"
[ -f "backend/app/agents/config/settings.py" ] && echo "  ✓ settings.py" || echo "  ✗ settings.py MISSING"

echo ""
echo "Backend Tasks:"
[ -f "backend/app/tasks/document_processing.py" ] && echo "  ✓ document_processing.py" || echo "  ✗ document_processing.py MISSING"
[ -f "backend/app/tasks/report_generation.py" ] && echo "  ✓ report_generation.py" || echo "  ✗ report_generation.py MISSING"
[ -f "backend/app/tasks/notification.py" ] && echo "  ✓ notification.py" || echo "  ✗ notification.py MISSING"

echo ""
echo "Database:"
[ -f "backend/app/db/base.py" ] && echo "  ✓ base.py" || echo "  ✗ base.py MISSING"

echo ""
echo "Scripts:"
[ -f "backend/scripts/init_db.py" ] && echo "  ✓ init_db.py" || echo "  ✗ init_db.py MISSING"
[ -f "backend/scripts/create_admin.py" ] && echo "  ✓ create_admin.py" || echo "  ✗ create_admin.py MISSING"

echo ""
echo "Migrations:"
[ -f "backend/migrations/001_initial_schema.sql" ] && echo "  ✓ 001_initial_schema.sql" || echo "  ✗ 001_initial_schema.sql MISSING"

echo ""
echo "=== MISSING FRONTEND FILES CHECK ==="
echo ""

# Check shadcn/ui components
echo "shadcn/ui Components:"
for comp in button card dialog input label select table tabs form toast dropdown-menu badge alert sheet separator scroll-area skeleton; do
  [ -f "frontend/src/components/ui/${comp}.tsx" ] && echo "  ✓ ${comp}.tsx" || echo "  ✗ ${comp}.tsx MISSING"
done

echo ""
echo "Public folder:"
[ -d "frontend/public" ] && echo "  ✓ public/ exists" || echo "  ✗ public/ MISSING"
[ -d "frontend/public/assets" ] && echo "  ✓ public/assets/ exists" || echo "  ✗ public/assets/ MISSING"

echo ""
echo "Assets folders:"
[ -d "frontend/src/assets/images" ] && echo "  ✓ assets/images/" || echo "  ✗ assets/images/ MISSING"
[ -d "frontend/src/assets/icons" ] && echo "  ✓ assets/icons/" || echo "  ✗ assets/icons/ MISSING"
[ -d "frontend/src/assets/styles" ] && echo "  ✓ assets/styles/" || echo "  ✗ assets/styles/ MISSING"

echo ""
echo "Styles:"
[ -f "frontend/src/styles/globals.css" ] && echo "  ✓ globals.css" || echo "  ✗ globals.css MISSING"

