import { useState, useEffect } from 'react';
import { agentsApi } from '../services/agentsApi';
import type { Agent } from '../types';

export function AgentDashboard() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAgents();
    const interval = setInterval(loadAgents, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadAgents = async () => {
    try {
      const data = await agentsApi.getAgents();
      setAgents(data);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-blue-100 text-blue-800';
      case 'idle': return 'bg-gray-100 text-gray-800';
      case 'paused': return 'bg-yellow-100 text-yellow-800';
      case 'error': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const groupByLevel = () => {
    return {
      level0: agents.filter(a => a.level === 0),
      level1: agents.filter(a => a.level === 1),
      level2: agents.filter(a => a.level === 2)
    };
  };

  const grouped = groupByLevel();

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Agent Dashboard</h1>
      {loading ? (
        <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>
      ) : (
        <div className="space-y-8">
          {/* Level 0: Compliance Agent */}
          {grouped.level0.length > 0 && (
            <div>
              <h2 className="text-xl font-semibold mb-4">Compliance Agent (Master)</h2>
              <div className="grid grid-cols-1 gap-4">
                {grouped.level0.map((agent) => (
                  <div key={agent.id} className="bg-purple-50 border-2 border-purple-200 rounded-lg p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-lg font-semibold">{agent.name}</h3>
                        <p className="text-sm text-gray-600 capitalize">{agent.agent_type}</p>
                      </div>
                      <span className={`px-3 py-1 rounded text-sm font-semibold ${getStatusColor(agent.status)}`}>
                        {agent.status}
                      </span>
                    </div>
                    {agent.current_task && (
                      <div className="bg-white rounded p-3 mb-2">
                        <span className="text-sm font-medium">Current Task:</span>
                        <p className="text-sm text-gray-700 mt-1">{agent.current_task}</p>
                      </div>
                    )}
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div><span className="text-gray-600">Success Rate:</span> {agent.success_rate}%</div>
                      <div><span className="text-gray-600">Total Executions:</span> {agent.total_executions}</div>
                      <div><span className="text-gray-600">Last Run:</span> {agent.last_execution ? new Date(agent.last_execution).toLocaleString() : 'N/A'}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Level 1: Supervisor Agents */}
          {grouped.level1.length > 0 && (
            <div>
              <h2 className="text-xl font-semibold mb-4">Supervisor Agents</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {grouped.level1.map((agent) => (
                  <div key={agent.id} className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold">{agent.name}</h3>
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${getStatusColor(agent.status)}`}>
                        {agent.status}
                      </span>
                    </div>
                    <div className="text-sm space-y-1">
                      <div>Executions: {agent.total_executions}</div>
                      <div>Success: {agent.success_rate}%</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Level 2: Worker Agents */}
          {grouped.level2.length > 0 && (
            <div>
              <h2 className="text-xl font-semibold mb-4">Worker Agents</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {grouped.level2.map((agent) => (
                  <div key={agent.id} className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold">{agent.name}</h3>
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${getStatusColor(agent.status)}`}>
                        {agent.status}
                      </span>
                    </div>
                    <div className="text-sm space-y-1">
                      <div>Executions: {agent.total_executions}</div>
                      <div>Success: {agent.success_rate}%</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
