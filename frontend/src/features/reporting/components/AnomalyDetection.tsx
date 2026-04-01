import { useState, useEffect } from 'react';
import { reportingApi } from '../services/reportingApi';
import type { Anomaly } from '../types';

interface AnomalyDetectionProps {
  reportId: number;
}

export function AnomalyDetection({ reportId }: AnomalyDetectionProps) {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnomalies();
  }, [reportId]);

  const loadAnomalies = async () => {
    try {
      const data = await reportingApi.getAnomalies(reportId);
      setAnomalies(data);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-500 text-white';
      case 'high': return 'bg-orange-500 text-white';
      case 'medium': return 'bg-yellow-500 text-white';
      case 'low': return 'bg-green-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-xl font-bold mb-4">Anomaly Detection</h3>
      {loading ? (
        <div className="flex justify-center p-8"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div></div>
      ) : anomalies.length === 0 ? (
        <p className="text-center text-gray-500 py-8">No anomalies detected</p>
      ) : (
        <div className="space-y-4">
          {anomalies.map((anomaly) => (
            <div key={anomaly.id} className="border rounded-lg p-4">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-semibold">{anomaly.anomaly_type}</h4>
                <span className={`px-3 py-1 rounded text-xs font-semibold ${getSeverityColor(anomaly.severity)}`}>
                  {anomaly.severity.toUpperCase()}
                </span>
              </div>
              <p className="text-sm text-gray-700 mb-2">{anomaly.description}</p>
              <div className="text-xs text-gray-500">
                Affected fields: {anomaly.affected_fields.join(', ')}
              </div>
              {anomaly.recommendation && (
                <div className="mt-2 p-2 bg-blue-50 text-blue-700 rounded text-sm">
                  <strong>Recommendation:</strong> {anomaly.recommendation}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
