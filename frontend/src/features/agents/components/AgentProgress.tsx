import { useState, useEffect } from 'react';
import { agentsApi } from '../services/agentsApi';
import type { AgentProgress as AgentProgressType } from '../types';

export function AgentProgress() {
  const [progress, setProgress] = useState<AgentProgressType[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProgress();
    const interval = setInterval(loadProgress, 3000);
    return () => clearInterval(interval);
  }, []);

  const loadProgress = async () => {
    try {
      const data = await agentsApi.getAgentProgress();
      setProgress(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Agent Progress</h1>
      {loading ? (
        <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>
      ) : progress.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center text-gray-500">No agents currently running</div>
      ) : (
        <div className="space-y-4">
          {progress.map((item) => (
            <div key={item.agent_id} className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold">{item.agent_name}</h3>
                  <p className="text-sm text-gray-600">{item.current_step}</p>
                </div>
                <span className="text-lg font-semibold">{item.progress_percentage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-primary h-3 rounded-full transition-all duration-300"
                  style={{ width: `${item.progress_percentage}%` }}
                />
              </div>
              {item.estimated_completion && (
                <p className="text-xs text-gray-500 mt-2">
                  Est. completion: {new Date(item.estimated_completion).toLocaleString()}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
