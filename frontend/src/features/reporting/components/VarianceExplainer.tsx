import { useState, useEffect } from 'react';
import { reportingApi } from '../services/reportingApi';
import type { Variance } from '../types';

interface VarianceExplainerProps {
  reportId: number;
}

export function VarianceExplainer({ reportId }: VarianceExplainerProps) {
  const [variances, setVariances] = useState<Variance[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadVariances();
  }, [reportId]);

  const loadVariances = async () => {
    try {
      const data = await reportingApi.getVariances(reportId);
      setVariances(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-xl font-bold mb-4">Variance Analysis</h3>
      {loading ? (
        <div className="flex justify-center p-8"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div></div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Metric</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Expected</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Actual</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Variance</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Explanation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {variances.map((variance, idx) => (
                <tr key={idx}>
                  <td className="px-4 py-2 text-sm font-medium">{variance.metric}</td>
                  <td className="px-4 py-2 text-sm">{variance.expected_value.toLocaleString()}</td>
                  <td className="px-4 py-2 text-sm">{variance.actual_value.toLocaleString()}</td>
                  <td className="px-4 py-2 text-sm">
                    <span className={`px-2 py-1 rounded ${Math.abs(variance.variance_percentage) > 10 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                      {variance.variance_percentage.toFixed(2)}%
                    </span>
                  </td>
                  <td className="px-4 py-2 text-sm text-gray-600">{variance.explanation || 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
