import { useState, useEffect } from 'react';
import { documentsApi } from '../services/documentsApi';
import { DocumentViewer } from './DocumentViewer';
import type { RegulatoryDocument, DocumentFilters } from '../types';
import type { PaginatedResponse } from '@/shared/types/common.types';

export function DocumentList() {
  const [documents, setDocuments] = useState<PaginatedResponse<RegulatoryDocument>>({
    items: [],
    total: 0,
    page: 1,
    limit: 10,
    pages: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [selectedDocument, setSelectedDocument] = useState<number | null>(null);
  const [filters, setFilters] = useState<DocumentFilters>({});
  const [page, setPage] = useState(1);

  useEffect(() => {
    loadDocuments();
  }, [page, filters]);

  const loadDocuments = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await documentsApi.getDocuments({ ...filters, page, limit: 10 });
      setDocuments(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load documents');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this document?')) {
      return;
    }

    try {
      await documentsApi.deleteDocument(id);
      loadDocuments();
    } catch (err: any) {
      setError(err.message || 'Failed to delete document');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
      case 'extracting_text':
      case 'analyzing_content':
      case 'building_graph':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Regulatory Documents</h1>
        <a
          href="/regulatory-updates/upload"
          className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90"
        >
          Upload Document
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
            placeholder="Search documents..."
            value={filters.search || ''}
            onChange={(e) => setFilters({ ...filters, search: e.target.value })}
            className="px-4 py-2 border rounded focus:ring-2 focus:ring-primary focus:border-transparent"
          />

          <select
            value={filters.document_type || ''}
            onChange={(e) =>
              setFilters({ ...filters, document_type: e.target.value || undefined })
            }
            className="px-4 py-2 border rounded focus:ring-2 focus:ring-primary focus:border-transparent"
          >
            <option value="">All Types</option>
            <option value="FCA">FCA</option>
            <option value="PRA">PRA</option>
            <option value="BOE">BOE</option>
            <option value="Other">Other</option>
          </select>

          <select
            value={filters.source || ''}
            onChange={(e) =>
              setFilters({ ...filters, source: e.target.value || undefined })
            }
            className="px-4 py-2 border rounded focus:ring-2 focus:ring-primary focus:border-transparent"
          >
            <option value="">All Sources</option>
            <option value="Email">Email</option>
            <option value="Web Portal">Web Portal</option>
            <option value="Manual Upload">Manual Upload</option>
            <option value="API">API</option>
          </select>

          <select
            value={filters.processed === undefined ? '' : filters.processed.toString()}
            onChange={(e) =>
              setFilters({
                ...filters,
                processed: e.target.value ? e.target.value === 'true' : undefined
              })
            }
            className="px-4 py-2 border rounded focus:ring-2 focus:ring-primary focus:border-transparent"
          >
            <option value="">All Status</option>
            <option value="true">Processed</option>
            <option value="false">Processing</option>
          </select>
        </div>
      </div>

      {/* Documents Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : documents.items.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            No documents found
          </div>
        ) : (
          <>
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Title
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Source
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Upload Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {documents.items.map((doc) => (
                  <tr key={doc.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{doc.title}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">{doc.document_type}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">{doc.source}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(
                          doc.processing_status
                        )}`}
                      >
                        {doc.processing_status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(doc.upload_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        onClick={() => setSelectedDocument(doc.id)}
                        className="text-primary hover:text-primary/90 mr-4"
                      >
                        View
                      </button>
                      <button
                        onClick={() => handleDelete(doc.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Pagination */}
            <div className="bg-gray-50 px-6 py-3 flex items-center justify-between border-t border-gray-200">
              <div className="text-sm text-gray-700">
                Showing {(page - 1) * documents.limit + 1} to{' '}
                {Math.min(page * documents.limit, documents.total)} of {documents.total} results
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setPage(page - 1)}
                  disabled={page === 1}
                  className="px-4 py-2 border rounded text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
                >
                  Previous
                </button>
                <button
                  onClick={() => setPage(page + 1)}
                  disabled={page >= documents.pages}
                  className="px-4 py-2 border rounded text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
                >
                  Next
                </button>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Document Viewer Modal */}
      {selectedDocument && (
        <DocumentViewer
          documentId={selectedDocument}
          onClose={() => setSelectedDocument(null)}
        />
      )}
    </div>
  );
}
