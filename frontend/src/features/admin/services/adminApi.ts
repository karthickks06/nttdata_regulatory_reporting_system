import { apiClient, handleApiError } from '@/shared/utils/api';
import type { User, Role, Permission, SystemMetrics, AuditLog, AgentConfig } from '../types';

export const adminApi = {
  async getUsers(): Promise<User[]> {
    try {
      const response = await apiClient.get<User[]>('/admin/users');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async createUser(data: Partial<User>): Promise<User> {
    try {
      const response = await apiClient.post<User>('/admin/users', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async updateUser(id: number, data: Partial<User>): Promise<User> {
    try {
      const response = await apiClient.put<User>(`/admin/users/${id}`, data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async deleteUser(id: number): Promise<void> {
    try {
      await apiClient.delete(`/admin/users/${id}`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getRoles(): Promise<Role[]> {
    try {
      const response = await apiClient.get<Role[]>('/admin/roles');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getPermissions(): Promise<Permission[]> {
    try {
      const response = await apiClient.get<Permission[]>('/admin/permissions');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async updateRolePermissions(roleId: number, permissionIds: number[]): Promise<void> {
    try {
      await apiClient.put(`/admin/roles/${roleId}/permissions`, { permission_ids: permissionIds });
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getSystemMetrics(): Promise<SystemMetrics> {
    try {
      const response = await apiClient.get<SystemMetrics>('/admin/metrics');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getAuditLogs(params?: any): Promise<AuditLog[]> {
    try {
      const response = await apiClient.get<AuditLog[]>('/admin/audit-logs', { params });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getAgentConfigs(): Promise<AgentConfig[]> {
    try {
      const response = await apiClient.get<AgentConfig[]>('/admin/agents');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async updateAgentConfig(id: number, data: Partial<AgentConfig>): Promise<AgentConfig> {
    try {
      const response = await apiClient.put<AgentConfig>(`/admin/agents/${id}`, data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
};
