import { useState, useEffect } from 'react';
import { reportingApi } from '../services/reportingApi';
import type { ValidationResult } from '../types';

interface ValidationDashboardProps {
  reportId: number;
}

export function ValidationDashboard({ reportId }: ValidationDashboardProps) {
  const [results, setResults] = useState<ValidationResult[]>([]);
  const [loading, setLoading] = useState(false);

  const handleValidate = async () => {
    setLoading(true);
    try {
      const data = await reportingApi.validateReport(reportId);
      setResults(data);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'passed': return 'bg-green-100 text-green-800';
      case 'warning': return 'bg-yellow-100 text-yellow-800';
      case 'failed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold">Validation Dashboard</h3>
        <button onClick={handleValidate} disabled={loading} className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50">
          {loading ? 'Validating...' : 'Run Validation'}
        </button>
      </div>
      {results.length === 0 ? (
        <p className="text-center text-gray-500 py-8">No validation results yet</p>
      ) : (
        <div className="space-y-3">
          {results.map((result) => (
            <div key={result.id} className="border rounded-lg p-4">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-semibold">{result.validation_type}</h4>
                  <p className="text-sm text-gray-600 mt-1">{result.message}</p>
                </div>
                <span className={`px-2 py-1 rounded text-xs font-semibold ${getStatusColor(result.status)}`}>
                  {result.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
