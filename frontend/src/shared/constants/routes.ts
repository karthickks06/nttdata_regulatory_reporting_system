/**
 * Application route constants
 */

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  PROFILE: '/profile',

  // Regulatory Updates
  REGULATORY_UPDATES: '/regulatory-updates',
  REGULATORY_UPDATE_DETAIL: '/regulatory-updates/:id',
  REGULATORY_UPDATE_UPLOAD: '/regulatory-updates/upload',

  // Requirements
  REQUIREMENTS: '/requirements',
  REQUIREMENT_DETAIL: '/requirements/:id',
  REQUIREMENT_CREATE: '/requirements/create',
  GAP_ANALYSIS: '/requirements/gap-analysis',
  DATA_MAPPING: '/requirements/data-mapping',

  // Development
  DEVELOPMENT: '/development',
  CODE_PREVIEW: '/development/code/:id',
  SQL_EDITOR: '/development/sql-editor',
  PYTHON_EDITOR: '/development/python-editor',
  LINEAGE_VIEWER: '/development/lineage',

  // Reporting
  REPORTING: '/reporting',
  REPORT_DETAIL: '/reporting/:id',
  REPORT_GENERATOR: '/reporting/generator',
  VALIDATION_DASHBOARD: '/reporting/validation',

  // Workflow
  WORKFLOW: '/workflow',
  WORKFLOW_DESIGNER: '/workflow/designer',
  APPROVAL_QUEUE: '/workflow/approvals',
  WORKFLOW_HISTORY: '/workflow/history',

  // Agents
  AGENTS: '/agents',
  AGENT_DASHBOARD: '/agents/dashboard',
  AGENT_DETAIL: '/agents/:id',

  // Admin
  ADMIN: '/admin',
  USER_MANAGEMENT: '/admin/users',
  ROLE_PERMISSIONS: '/admin/roles',
  SYSTEM_MONITORING: '/admin/monitoring',
  AUDIT_LOGS: '/admin/audit-logs',
  AGENT_CONFIGURATION: '/admin/agent-config',
} as const;

export type RouteKey = keyof typeof ROUTES;
export type RouteValue = typeof ROUTES[RouteKey];
