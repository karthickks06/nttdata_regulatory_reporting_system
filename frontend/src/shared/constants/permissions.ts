/**
 * Permission constants for RBAC
 */

export const PERMISSIONS = {
  // User Management
  USERS_READ: 'users.read',
  USERS_CREATE: 'users.create',
  USERS_UPDATE: 'users.update',
  USERS_DELETE: 'users.delete',

  // Regulatory Updates
  REGULATORY_UPDATES_READ: 'regulatory_updates.read',
  REGULATORY_UPDATES_CREATE: 'regulatory_updates.create',
  REGULATORY_UPDATES_UPDATE: 'regulatory_updates.update',
  REGULATORY_UPDATES_DELETE: 'regulatory_updates.delete',

  // Requirements
  REQUIREMENTS_READ: 'requirements.read',
  REQUIREMENTS_CREATE: 'requirements.create',
  REQUIREMENTS_UPDATE: 'requirements.update',
  REQUIREMENTS_DELETE: 'requirements.delete',

  // Data Mappings
  DATA_MAPPINGS_READ: 'data_mappings.read',
  DATA_MAPPINGS_CREATE: 'data_mappings.create',
  DATA_MAPPINGS_UPDATE: 'data_mappings.update',
  DATA_MAPPINGS_DELETE: 'data_mappings.delete',

  // Generated Code
  GENERATED_CODE_READ: 'generated_code.read',
  GENERATED_CODE_CREATE: 'generated_code.create',
  GENERATED_CODE_UPDATE: 'generated_code.update',
  GENERATED_CODE_DELETE: 'generated_code.delete',

  // Reports
  REPORTS_READ: 'reports.read',
  REPORTS_CREATE: 'reports.create',
  REPORTS_UPDATE: 'reports.update',
  REPORTS_DELETE: 'reports.delete',
  REPORTS_SUBMIT: 'reports.submit',
  REPORTS_APPROVE: 'reports.approve',

  // Workflows
  WORKFLOWS_READ: 'workflows.read',
  WORKFLOWS_CREATE: 'workflows.create',
  WORKFLOWS_UPDATE: 'workflows.update',
  WORKFLOWS_DELETE: 'workflows.delete',
  WORKFLOWS_EXECUTE: 'workflows.execute',

  // Audit Logs
  AUDIT_LOGS_READ: 'audit_logs.read',

  // Admin
  ADMIN_FULL_ACCESS: 'admin.full_access',
} as const;

export type Permission = typeof PERMISSIONS[keyof typeof PERMISSIONS];
