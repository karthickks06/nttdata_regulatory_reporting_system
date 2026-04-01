import { useState } from 'react';
import { requirementsApi } from '../services/requirementsApi';
import type { GapAnalysisResult } from '../types';

interface GapAnalysisProps {
  requirementId: number;
}

export function GapAnalysis({ requirementId }: GapAnalysisProps) {
  const [result, setResult] = useState<GapAnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const performAnalysis = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await requirementsApi.performGapAnalysis(requirementId);
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Failed to perform gap analysis');
    } finally {
      setLoading(false);
    }
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-200';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-xl font-bold mb-4">Gap Analysis</h3>
      {error && <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>}
      {!result ? (
        <div className="text-center py-8">
          <p className="text-gray-600 mb-4">Click below to perform gap analysis for this requirement</p>
          <button onClick={performAnalysis} disabled={loading} className="px-6 py-2 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50">
            {loading ? 'Analyzing...' : 'Perform Gap Analysis'}
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          <div className={`p-4 rounded border ${getImpactColor(result.impact)}`}>
            <h4 className="font-semibold mb-2">Impact Level: {result.impact.toUpperCase()}</h4>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Current State</h4>
            <p className="text-gray-700 bg-gray-50 p-3 rounded">{result.current_state}</p>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Target State</h4>
            <p className="text-gray-700 bg-gray-50 p-3 rounded">{result.target_state}</p>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Gap Description</h4>
            <p className="text-gray-700 bg-gray-50 p-3 rounded">{result.gap_description}</p>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Remediation Effort</h4>
            <p className="text-gray-700 bg-gray-50 p-3 rounded">{result.remediation_effort}</p>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Recommended Actions</h4>
            <ul className="list-disc list-inside space-y-1 bg-gray-50 p-3 rounded">
              {result.recommended_actions.map((action, idx) => (
                <li key={idx} className="text-gray-700">{action}</li>
              ))}
            </ul>
          </div>
          <button onClick={performAnalysis} disabled={loading} className="px-6 py-2 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50">
            Re-run Analysis
          </button>
        </div>
      )}
    </div>
  );
}
