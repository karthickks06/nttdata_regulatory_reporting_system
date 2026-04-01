import { useState, useEffect } from 'react';
import { documentsApi } from '../services/documentsApi';
import type { ProcessingStatusResponse } from '../types';

interface ProcessingStatusProps {
  documentId: number;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

export function ProcessingStatus({
  documentId,
  autoRefresh = true,
  refreshInterval = 2000
}: ProcessingStatusProps) {
  const [status, setStatus] = useState<ProcessingStatusResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadStatus();

    if (autoRefresh) {
      const interval = setInterval(() => {
        loadStatus();
      }, refreshInterval);

      return () => clearInterval(interval);
    }
  }, [documentId, autoRefresh, refreshInterval]);

  const loadStatus = async () => {
    try {
      const data = await documentsApi.getProcessingStatus(documentId);
      setStatus(data);
      setError('');

      // Stop auto-refresh if completed or failed
      if (data.status === 'completed' || data.status === 'failed') {
        setLoading(false);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load status');
      setLoading(false);
    }
  };

  const getStatusColor = (statusValue: string) => {
    switch (statusValue) {
      case 'completed':
        return 'bg-green-500';
      case 'processing':
      case 'extracting_text':
      case 'analyzing_content':
      case 'building_graph':
        return 'bg-yellow-500';
      case 'failed':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusIcon = (statusValue: string) => {
    switch (statusValue) {
      case 'completed':
        return (
          <svg className="w-6 h-6 text-green-500" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clipRule="evenodd"
            />
          </svg>
        );
      case 'failed':
        return (
          <svg className="w-6 h-6 text-red-500" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clipRule="evenodd"
            />
          </svg>
        );
      default:
        return (
          <svg
            className="animate-spin h-6 w-6 text-yellow-500"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        );
    }
  };

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-red-600">{error}</div>
      </div>
    );
  }

  if (!status) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="animate-pulse flex space-x-4">
          <div className="flex-1 space-y-4 py-1">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="space-y-2">
              <div className="h-4 bg-gray-200 rounded"></div>
              <div className="h-4 bg-gray-200 rounded w-5/6"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Processing Status</h3>
        {getStatusIcon(status.status)}
      </div>

      <div className="space-y-4">
        {/* Status */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Status</span>
            <span className="text-sm font-medium capitalize">{status.status}</span>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className={`h-2.5 rounded-full ${getStatusColor(status.status)} transition-all duration-300`}
              style={{ width: `${status.progress}%` }}
            />
          </div>
          <div className="text-xs text-gray-500 text-right mt-1">
            {status.progress}%
          </div>
        </div>

        {/* Current Step */}
        {status.current_step && (
          <div>
            <span className="text-sm font-medium text-gray-700">Current Step</span>
            <p className="text-sm text-gray-600 mt-1">{status.current_step}</p>
          </div>
        )}

        {/* Error Message */}
        {status.error_message && (
          <div className="bg-red-50 border border-red-200 rounded p-3">
            <span className="text-sm font-medium text-red-800">Error</span>
            <p className="text-sm text-red-600 mt-1">{status.error_message}</p>
          </div>
        )}

        {/* Completed Time */}
        {status.completed_at && (
          <div>
            <span className="text-sm font-medium text-gray-700">Completed At</span>
            <p className="text-sm text-gray-600 mt-1">
              {new Date(status.completed_at).toLocaleString()}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
