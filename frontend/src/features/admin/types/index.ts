import type { User, Role, Permission } from '@/shared/types/common.types';

export interface SystemMetrics {
  total_users: number;
  active_workflows: number;
  documents_processed: number;
  reports_generated: number;
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
}

export interface AuditLog {
  id: number;
  user_id: number;
  username: string;
  action: string;
  resource_type: string;
  resource_id?: number;
  ip_address: string;
  user_agent: string;
  timestamp: string;
  details?: any;
}

export interface AgentConfig {
  id: number;
  agent_name: string;
  agent_type: string;
  is_active: boolean;
  model: string;
  temperature: number;
  max_tokens: number;
  configuration: Record<string, any>;
}

export { User, Role, Permission };
