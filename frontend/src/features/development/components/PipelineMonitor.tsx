import { useState, useEffect } from 'react';
import { developmentApi } from '../services/developmentApi';
import type { PipelineExecution } from '../types';

export function PipelineMonitor() {
  const [executions, setExecutions] = useState<PipelineExecution[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadExecutions();
    const interval = setInterval(loadExecutions, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadExecutions = async () => {
    try {
      const data = await developmentApi.getPipelineExecutions();
      setExecutions(data);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'running': return 'bg-blue-100 text-blue-800';
      case 'failed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Pipeline Monitor</h1>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="flex justify-center p-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : (
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Pipeline</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Start Time</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Duration</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Records</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {executions.map((exec) => (
                <tr key={exec.id}>
                  <td className="px-6 py-4 text-sm font-medium">{exec.pipeline_name}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${getStatusColor(exec.status)}`}>
                      {exec.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm">{new Date(exec.start_time).toLocaleString()}</td>
                  <td className="px-6 py-4 text-sm">{exec.duration_seconds ? `${exec.duration_seconds}s` : '-'}</td>
                  <td className="px-6 py-4 text-sm">{exec.records_processed?.toLocaleString() || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
