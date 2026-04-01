import { useState, useEffect } from 'react';
import { requirementsApi } from '../services/requirementsApi';
import type { ApprovalWorkflowStep } from '../types';

interface ApprovalWorkflowProps {
  requirementId: number;
}

export function ApprovalWorkflow({ requirementId }: ApprovalWorkflowProps) {
  const [steps, setSteps] = useState<ApprovalWorkflowStep[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [actionLoading, setActionLoading] = useState(false);
  const [comments, setComments] = useState<{ [key: number]: string }>({});

  useEffect(() => {
    loadWorkflow();
  }, [requirementId]);

  const loadWorkflow = async () => {
    setLoading(true);
    try {
      const data = await requirementsApi.getApprovalWorkflow(requirementId);
      setSteps(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (stepId: number) => {
    setActionLoading(true);
    try {
      await requirementsApi.approveRequirement(requirementId, stepId, comments[stepId]);
      loadWorkflow();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const handleReject = async (stepId: number) => {
    if (!comments[stepId]) {
      alert('Please provide a reason for rejection');
      return;
    }
    setActionLoading(true);
    try {
      await requirementsApi.rejectRequirement(requirementId, stepId, comments[stepId]);
      loadWorkflow();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'approved': return <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center"><svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" /></svg></div>;
      case 'rejected': return <div className="w-6 h-6 bg-red-500 rounded-full flex items-center justify-center"><svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" /></svg></div>;
      default: return <div className="w-6 h-6 bg-gray-300 rounded-full"></div>;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-xl font-bold mb-4">Approval Workflow</h3>
      {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">{error}</div>}
      {loading ? (
        <div className="flex justify-center p-8"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div></div>
      ) : (
        <div className="space-y-4">
          {steps.map((step, idx) => (
            <div key={step.id} className="flex gap-4">
              <div className="flex flex-col items-center">
                {getStatusIcon(step.status)}
                {idx < steps.length - 1 && <div className="w-0.5 h-full bg-gray-300 my-2"></div>}
              </div>
              <div className="flex-1 pb-8">
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="font-semibold">{step.step_name}</h4>
                      <p className="text-sm text-gray-600">Approver: {step.approver_name}</p>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${step.status === 'approved' ? 'bg-green-100 text-green-800' : step.status === 'rejected' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>{step.status}</span>
                  </div>
                  {step.comments && <p className="text-sm text-gray-700 mb-2">{step.comments}</p>}
                  {step.approved_at && <p className="text-xs text-gray-500">Completed: {new Date(step.approved_at).toLocaleString()}</p>}
                  {step.status === 'pending' && (
                    <div className="mt-3 space-y-2">
                      <textarea placeholder="Add comments (optional for approval, required for rejection)" value={comments[step.id] || ''} onChange={(e) => setComments({ ...comments, [step.id]: e.target.value })} rows={2} className="w-full px-3 py-2 border rounded text-sm" />
                      <div className="flex gap-2">
                        <button onClick={() => handleApprove(step.id)} disabled={actionLoading} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm disabled:opacity-50">Approve</button>
                        <button onClick={() => handleReject(step.id)} disabled={actionLoading} className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm disabled:opacity-50">Reject</button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
