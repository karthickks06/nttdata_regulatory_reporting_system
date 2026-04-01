import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { reportingApi } from '../services/reportingApi';
import type { Report } from '../types';

export function ReportViewer() {
  const { id } = useParams<{ id: string }>();
  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) loadReport();
  }, [id]);

  const loadReport = async () => {
    try {
      const data = await reportingApi.getReport(Number(id));
      setReport(data);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>;
  if (!report) return <div className="p-6">Report not found</div>;

  return (
    <div className="p-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h1 className="text-3xl font-bold mb-4">{report.title}</h1>
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="text-sm font-medium text-gray-600">Type</label>
            <p>{report.report_type}</p>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-600">Status</label>
            <p className="capitalize">{report.status}</p>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-600">Generated</label>
            <p>{new Date(report.generation_date).toLocaleString()}</p>
          </div>
          {report.submission_date && (
            <div>
              <label className="text-sm font-medium text-gray-600">Submitted</label>
              <p>{new Date(report.submission_date).toLocaleString()}</p>
            </div>
          )}
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90">Download</button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Validate</button>
          {report.status === 'validated' && (
            <button className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Submit</button>
          )}
        </div>
      </div>
    </div>
  );
}
