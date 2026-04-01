import { useState, useEffect } from 'react';
import { agentsApi } from '../services/agentsApi';
import type { Agent, AgentExecution } from '../types';

export function ComplianceAgentView() {
  const [agent, setAgent] = useState<Agent | null>(null);
  const [executions, setExecutions] = useState<AgentExecution[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const agents = await agentsApi.getAgents();
      const complianceAgent = agents.find(a => a.agent_type === 'compliance');
      if (complianceAgent) {
        setAgent(complianceAgent);
        const execs = await agentsApi.getAgentExecutions(complianceAgent.id);
        setExecutions(execs);
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>;
  if (!agent) return <div className="p-6">Compliance Agent not found</div>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Compliance Agent (Master Orchestrator)</h1>
      <div className="bg-purple-50 border-2 border-purple-200 rounded-lg p-6 mb-6">
        <div className="grid grid-cols-2 gap-4">
          <div><span className="font-medium">Agent Name:</span> {agent.name}</div>
          <div><span className="font-medium">Status:</span> <span className="capitalize">{agent.status}</span></div>
          <div><span className="font-medium">Success Rate:</span> {agent.success_rate}%</div>
          <div><span className="font-medium">Total Executions:</span> {agent.total_executions}</div>
        </div>
      </div>
      <h2 className="text-xl font-semibold mb-4">Recent Executions</h2>
      <div className="space-y-3">
        {executions.map((exec) => (
          <div key={exec.id} className="bg-white rounded-lg shadow p-4">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-semibold">{exec.task_name}</h3>
                <p className="text-sm text-gray-600">Started: {new Date(exec.start_time).toLocaleString()}</p>
              </div>
              <span className={`px-2 py-1 rounded text-xs ${exec.status === 'completed' ? 'bg-green-100 text-green-800' : exec.status === 'failed' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'}`}>
                {exec.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
