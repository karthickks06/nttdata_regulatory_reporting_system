import { useState } from 'react';
import { reportingApi } from '../services/reportingApi';

export function ReportGenerator() {
  const [formData, setFormData] = useState({
    title: '',
    report_type: 'Regulatory',
    parameters: {}
  });
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setGenerating(true);
    setError('');
    setSuccess('');
    try {
      await reportingApi.generateReport(formData);
      setSuccess('Report generation started successfully');
      setFormData({ title: '', report_type: 'Regulatory', parameters: {} });
    } catch (err: any) {
      setError(err.message);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-6">Generate Report</h2>
        {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">{error}</div>}
        {success && <div className="mb-4 p-3 bg-green-100 text-green-700 rounded">{success}</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Report Title*</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required
              className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Report Type*</label>
            <select
              value={formData.report_type}
              onChange={(e) => setFormData({ ...formData, report_type: e.target.value })}
              className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary"
            >
              <option value="Regulatory">Regulatory Report</option>
              <option value="Compliance">Compliance Report</option>
              <option value="Audit">Audit Report</option>
              <option value="Management">Management Report</option>
            </select>
          </div>
          <button
            type="submit"
            disabled={generating}
            className="w-full px-6 py-3 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50"
          >
            {generating ? 'Generating...' : 'Generate Report'}
          </button>
        </form>
      </div>
    </div>
  );
}
