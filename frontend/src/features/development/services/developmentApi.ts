import { apiClient, handleApiError } from '@/shared/utils/api';
import type {
  GeneratedCode,
  TestCase,
  DataLineage,
  PipelineExecution,
  SchemaDefinition
} from '../types';

export const developmentApi = {
  async getGeneratedCode(params?: any): Promise<GeneratedCode[]> {
    try {
      const response = await apiClient.get<GeneratedCode[]>('/development/code', { params });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getCodeById(id: number): Promise<GeneratedCode> {
    try {
      const response = await apiClient.get<GeneratedCode>(`/development/code/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async generateCode(data: { requirement_id: number; code_type: string }): Promise<GeneratedCode> {
    try {
      const response = await apiClient.post<GeneratedCode>('/development/generate', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getTestCases(codeId: number): Promise<TestCase[]> {
    try {
      const response = await apiClient.get<TestCase[]>(`/development/code/${codeId}/tests`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async runTests(codeId: number): Promise<TestCase[]> {
    try {
      const response = await apiClient.post<TestCase[]>(`/development/code/${codeId}/run-tests`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getDataLineage(params?: any): Promise<DataLineage[]> {
    try {
      const response = await apiClient.get<DataLineage[]>('/development/lineage', { params });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getPipelineExecutions(): Promise<PipelineExecution[]> {
    try {
      const response = await apiClient.get<PipelineExecution[]>('/development/pipelines');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async getSchema(tableName?: string): Promise<SchemaDefinition[]> {
    try {
      const response = await apiClient.get<SchemaDefinition[]>('/development/schema', {
        params: { table_name: tableName }
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
};
