-- Migration: Add priority and SLA tracking to workflows
-- Date: 2026-04-01
-- Description: Adds priority field and SLA tracking capabilities to workflows table

-- Add priority column to workflows
ALTER TABLE workflows
ADD COLUMN IF NOT EXISTS priority INTEGER DEFAULT 0;

-- Add SLA-related columns
ALTER TABLE workflows
ADD COLUMN IF NOT EXISTS sla_deadline TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS sla_breached BOOLEAN DEFAULT FALSE;

-- Add execution time tracking
ALTER TABLE workflows
ADD COLUMN IF NOT EXISTS execution_time_seconds NUMERIC;

-- Create index for priority-based queries
CREATE INDEX IF NOT EXISTS idx_workflows_priority ON workflows(priority DESC);

-- Create index for SLA monitoring
CREATE INDEX IF NOT EXISTS idx_workflows_sla_deadline ON workflows(sla_deadline) WHERE sla_breached = FALSE;

-- Comment on changes
COMMENT ON COLUMN workflows.priority IS 'Workflow priority (0=low, 1=medium, 2=high, 3=critical)';
COMMENT ON COLUMN workflows.sla_deadline IS 'Service Level Agreement deadline for workflow completion';
COMMENT ON COLUMN workflows.sla_breached IS 'Flag indicating if SLA deadline was breached';
COMMENT ON COLUMN workflows.execution_time_seconds IS 'Total execution time in seconds';
