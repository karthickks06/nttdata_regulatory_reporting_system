import { useState, useEffect } from 'react';
import { adminApi } from '../services/adminApi';
import type { SystemMetrics } from '../types';

export function SystemMonitoring() {
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMetrics();
    const interval = setInterval(loadMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadMetrics = async () => {
    try {
      const data = await adminApi.getSystemMetrics();
      setMetrics(data);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>;
  if (!metrics) return <div>No metrics available</div>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">System Monitoring</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-600 mb-2">Total Users</div>
          <div className="text-3xl font-bold">{metrics.total_users}</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-600 mb-2">Active Workflows</div>
          <div className="text-3xl font-bold">{metrics.active_workflows}</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-600 mb-2">Documents Processed</div>
          <div className="text-3xl font-bold">{metrics.documents_processed}</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-600 mb-2">Reports Generated</div>
          <div className="text-3xl font-bold">{metrics.reports_generated}</div>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold mb-4">CPU Usage</h3>
          <div className="relative pt-1">
            <div className="flex mb-2 items-center justify-between">
              <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-primary bg-primary/10">{metrics.cpu_usage}%</span>
            </div>
            <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-gray-200">
              <div style={{ width: `${metrics.cpu_usage}%` }} className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${metrics.cpu_usage > 80 ? 'bg-red-500' : metrics.cpu_usage > 60 ? 'bg-yellow-500' : 'bg-green-500'}`}></div>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold mb-4">Memory Usage</h3>
          <div className="relative pt-1">
            <div className="flex mb-2 items-center justify-between">
              <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-primary bg-primary/10">{metrics.memory_usage}%</span>
            </div>
            <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-gray-200">
              <div style={{ width: `${metrics.memory_usage}%` }} className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${metrics.memory_usage > 80 ? 'bg-red-500' : metrics.memory_usage > 60 ? 'bg-yellow-500' : 'bg-green-500'}`}></div>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold mb-4">Disk Usage</h3>
          <div className="relative pt-1">
            <div className="flex mb-2 items-center justify-between">
              <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-primary bg-primary/10">{metrics.disk_usage}%</span>
            </div>
            <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-gray-200">
              <div style={{ width: `${metrics.disk_usage}%` }} className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${metrics.disk_usage > 80 ? 'bg-red-500' : metrics.disk_usage > 60 ? 'bg-yellow-500' : 'bg-green-500'}`}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
