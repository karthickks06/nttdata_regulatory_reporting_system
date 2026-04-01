export interface Workflow {
  id: number;
  name: string;
  description?: string;
  workflow_type: string;
  status: 'active' | 'paused' | 'completed' | 'failed';
  current_step?: string;
  progress_percentage: number;
  created_by: number;
  created_at: string;
  updated_at: string;
  completed_at?: string;
}

export interface WorkflowStep {
  id: number;
  workflow_id: number;
  step_name: string;
  step_type: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'skipped';
  assigned_to?: number;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
}

export interface ApprovalQueueItem {
  id: number;
  workflow_id: number;
  workflow_name: string;
  item_type: string;
  item_title: string;
  requester: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'pending' | 'approved' | 'rejected';
  created_at: string;
  due_date?: string;
}
