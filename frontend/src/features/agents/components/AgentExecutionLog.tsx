import { useState, useEffect } from 'react';
import { agentsApi } from '../services/agentsApi';
import type { AgentExecution } from '../types';

export function AgentExecutionLog() {
  const [executions, setExecutions] = useState<AgentExecution[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedExec, setSelectedExec] = useState<AgentExecution | null>(null);

  useEffect(() => {
    loadExecutions();
  }, []);

  const loadExecutions = async () => {
    try {
      const data = await agentsApi.getAgentExecutions();
      setExecutions(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Agent Execution Logs</h1>
      {loading ? (
        <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>
      ) : (
        <div className="grid grid-cols-3 gap-6">
          <div className="col-span-1 space-y-2">
            {executions.map((exec) => (
              <div
                key={exec.id}
                onClick={() => setSelectedExec(exec)}
                className={`p-3 rounded cursor-pointer ${selectedExec?.id === exec.id ? 'bg-primary text-white' : 'bg-white hover:bg-gray-50'}`}
              >
                <div className="font-medium">{exec.task_name}</div>
                <div className="text-xs mt-1">{exec.agent_name}</div>
              </div>
            ))}
          </div>
          <div className="col-span-2 bg-white rounded-lg shadow p-6">
            {selectedExec ? (
              <div>
                <h3 className="text-lg font-semibold mb-4">{selectedExec.task_name}</h3>
                <div className="space-y-2 mb-4">
                  <div><span className="font-medium">Agent:</span> {selectedExec.agent_name}</div>
                  <div><span className="font-medium">Status:</span> {selectedExec.status}</div>
                  <div><span className="font-medium">Start:</span> {new Date(selectedExec.start_time).toLocaleString()}</div>
                  {selectedExec.end_time && <div><span className="font-medium">End:</span> {new Date(selectedExec.end_time).toLocaleString()}</div>}
                </div>
                <h4 className="font-semibold mb-2">Logs</h4>
                <div className="bg-gray-900 text-green-400 rounded p-4 font-mono text-sm max-h-96 overflow-y-auto">
                  {selectedExec.logs.map((log) => (
                    <div key={log.id} className="mb-1">
                      <span className="text-gray-500">[{new Date(log.timestamp).toLocaleTimeString()}]</span>
                      <span className={`ml-2 ${log.level === 'error' ? 'text-red-400' : log.level === 'warning' ? 'text-yellow-400' : ''}`}>
                        {log.message}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-center text-gray-500 py-12">Select an execution to view logs</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
