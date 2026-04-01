import { useState } from 'react';
import { reportingApi } from '../services/reportingApi';

interface SubmissionPortalProps {
  reportId: number;
}

export function SubmissionPortal({ reportId }: SubmissionPortalProps) {
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async () => {
    if (!window.confirm('Are you sure you want to submit this report? This action cannot be undone.')) return;
    setSubmitting(true);
    setError('');
    try {
      await reportingApi.submitReport(reportId);
      setSuccess(true);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-xl font-bold mb-4">Submission Portal</h3>
      {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">{error}</div>}
      {success ? (
        <div className="p-6 bg-green-50 border border-green-200 rounded text-center">
          <svg className="mx-auto h-12 w-12 text-green-500 mb-3" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          <h4 className="text-lg font-semibold text-green-800 mb-2">Report Submitted Successfully</h4>
          <p className="text-green-700">Your report has been submitted to the regulatory authority.</p>
        </div>
      ) : (
        <>
          <div className="bg-yellow-50 border border-yellow-200 rounded p-4 mb-4">
            <p className="text-sm text-yellow-800"><strong>Warning:</strong> Please ensure all validation checks have passed before submitting.</p>
          </div>
          <button onClick={handleSubmit} disabled={submitting} className="w-full px-6 py-3 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50 font-medium">
            {submitting ? 'Submitting...' : 'Submit Report'}
          </button>
        </>
      )}
    </div>
  );
}
