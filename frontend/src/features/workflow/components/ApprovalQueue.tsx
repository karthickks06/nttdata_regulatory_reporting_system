import { useState, useEffect } from 'react';
import { workflowApi } from '../services/workflowApi';
import type { ApprovalQueueItem } from '../types';

export function ApprovalQueue() {
  const [items, setItems] = useState<ApprovalQueueItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    loadQueue();
  }, []);

  const loadQueue = async () => {
    try {
      const data = await workflowApi.getApprovalQueue();
      setItems(data);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id: number) => {
    setActionLoading(true);
    try {
      await workflowApi.approveItem(id);
      loadQueue();
    } finally {
      setActionLoading(false);
    }
  };

  const handleReject = async (id: number) => {
    const reason = prompt('Please provide a reason for rejection:');
    if (!reason) return;
    setActionLoading(true);
    try {
      await workflowApi.rejectItem(id, reason);
      loadQueue();
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Approval Queue</h1>
      {loading ? (
        <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>
      ) : items.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center text-gray-500">No items pending approval</div>
      ) : (
        <div className="space-y-4">
          {items.map((item) => (
            <div key={item.id} className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold mb-2">{item.item_title}</h3>
                  <div className="grid grid-cols-2 gap-2 text-sm text-gray-600">
                    <div>Workflow: {item.workflow_name}</div>
                    <div>Requester: {item.requester}</div>
                    <div>Type: {item.item_type}</div>
                    <div>Priority: <span className={`px-2 py-0.5 rounded text-xs ${item.priority === 'high' || item.priority === 'critical' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>{item.priority}</span></div>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => handleApprove(item.id)} disabled={actionLoading} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50">Approve</button>
                  <button onClick={() => handleReject(item.id)} disabled={actionLoading} className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 disabled:opacity-50">Reject</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
