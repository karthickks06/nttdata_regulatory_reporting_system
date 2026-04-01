import { useState, useEffect } from 'react';
import { developmentApi } from '../services/developmentApi';
import type { SchemaDefinition } from '../types';

export function SchemaViewer() {
  const [schemas, setSchemas] = useState<SchemaDefinition[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTable, setSelectedTable] = useState<string>('');

  useEffect(() => {
    loadSchemas();
  }, [selectedTable]);

  const loadSchemas = async () => {
    setLoading(true);
    try {
      const data = await developmentApi.getSchema(selectedTable || undefined);
      setSchemas(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Database Schema</h1>
      <div className="mb-4">
        <input
          type="text"
          value={selectedTable}
          onChange={(e) => setSelectedTable(e.target.value)}
          placeholder="Filter by table name..."
          className="w-full max-w-md px-4 py-2 border rounded focus:ring-2 focus:ring-primary"
        />
      </div>
      {loading ? (
        <div className="flex justify-center p-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      ) : (
        <div className="space-y-6">
          {schemas.map((schema) => (
            <div key={schema.table_name} className="bg-white rounded-lg shadow overflow-hidden">
              <div className="px-6 py-4 bg-gray-50 border-b">
                <h2 className="text-xl font-bold">{schema.table_name}</h2>
              </div>
              <table className="min-w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Column</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nullable</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Default</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {schema.columns.map((col) => (
                    <tr key={col.name}>
                      <td className="px-6 py-4 text-sm font-medium">{col.name}</td>
                      <td className="px-6 py-4 text-sm font-mono">{col.data_type}</td>
                      <td className="px-6 py-4 text-sm">{col.nullable ? 'Yes' : 'No'}</td>
                      <td className="px-6 py-4 text-sm font-mono">{col.default_value || '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
