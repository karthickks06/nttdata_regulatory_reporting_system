import { useState, useEffect } from 'react';
import { workflowApi } from '../services/workflowApi';
import type { Workflow, WorkflowStep } from '../types';

interface ProcessStatusProps {
  workflowId: number;
}

export function ProcessStatus({ workflowId }: ProcessStatusProps) {
  const [workflow, setWorkflow] = useState<Workflow | null>(null);
  const [steps, setSteps] = useState<WorkflowStep[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadWorkflow();
  }, [workflowId]);

  const loadWorkflow = async () => {
    try {
      const [workflowData, stepsData] = await Promise.all([
        workflowApi.getWorkflow(workflowId),
        workflowApi.getWorkflowSteps(workflowId)
      ]);
      setWorkflow(workflowData);
      setSteps(stepsData);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>;
  if (!workflow) return <div>Workflow not found</div>;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-xl font-bold mb-4">{workflow.name}</h3>
      <div className="mb-6">
        <div className="flex justify-between text-sm mb-2">
          <span>Progress</span>
          <span>{workflow.progress_percentage}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div className="bg-primary h-2 rounded-full transition-all" style={{ width: `${workflow.progress_percentage}%` }} />
        </div>
      </div>
      <div className="space-y-3">
        {steps.map((step, idx) => (
          <div key={step.id} className="flex gap-4">
            <div className="flex flex-col items-center">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${step.status === 'completed' ? 'bg-green-500 text-white' : step.status === 'in_progress' ? 'bg-blue-500 text-white' : step.status === 'failed' ? 'bg-red-500 text-white' : 'bg-gray-300'}`}>
                {idx + 1}
              </div>
              {idx < steps.length - 1 && <div className="w-0.5 h-full bg-gray-300 my-2" />}
            </div>
            <div className="flex-1 pb-4">
              <h4 className="font-semibold">{step.step_name}</h4>
              <p className="text-sm text-gray-600 capitalize">{step.status.replace('_', ' ')}</p>
              {step.error_message && <p className="text-sm text-red-600 mt-1">{step.error_message}</p>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
