import { useState, useEffect } from 'react';
import { developmentApi } from '../services/developmentApi';
import type { TestCase } from '../types';

interface TestCaseManagerProps {
  codeId: number;
}

export function TestCaseManager({ codeId }: TestCaseManagerProps) {
  const [tests, setTests] = useState<TestCase[]>([]);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    loadTests();
  }, [codeId]);

  const loadTests = async () => {
    setLoading(true);
    try {
      const data = await developmentApi.getTestCases(codeId);
      setTests(data);
    } finally {
      setLoading(false);
    }
  };

  const handleRunTests = async () => {
    setRunning(true);
    try {
      const results = await developmentApi.runTests(codeId);
      setTests(results);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold">Test Cases</h3>
        <button
          onClick={handleRunTests}
          disabled={running}
          className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50"
        >
          {running ? 'Running...' : 'Run All Tests'}
        </button>
      </div>
      {loading ? (
        <div className="flex justify-center p-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      ) : tests.length === 0 ? (
        <p className="text-center text-gray-500 py-8">No test cases defined</p>
      ) : (
        <div className="space-y-3">
          {tests.map((test) => (
            <div key={test.id} className="border rounded-lg p-4">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h4 className="font-semibold">{test.test_name}</h4>
                  <p className="text-sm text-gray-600">{test.test_type}</p>
                </div>
                <span
                  className={`px-2 py-1 rounded text-xs font-semibold ${
                    test.status === 'passed'
                      ? 'bg-green-100 text-green-800'
                      : test.status === 'failed'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {test.status}
                </span>
              </div>
              {test.error_message && (
                <div className="mt-2 p-2 bg-red-50 text-red-700 rounded text-sm">
                  {test.error_message}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
