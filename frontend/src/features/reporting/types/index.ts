export interface Report {
  id: number;
  title: string;
  report_type: string;
  status: 'draft' | 'generated' | 'validated' | 'submitted';
  file_path?: string;
  generation_date: string;
  submission_date?: string;
  created_by: number;
  created_at: string;
}

export interface ValidationResult {
  id: number;
  report_id: number;
  validation_type: string;
  status: 'passed' | 'failed' | 'warning';
  message: string;
  details?: any;
  validated_at: string;
}

export interface Anomaly {
  id: number;
  report_id: number;
  anomaly_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  affected_fields: string[];
  recommendation?: string;
  detected_at: string;
}

export interface Variance {
  metric: string;
  expected_value: number;
  actual_value: number;
  variance_percentage: number;
  explanation?: string;
}

export interface AuditPackage {
  id: number;
  report_id: number;
  package_type: string;
  file_path: string;
  created_at: string;
}
