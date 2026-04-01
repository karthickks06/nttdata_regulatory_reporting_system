import { useState, useEffect } from 'react';
import { adminApi } from '../services/adminApi';
import type { AuditLog } from '../types';

export function AuditLogs() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    loadLogs();
  }, [filter]);

  const loadLogs = async () => {
    try {
      const data = await adminApi.getAuditLogs({ action: filter });
      setLogs(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Audit Logs</h1>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-4 border-b">
          <input
            type="text"
            placeholder="Filter by action..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-4 py-2 border rounded focus:ring-2 focus:ring-primary"
          />
        </div>
        {loading ? (
          <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>
        ) : (
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Resource</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">IP Address</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {logs.map((log) => (
                <tr key={log.id}>
                  <td className="px-6 py-4 text-sm">{log.username}</td>
                  <td className="px-6 py-4 text-sm font-medium">{log.action}</td>
                  <td className="px-6 py-4 text-sm">{log.resource_type}</td>
                  <td className="px-6 py-4 text-sm font-mono">{log.ip_address}</td>
                  <td className="px-6 py-4 text-sm">{new Date(log.timestamp).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
