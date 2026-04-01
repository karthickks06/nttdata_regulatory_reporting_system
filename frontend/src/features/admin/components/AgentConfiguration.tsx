import { useState, useEffect } from 'react';
import { adminApi } from '../services/adminApi';
import type { AgentConfig } from '../types';

export function AgentConfiguration() {
  const [configs, setConfigs] = useState<AgentConfig[]>([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState<number | null>(null);
  const [formData, setFormData] = useState<Partial<AgentConfig>>({});

  useEffect(() => {
    loadConfigs();
  }, []);

  const loadConfigs = async () => {
    try {
      const data = await adminApi.getAgentConfigs();
      setConfigs(data);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (config: AgentConfig) => {
    setEditing(config.id);
    setFormData(config);
  };

  const handleSave = async () => {
    if (!editing) return;
    try {
      await adminApi.updateAgentConfig(editing, formData);
      setEditing(null);
      loadConfigs();
    } catch (error) {
      alert('Failed to update configuration');
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Agent Configuration</h1>
      {loading ? (
        <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>
      ) : (
        <div className="space-y-4">
          {configs.map((config) => (
            <div key={config.id} className="bg-white rounded-lg shadow p-6">
              {editing === config.id ? (
                <div className="space-y-4">
                  <input
                    type="text"
                    value={formData.agent_name || ''}
                    onChange={(e) => setFormData({ ...formData, agent_name: e.target.value })}
                    className="w-full px-4 py-2 border rounded"
                  />
                  <div className="grid grid-cols-3 gap-4">
                    <input
                      type="text"
                      value={formData.model || ''}
                      onChange={(e) => setFormData({ ...formData, model: e.target.value })}
                      placeholder="Model"
                      className="px-4 py-2 border rounded"
                    />
                    <input
                      type="number"
                      step="0.1"
                      value={formData.temperature || 0}
                      onChange={(e) => setFormData({ ...formData, temperature: parseFloat(e.target.value) })}
                      placeholder="Temperature"
                      className="px-4 py-2 border rounded"
                    />
                    <input
                      type="number"
                      value={formData.max_tokens || 0}
                      onChange={(e) => setFormData({ ...formData, max_tokens: parseInt(e.target.value) })}
                      placeholder="Max Tokens"
                      className="px-4 py-2 border rounded"
                    />
                  </div>
                  <div className="flex gap-2">
                    <button onClick={handleSave} className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90">Save</button>
                    <button onClick={() => setEditing(null)} className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">Cancel</button>
                  </div>
                </div>
              ) : (
                <div>
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-lg font-semibold">{config.agent_name}</h3>
                      <p className="text-sm text-gray-600">{config.agent_type}</p>
                    </div>
                    <div className="flex gap-2">
                      <span className={`px-2 py-1 rounded text-xs ${config.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                        {config.is_active ? 'Active' : 'Inactive'}
                      </span>
                      <button onClick={() => handleEdit(config)} className="text-primary hover:text-primary/90">Edit</button>
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div><span className="text-gray-600">Model:</span> {config.model}</div>
                    <div><span className="text-gray-600">Temperature:</span> {config.temperature}</div>
                    <div><span className="text-gray-600">Max Tokens:</span> {config.max_tokens}</div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
