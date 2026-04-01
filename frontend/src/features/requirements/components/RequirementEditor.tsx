import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { requirementsApi } from '../services/requirementsApi';
import type { Requirement } from '../types';

export function RequirementEditor() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [formData, setFormData] = useState<Partial<Requirement>>({
    title: '',
    description: '',
    requirement_type: 'Functional',
    priority: 'medium',
    status: 'draft',
    regulatory_reference: '',
    impact_assessment: '',
    implementation_notes: ''
  });

  useEffect(() => {
    if (id) {
      loadRequirement();
    }
  }, [id]);

  const loadRequirement = async () => {
    setLoading(true);
    try {
      const data = await requirementsApi.getRequirement(Number(id));
      setFormData(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load requirement');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (id) {
        await requirementsApi.updateRequirement(Number(id), formData);
      } else {
        await requirementsApi.createRequirement(formData);
      }
      navigate('/requirements');
    } catch (err: any) {
      setError(err.message || 'Failed to save requirement');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-6">{id ? 'Edit Requirement' : 'Create Requirement'}</h2>
        {error && <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Title*</label>
            <input type="text" name="title" value={formData.title} onChange={handleChange} required className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Description*</label>
            <textarea name="description" value={formData.description} onChange={handleChange} required rows={4} className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Type*</label>
              <select name="requirement_type" value={formData.requirement_type} onChange={handleChange} className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary">
                <option value="Functional">Functional</option>
                <option value="Data">Data</option>
                <option value="Reporting">Reporting</option>
                <option value="Compliance">Compliance</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Priority*</label>
              <select name="priority" value={formData.priority} onChange={handleChange} className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary">
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Regulatory Reference</label>
            <input type="text" name="regulatory_reference" value={formData.regulatory_reference} onChange={handleChange} className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Impact Assessment</label>
            <textarea name="impact_assessment" value={formData.impact_assessment} onChange={handleChange} rows={3} className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Implementation Notes</label>
            <textarea name="implementation_notes" value={formData.implementation_notes} onChange={handleChange} rows={3} className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary" />
          </div>
          <div className="flex gap-3">
            <button type="submit" disabled={loading} className="px-6 py-2 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50">{loading ? 'Saving...' : 'Save Requirement'}</button>
            <button type="button" onClick={() => navigate('/requirements')} className="px-6 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}
