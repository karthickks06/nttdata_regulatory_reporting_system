export interface RegulatoryDocument {
  id: number;
  title: string;
  document_type: string;
  source: string;
  file_path: string;
  file_size: number;
  upload_date: string;
  processed: boolean;
  processing_status: ProcessingStatus;
  extracted_text?: string;
  metadata?: Record<string, any>;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export type ProcessingStatus =
  | 'pending'
  | 'processing'
  | 'completed'
  | 'failed'
  | 'extracting_text'
  | 'analyzing_content'
  | 'building_graph';

export interface DocumentUploadRequest {
  file: File;
  document_type: string;
  source: string;
  title?: string;
}

export interface DocumentUploadResponse {
  document_id: number;
  message: string;
  processing_started: boolean;
}

export interface ProcessingStatusResponse {
  document_id: number;
  status: ProcessingStatus;
  progress: number;
  current_step?: string;
  error_message?: string;
  completed_at?: string;
}

export interface DocumentFilters {
  document_type?: string;
  source?: string;
  processed?: boolean;
  date_from?: string;
  date_to?: string;
  search?: string;
}
