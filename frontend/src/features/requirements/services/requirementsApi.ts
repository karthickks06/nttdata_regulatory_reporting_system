import { apiClient, handleApiError } from '@/shared/utils/api';
import type { PaginatedResponse } from '@/shared/types/common.types';
import type {
  Requirement,
  DataMapping,
  GapAnalysisResult,
  ImpactMatrixItem,
  ApprovalWorkflowStep,
  RequirementFilters
} from '../types';

export const requirementsApi = {
  // Requirements
  async getRequirements(
    params: RequirementFilters & { page?: number; limit?: number }
  ): Promise<PaginatedResponse<Requirement>> {
    try {
      const response = await apiClient.get<PaginatedResponse<Requirement>>(
        '/requirements',
        { params }
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getRequirement(id: number): Promise<Requirement> {
    try {
      const response = await apiClient.get<Requirement>(`/requirements/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async createRequirement(data: Partial<Requirement>): Promise<Requirement> {
    try {
      const response = await apiClient.post<Requirement>('/requirements', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async updateRequirement(id: number, data: Partial<Requirement>): Promise<Requirement> {
    try {
      const response = await apiClient.put<Requirement>(`/requirements/${id}`, data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async deleteRequirement(id: number): Promise<void> {
    try {
      await apiClient.delete(`/requirements/${id}`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Data Mappings
  async getDataMappings(requirementId: number): Promise<DataMapping[]> {
    try {
      const response = await apiClient.get<DataMapping[]>(
        `/requirements/${requirementId}/mappings`
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async createDataMapping(data: Partial<DataMapping>): Promise<DataMapping> {
    try {
      const response = await apiClient.post<DataMapping>('/data-mappings', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async updateDataMapping(id: number, data: Partial<DataMapping>): Promise<DataMapping> {
    try {
      const response = await apiClient.put<DataMapping>(`/data-mappings/${id}`, data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Gap Analysis
  async performGapAnalysis(requirementId: number): Promise<GapAnalysisResult> {
    try {
      const response = await apiClient.post<GapAnalysisResult>(
        `/requirements/${requirementId}/gap-analysis`
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Impact Matrix
  async getImpactMatrix(): Promise<ImpactMatrixItem[]> {
    try {
      const response = await apiClient.get<ImpactMatrixItem[]>('/requirements/impact-matrix');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Approval Workflow
  async getApprovalWorkflow(requirementId: number): Promise<ApprovalWorkflowStep[]> {
    try {
      const response = await apiClient.get<ApprovalWorkflowStep[]>(
        `/requirements/${requirementId}/workflow`
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async approveRequirement(
    requirementId: number,
    stepId: number,
    comments?: string
  ): Promise<void> {
    try {
      await apiClient.post(`/requirements/${requirementId}/workflow/${stepId}/approve`, {
        comments
      });
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async rejectRequirement(
    requirementId: number,
    stepId: number,
    comments: string
  ): Promise<void> {
    try {
      await apiClient.post(`/requirements/${requirementId}/workflow/${stepId}/reject`, {
        comments
      });
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
};
