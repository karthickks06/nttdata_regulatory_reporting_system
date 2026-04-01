export interface Agent {
  id: number;
  name: string;
  agent_type: 'compliance' | 'supervisor' | 'worker';
  level: number;
  status: 'idle' | 'running' | 'paused' | 'error';
  current_task?: string;
  last_execution?: string;
  success_rate: number;
  total_executions: number;
}

export interface AgentExecution {
  id: number;
  agent_id: number;
  agent_name: string;
  task_name: string;
  status: 'running' | 'completed' | 'failed';
  start_time: string;
  end_time?: string;
  duration_seconds?: number;
  result?: any;
  error_message?: string;
  logs: AgentLog[];
}

export interface AgentLog {
  id: number;
  execution_id: number;
  level: 'info' | 'warning' | 'error' | 'debug';
  message: string;
  timestamp: string;
  details?: any;
}

export interface AgentProgress {
  agent_id: number;
  agent_name: string;
  current_step: string;
  progress_percentage: number;
  estimated_completion?: string;
}
