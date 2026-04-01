import { useState, useEffect } from 'react';
import { developmentApi } from '../services/developmentApi';
import type { DataLineage } from '../types';

export function LineageViewer() {
  const [lineages, setLineages] = useState<DataLineage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [selectedTable, setSelectedTable] = useState<string>('');

  useEffect(() => {
    loadLineage();
  }, [selectedTable]);

  const loadLineage = async () => {
    setLoading(true);
    try {
      const data = await developmentApi.getDataLineage({ table: selectedTable });
      setLineages(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Data Lineage</h1>
      {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">{error}</div>}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Filter by Table</label>
          <input
            type="text"
            value={selectedTable}
            onChange={(e) => setSelectedTable(e.target.value)}
            placeholder="Enter table name..."
            className="w-full max-w-md px-4 py-2 border rounded focus:ring-2 focus:ring-primary"
          />
        </div>
        {loading ? (
          <div className="flex justify-center p-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : lineages.length === 0 ? (
          <p className="text-center text-gray-500 py-8">No lineage data found</p>
        ) : (
          <div className="space-y-4">
            {lineages.map((lineage, idx) => (
              <div key={idx} className="border rounded-lg p-4 bg-gray-50">
                <div className="flex items-center gap-4">
                  <div className="flex-1">
                    <div className="text-sm font-medium">Source</div>
                    <div className="text-gray-700">{lineage.source_table}.{lineage.source_column}</div>
                  </div>
                  <div className="text-gray-400">→</div>
                  <div className="flex-1">
                    <div className="text-sm font-medium">Transformation</div>
                    <div className="text-gray-700 font-mono text-sm">{lineage.transformation}</div>
                  </div>
                  <div className="text-gray-400">→</div>
                  <div className="flex-1">
                    <div className="text-sm font-medium">Target</div>
                    <div className="text-gray-700">{lineage.target_table}.{lineage.target_column}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
