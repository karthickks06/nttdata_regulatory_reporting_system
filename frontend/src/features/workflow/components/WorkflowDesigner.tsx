import { useState } from 'react';

export function WorkflowDesigner() {
  const [workflowName, setWorkflowName] = useState('');
  const [steps, setSteps] = useState<string[]>([]);

  const addStep = () => {
    setSteps([...steps, `Step ${steps.length + 1}`]);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Workflow Designer</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">Workflow Name</label>
          <input
            type="text"
            value={workflowName}
            onChange={(e) => setWorkflowName(e.target.value)}
            className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary"
            placeholder="Enter workflow name..."
          />
        </div>
        <div className="mb-4">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-semibold">Workflow Steps</h3>
            <button
              onClick={addStep}
              className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90"
            >
              Add Step
            </button>
          </div>
          <div className="space-y-2">
            {steps.map((step, idx) => (
              <div key={idx} className="flex items-center gap-2 p-3 border rounded">
                <span className="text-sm font-medium">{idx + 1}.</span>
                <input
                  type="text"
                  value={step}
                  onChange={(e) => {
                    const newSteps = [...steps];
                    newSteps[idx] = e.target.value;
                    setSteps(newSteps);
                  }}
                  className="flex-1 px-3 py-1 border rounded"
                />
              </div>
            ))}
          </div>
        </div>
        <button className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700">
          Save Workflow
        </button>
      </div>
    </div>
  );
}
