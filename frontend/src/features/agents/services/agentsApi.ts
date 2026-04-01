import { apiClient, handleApiError } from '@/shared/utils/api';
import type { Agent, AgentExecution, AgentProgress } from '../types';

export const agentsApi = {
  async getAgents(): Promise<Agent[]> {
    try {
      const response = await apiClient.get<Agent[]>('/agents');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getAgent(id: number): Promise<Agent> {
    try {
      const response = await apiClient.get<Agent>(`/agents/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getAgentExecutions(agentId?: number): Promise<AgentExecution[]> {
    try {
      const response = await apiClient.get<AgentExecution[]>('/agents/executions', {
        params: { agent_id: agentId }
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getAgentProgress(): Promise<AgentProgress[]> {
    try {
      const response = await apiClient.get<AgentProgress[]>('/agents/progress');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async triggerAgent(agentId: number, taskData: any): Promise<AgentExecution> {
    try {
      const response = await apiClient.post<AgentExecution>(`/agents/${agentId}/trigger`, taskData);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async pauseAgent(agentId: number): Promise<void> {
    try {
      await apiClient.post(`/agents/${agentId}/pause`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async resumeAgent(agentId: number): Promise<void> {
    try {
      await apiClient.post(`/agents/${agentId}/resume`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
};
