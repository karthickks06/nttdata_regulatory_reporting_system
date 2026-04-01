import { useState, useEffect } from 'react';
import { workflowApi } from '../services/workflowApi';
import type { Workflow } from '../types';

export function WorkflowHistory() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await workflowApi.getWorkflows({ status: 'completed' });
      setWorkflows(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Workflow History</h1>
      {loading ? (
        <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Completed</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {workflows.map((wf) => (
                <tr key={wf.id}>
                  <td className="px-6 py-4 text-sm font-medium">{wf.name}</td>
                  <td className="px-6 py-4 text-sm">{wf.workflow_type}</td>
                  <td className="px-6 py-4"><span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">{wf.status}</span></td>
                  <td className="px-6 py-4 text-sm">{wf.completed_at ? new Date(wf.completed_at).toLocaleString() : 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
