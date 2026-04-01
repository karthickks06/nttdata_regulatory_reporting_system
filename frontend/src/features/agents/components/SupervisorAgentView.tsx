import { useState, useEffect } from 'react';
import { agentsApi } from '../services/agentsApi';
import type { Agent } from '../types';

export function SupervisorAgentView() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      const data = await agentsApi.getAgents();
      setAgents(data.filter(a => a.agent_type === 'supervisor'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Supervisor Agents (Level 1)</h1>
      {loading ? (
        <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <div key={agent.id} className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4">{agent.name}</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Status:</span>
                  <span className="capitalize font-medium">{agent.status}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Success Rate:</span>
                  <span className="font-medium">{agent.success_rate}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Executions:</span>
                  <span className="font-medium">{agent.total_executions}</span>
                </div>
              </div>
              {agent.current_task && (
                <div className="mt-4 p-3 bg-blue-50 rounded">
                  <div className="text-xs text-gray-600 mb-1">Current Task</div>
                  <div className="text-sm">{agent.current_task}</div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
