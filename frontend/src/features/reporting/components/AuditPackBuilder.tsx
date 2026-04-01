import { useState } from 'react';
import { reportingApi } from '../services/reportingApi';

interface AuditPackBuilderProps {
  reportId: number;
}

export function AuditPackBuilder({ reportId }: AuditPackBuilderProps) {
  const [building, setBuilding] = useState(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  const handleBuild = async () => {
    setBuilding(true);
    setError('');
    setSuccess('');
    try {
      const pack = await reportingApi.buildAuditPack(reportId);
      setSuccess(`Audit pack created successfully: ${pack.file_path}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setBuilding(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-xl font-bold mb-4">Audit Pack Builder</h3>
      {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">{error}</div>}
      {success && <div className="mb-4 p-3 bg-green-100 text-green-700 rounded">{success}</div>}
      <p className="text-gray-600 mb-4">
        Build a comprehensive audit package including all supporting documentation, validation results, and evidence.
      </p>
      <button
        onClick={handleBuild}
        disabled={building}
        className="px-6 py-2 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50"
      >
        {building ? 'Building...' : 'Build Audit Pack'}
      </button>
    </div>
  );
}
