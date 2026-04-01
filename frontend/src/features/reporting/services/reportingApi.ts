import { apiClient, handleApiError } from '@/shared/utils/api';
import type { Report, ValidationResult, Anomaly, Variance, AuditPackage } from '../types';

export const reportingApi = {
  async getReports(params?: any): Promise<Report[]> {
    try {
      const response = await apiClient.get<Report[]>('/reports', { params });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getReport(id: number): Promise<Report> {
    try {
      const response = await apiClient.get<Report>(`/reports/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async generateReport(data: Partial<Report>): Promise<Report> {
    try {
      const response = await apiClient.post<Report>('/reports/generate', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async validateReport(reportId: number): Promise<ValidationResult[]> {
    try {
      const response = await apiClient.post<ValidationResult[]>(`/reports/${reportId}/validate`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getAnomalies(reportId: number): Promise<Anomaly[]> {
    try {
      const response = await apiClient.get<Anomaly[]>(`/reports/${reportId}/anomalies`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getVariances(reportId: number): Promise<Variance[]> {
    try {
      const response = await apiClient.get<Variance[]>(`/reports/${reportId}/variances`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async buildAuditPack(reportId: number): Promise<AuditPackage> {
    try {
      const response = await apiClient.post<AuditPackage>(`/reports/${reportId}/audit-pack`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async submitReport(reportId: number): Promise<void> {
    try {
      await apiClient.post(`/reports/${reportId}/submit`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
};
