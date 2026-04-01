export interface Requirement {
  id: number;
  title: string;
  description: string;
  requirement_type: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'draft' | 'under_review' | 'approved' | 'rejected' | 'implemented';
  source_document_id?: number;
  regulatory_reference?: string;
  impact_assessment?: string;
  implementation_notes?: string;
  created_by: number;
  assigned_to?: number;
  due_date?: string;
  created_at: string;
  updated_at: string;
}

export interface DataMapping {
  id: number;
  requirement_id: number;
  source_system: string;
  source_field: string;
  target_field: string;
  transformation_logic?: string;
  validation_rules?: string;
  status: 'pending' | 'mapped' | 'validated' | 'approved';
  created_at: string;
  updated_at: string;
}

export interface GapAnalysisResult {
  requirement_id: number;
  requirement_title: string;
  current_state: string;
  target_state: string;
  gap_description: string;
  impact: 'low' | 'medium' | 'high' | 'critical';
  remediation_effort: string;
  recommended_actions: string[];
}

export interface ImpactMatrixItem {
  requirement_id: number;
  requirement_title: string;
  systems_affected: string[];
  data_fields_impacted: number;
  estimated_effort_hours: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  dependencies: number[];
}

export interface ApprovalWorkflowStep {
  id: number;
  requirement_id: number;
  step_name: string;
  approver_id: number;
  approver_name: string;
  status: 'pending' | 'approved' | 'rejected' | 'cancelled';
  comments?: string;
  approved_at?: string;
}

export interface RequirementFilters {
  status?: string;
  priority?: string;
  requirement_type?: string;
  assigned_to?: number;
  search?: string;
}
