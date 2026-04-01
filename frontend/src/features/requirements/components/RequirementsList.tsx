import { useState, useEffect } from 'react';
import { requirementsApi } from '../services/requirementsApi';
import type { Requirement, RequirementFilters } from '../types';
import type { PaginatedResponse } from '@/shared/types/common.types';

export function RequirementsList() {
  const [requirements, setRequirements] = useState<PaginatedResponse<Requirement>>({
    items: [],
    total: 0,
    page: 1,
    limit: 10,
    pages: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [filters, setFilters] = useState<RequirementFilters>({});
  const [page, setPage] = useState(1);

  useEffect(() => {
    loadRequirements();
  }, [page, filters]);

  const loadRequirements = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await requirementsApi.getRequirements({ ...filters, page, limit: 10 });
      setRequirements(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load requirements');
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'bg-red-100 text-red-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved': return 'bg-green-100 text-green-800';
      case 'under_review': return 'bg-yellow-100 text-yellow-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      case 'implemented': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Requirements</h1>
        <a
          href="/requirements/new"
          className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90"
        >
          Create Requirement
        </a>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input
            type="text"
            placeholder="Search requirements..."
            value={filters.search || ''}
            onChange={(e) => setFilters({ ...filters, search: e.target.value })}
            className="px-4 py-2 border rounded focus:ring-2 focus:ring-primary"
          />
          <select
            value={filters.status || ''}
            onChange={(e) => setFilters({ ...filters, status: e.target.value || undefined })}
            className="px-4 py-2 border rounded focus:ring-2 focus:ring-primary"
          >
            <option value="">All Status</option>
            <option value="draft">Draft</option>
            <option value="under_review">Under Review</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
            <option value="implemented">Implemented</option>
          </select>
          <select
            value={filters.priority || ''}
            onChange={(e) => setFilters({ ...filters, priority: e.target.value || undefined })}
            className="px-4 py-2 border rounded focus:ring-2 focus:ring-primary"
          >
            <option value="">All Priorities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
      </div>

      {/* Requirements Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : requirements.items.length === 0 ? (
          <div className="text-center py-12 text-gray-500">No requirements found</div>
        ) : (
          <>
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Priority</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Due Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {requirements.items.map((req) => (
                  <tr key={req.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900">{req.title}</div>
                      <div className="text-sm text-gray-500">{req.description?.substring(0, 50)}...</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{req.requirement_type}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getPriorityColor(req.priority)}`}>
                        {req.priority}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(req.status)}`}>
                        {req.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {req.due_date ? new Date(req.due_date).toLocaleDateString() : 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <a href={`/requirements/${req.id}`} className="text-primary hover:text-primary/90 mr-4">Edit</a>
                      <a href={`/requirements/${req.id}/workflow`} className="text-blue-600 hover:text-blue-900">Workflow</a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Pagination */}
            <div className="bg-gray-50 px-6 py-3 flex items-center justify-between border-t">
              <div className="text-sm text-gray-700">
                Showing {(page - 1) * requirements.limit + 1} to {Math.min(page * requirements.limit, requirements.total)} of {requirements.total} results
              </div>
              <div className="flex gap-2">
                <button onClick={() => setPage(page - 1)} disabled={page === 1} className="px-4 py-2 border rounded text-sm font-medium disabled:opacity-50 hover:bg-gray-100">Previous</button>
                <button onClick={() => setPage(page + 1)} disabled={page >= requirements.pages} className="px-4 py-2 border rounded text-sm font-medium disabled:opacity-50 hover:bg-gray-100">Next</button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
