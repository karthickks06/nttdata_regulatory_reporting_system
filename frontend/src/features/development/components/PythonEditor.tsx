import { useState } from 'react';

export function PythonEditor() {
  const [code, setCode] = useState('# Python code editor\nimport pandas as pd\n\n# Your code here');
  const [output, setOutput] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const handleRun = async () => {
    setLoading(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      setOutput('Code executed successfully');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Python Editor</h1>
      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          rows={15}
          className="w-full px-4 py-2 border rounded font-mono text-sm focus:ring-2 focus:ring-primary"
        />
        <button
          onClick={handleRun}
          disabled={loading}
          className="px-6 py-2 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50"
        >
          {loading ? 'Running...' : 'Run Code'}
        </button>
        {output && (
          <div className="p-4 bg-gray-900 text-green-400 rounded font-mono text-sm">
            <pre>{output}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
