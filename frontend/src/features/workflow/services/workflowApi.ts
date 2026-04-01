import { apiClient, handleApiError } from '@/shared/utils/api';
import type { Workflow, WorkflowStep, ApprovalQueueItem } from '../types';

export const workflowApi = {
  async getWorkflows(params?: any): Promise<Workflow[]> {
    try {
      const response = await apiClient.get<Workflow[]>('/workflow', { params });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getWorkflow(id: number): Promise<Workflow> {
    try {
      const response = await apiClient.get<Workflow>(`/workflow/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getWorkflowSteps(workflowId: number): Promise<WorkflowStep[]> {
    try {
      const response = await apiClient.get<WorkflowStep[]>(`/workflow/${workflowId}/steps`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getApprovalQueue(): Promise<ApprovalQueueItem[]> {
    try {
      const response = await apiClient.get<ApprovalQueueItem[]>('/workflow/approval-queue');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async approveItem(itemId: number, comments?: string): Promise<void> {
    try {
      await apiClient.post(`/workflow/approval-queue/${itemId}/approve`, { comments });
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async rejectItem(itemId: number, reason: string): Promise<void> {
    try {
      await apiClient.post(`/workflow/approval-queue/${itemId}/reject`, { reason });
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
};
