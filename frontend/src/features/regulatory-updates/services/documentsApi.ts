import { apiClient, handleApiError } from '@/shared/utils/api';
import type { PaginatedResponse } from '@/shared/types/common.types';
import type {
  RegulatoryDocument,
  DocumentUploadRequest,
  DocumentUploadResponse,
  ProcessingStatusResponse,
  DocumentFilters
} from '../types';

export const documentsApi = {
  async uploadDocument(data: DocumentUploadRequest): Promise<DocumentUploadResponse> {
    try {
      const formData = new FormData();
      formData.append('file', data.file);
      formData.append('document_type', data.document_type);
      formData.append('source', data.source);
      if (data.title) {
        formData.append('title', data.title);
      }

      const response = await apiClient.post<DocumentUploadResponse>(
        '/regulatory-updates/upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getDocuments(
    params: DocumentFilters & { page?: number; limit?: number }
  ): Promise<PaginatedResponse<RegulatoryDocument>> {
    try {
      const response = await apiClient.get<PaginatedResponse<RegulatoryDocument>>(
        '/regulatory-updates',
        { params }
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getDocument(id: number): Promise<RegulatoryDocument> {
    try {
      const response = await apiClient.get<RegulatoryDocument>(
        `/regulatory-updates/${id}`
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getProcessingStatus(documentId: number): Promise<ProcessingStatusResponse> {
    try {
      const response = await apiClient.get<ProcessingStatusResponse>(
        `/regulatory-updates/${documentId}/status`
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async deleteDocument(id: number): Promise<void> {
    try {
      await apiClient.delete(`/regulatory-updates/${id}`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async downloadDocument(id: number): Promise<Blob> {
    try {
      const response = await apiClient.get(`/regulatory-updates/${id}/download`, {
        responseType: 'blob',
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async reprocessDocument(id: number): Promise<void> {
    try {
      await apiClient.post(`/regulatory-updates/${id}/reprocess`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
};
