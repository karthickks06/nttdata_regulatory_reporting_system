import { useState, useEffect } from 'react';
import { requirementsApi } from '../services/requirementsApi';
import type { DataMapping as DataMappingType } from '../types';

interface DataMappingProps {
  requirementId: number;
}

export function DataMapping({ requirementId }: DataMappingProps) {
  const [mappings, setMappings] = useState<DataMappingType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    source_system: '',
    source_field: '',
    target_field: '',
    transformation_logic: '',
    validation_rules: ''
  });

  useEffect(() => {
    loadMappings();
  }, [requirementId]);

  const loadMappings = async () => {
    setLoading(true);
    try {
      const data = await requirementsApi.getDataMappings(requirementId);
      setMappings(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await requirementsApi.createDataMapping({ ...formData, requirement_id: requirementId, status: 'pending' });
      setShowForm(false);
      setFormData({ source_system: '', source_field: '', target_field: '', transformation_logic: '', validation_rules: '' });
      loadMappings();
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold">Data Mappings</h3>
        <button onClick={() => setShowForm(!showForm)} className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90">
          {showForm ? 'Cancel' : 'Add Mapping'}
        </button>
      </div>
      {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">{error}</div>}
      {showForm && (
        <form onSubmit={handleSubmit} className="mb-6 space-y-4 bg-gray-50 p-4 rounded">
          <div className="grid grid-cols-2 gap-4">
            <input type="text" placeholder="Source System" value={formData.source_system} onChange={(e) => setFormData({ ...formData, source_system: e.target.value })} required className="px-4 py-2 border rounded" />
            <input type="text" placeholder="Source Field" value={formData.source_field} onChange={(e) => setFormData({ ...formData, source_field: e.target.value })} required className="px-4 py-2 border rounded" />
            <input type="text" placeholder="Target Field" value={formData.target_field} onChange={(e) => setFormData({ ...formData, target_field: e.target.value })} required className="px-4 py-2 border rounded" />
            <input type="text" placeholder="Transformation Logic" value={formData.transformation_logic} onChange={(e) => setFormData({ ...formData, transformation_logic: e.target.value })} className="px-4 py-2 border rounded" />
          </div>
          <textarea placeholder="Validation Rules" value={formData.validation_rules} onChange={(e) => setFormData({ ...formData, validation_rules: e.target.value })} rows={2} className="w-full px-4 py-2 border rounded" />
          <button type="submit" className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90">Save Mapping</button>
        </form>
      )}
      {loading ? (
        <div className="flex justify-center p-8"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div></div>
      ) : mappings.length === 0 ? (
        <p className="text-center text-gray-500 py-8">No data mappings yet</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Source System</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Source Field</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Target Field</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {mappings.map((mapping) => (
                <tr key={mapping.id}>
                  <td className="px-4 py-2 text-sm">{mapping.source_system}</td>
                  <td className="px-4 py-2 text-sm">{mapping.source_field}</td>
                  <td className="px-4 py-2 text-sm">{mapping.target_field}</td>
                  <td className="px-4 py-2 text-sm"><span className={`px-2 py-1 rounded text-xs ${mapping.status === 'approved' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>{mapping.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
