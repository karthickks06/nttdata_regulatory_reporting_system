import { useState, useEffect } from 'react';
import { documentsApi } from '../services/documentsApi';
import type { RegulatoryDocument } from '../types';

interface DocumentViewerProps {
  documentId: number;
  onClose: () => void;
}

export function DocumentViewer({ documentId, onClose }: DocumentViewerProps) {
  const [document, setDocument] = useState<RegulatoryDocument | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'metadata' | 'content'>('metadata');

  useEffect(() => {
    loadDocument();
  }, [documentId]);

  const loadDocument = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await documentsApi.getDocument(documentId);
      setDocument(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load document');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    try {
      const blob = await documentsApi.downloadDocument(documentId);
      const url = window.URL.createObjectURL(blob);
      const a = window.document.createElement('a');
      a.href = url;
      a.download = document?.title || 'document';
      window.document.body.appendChild(a);
      a.click();
      window.document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      setError(err.message || 'Failed to download document');
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading document...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-4 border-b flex justify-between items-center">
          <h2 className="text-xl font-bold">{document?.title}</h2>
          <div className="flex gap-2">
            <button
              onClick={handleDownload}
              className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90"
            >
              Download
            </button>
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
            >
              Close
            </button>
          </div>
        </div>

        {error && (
          <div className="p-4 bg-red-100 border-b border-red-400 text-red-700">
            {error}
          </div>
        )}

        {/* Tabs */}
        <div className="border-b">
          <div className="flex">
            <button
              onClick={() => setActiveTab('metadata')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'metadata'
                  ? 'border-b-2 border-primary text-primary'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Metadata
            </button>
            <button
              onClick={() => setActiveTab('content')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'content'
                  ? 'border-b-2 border-primary text-primary'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Extracted Content
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-6">
          {activeTab === 'metadata' && document && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-600">Document ID</label>
                  <p className="mt-1 text-lg">{document.id}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-600">Type</label>
                  <p className="mt-1 text-lg">{document.document_type}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-600">Source</label>
                  <p className="mt-1 text-lg">{document.source}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-600">File Size</label>
                  <p className="mt-1 text-lg">
                    {(document.file_size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-600">Upload Date</label>
                  <p className="mt-1 text-lg">
                    {new Date(document.upload_date).toLocaleString()}
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-600">Status</label>
                  <p className="mt-1 text-lg">
                    <span
                      className={`px-2 py-1 rounded text-sm ${
                        document.processed
                          ? 'bg-green-100 text-green-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {document.processing_status}
                    </span>
                  </p>
                </div>
              </div>

              {document.metadata && (
                <div className="mt-6">
                  <label className="block text-sm font-medium text-gray-600 mb-2">
                    Additional Metadata
                  </label>
                  <pre className="bg-gray-50 p-4 rounded text-sm overflow-auto">
                    {JSON.stringify(document.metadata, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          )}

          {activeTab === 'content' && document && (
            <div>
              {document.extracted_text ? (
                <div className="prose max-w-none">
                  <div className="bg-gray-50 p-4 rounded">
                    <pre className="whitespace-pre-wrap font-sans text-sm">
                      {document.extracted_text}
                    </pre>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  {document.processed
                    ? 'No extracted text available'
                    : 'Document is still being processed'}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
