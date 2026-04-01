export interface GeneratedCode {
  id: number;
  requirement_id?: number;
  code_type: 'SQL' | 'Python' | 'Other';
  code_content: string;
  file_path?: string;
  description?: string;
  status: 'generated' | 'reviewed' | 'approved' | 'deployed';
  test_results?: any;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface TestCase {
  id: number;
  code_id: number;
  test_name: string;
  test_type: 'unit' | 'integration' | 'e2e';
  test_input: string;
  expected_output: string;
  actual_output?: string;
  status: 'pending' | 'passed' | 'failed';
  error_message?: string;
  executed_at?: string;
}

export interface DataLineage {
  id: number;
  source_table: string;
  source_column: string;
  target_table: string;
  target_column: string;
  transformation: string;
  lineage_path: string[];
}

export interface PipelineExecution {
  id: number;
  pipeline_name: string;
  status: 'running' | 'completed' | 'failed' | 'cancelled';
  start_time: string;
  end_time?: string;
  duration_seconds?: number;
  records_processed?: number;
  error_message?: string;
}

export interface SchemaDefinition {
  table_name: string;
  columns: SchemaColumn[];
  primary_keys: string[];
  foreign_keys: ForeignKey[];
}

export interface SchemaColumn {
  name: string;
  data_type: string;
  nullable: boolean;
  default_value?: string;
  description?: string;
}

export interface ForeignKey {
  column: string;
  referenced_table: string;
  referenced_column: string;
}
