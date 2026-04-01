import { useState, useEffect } from 'react';
import { requirementsApi } from '../services/requirementsApi';
import type { ImpactMatrixItem } from '../types';

export function ImpactMatrix() {
  const [items, setItems] = useState<ImpactMatrixItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadMatrix();
  }, []);

  const loadMatrix = async () => {
    setLoading(true);
    try {
      const data = await requirementsApi.getImpactMatrix();
      setItems(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'critical': return 'bg-red-500 text-white';
      case 'high': return 'bg-orange-500 text-white';
      case 'medium': return 'bg-yellow-500 text-white';
      case 'low': return 'bg-green-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Impact Matrix</h1>
      {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">{error}</div>}
      {loading ? (
        <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Requirement</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Systems Affected</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Data Fields</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Effort (hrs)</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk Level</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {items.map((item) => (
                <tr key={item.requirement_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4"><div className="text-sm font-medium text-gray-900">{item.requirement_title}</div></td>
                  <td className="px-6 py-4"><div className="text-sm text-gray-500">{item.systems_affected.join(', ')}</div></td>
                  <td className="px-6 py-4 text-sm text-gray-500">{item.data_fields_impacted}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{item.estimated_effort_hours}</td>
                  <td className="px-6 py-4"><span className={`px-3 py-1 rounded text-xs font-semibold ${getRiskColor(item.risk_level)}`}>{item.risk_level.toUpperCase()}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
