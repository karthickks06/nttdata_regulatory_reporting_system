import { useState } from 'react';
import { developmentApi } from '../services/developmentApi';

export function SQLEditor() {
  const [code, setCode] = useState('SELECT * FROM regulatory_updates LIMIT 10;');
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const handleExecute = async () => {
    setLoading(true);
    setError('');
    try {
      // Simulate execution - replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      setResults({ rows: [], rowCount: 0, message: 'Query executed successfully' });
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">SQL Editor</h1>
      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">SQL Query</label>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            rows={10}
            className="w-full px-4 py-2 border rounded font-mono text-sm focus:ring-2 focus:ring-primary"
            placeholder="Enter your SQL query here..."
          />
        </div>
        <button
          onClick={handleExecute}
          disabled={loading}
          className="px-6 py-2 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50"
        >
          {loading ? 'Executing...' : 'Execute Query'}
        </button>
        {error && (
          <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}
        {results && (
          <div className="mt-4 p-4 bg-gray-50 rounded">
            <h3 className="font-semibold mb-2">Results</h3>
            <p className="text-sm text-gray-700">{results.message}</p>
            <p className="text-sm text-gray-500 mt-1">Rows affected: {results.rowCount}</p>
          </div>
        )}
      </div>
    </div>
  );
}
