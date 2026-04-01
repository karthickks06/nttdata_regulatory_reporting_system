import { useState, useEffect } from 'react';
import { adminApi } from '../services/adminApi';
import type { Role, Permission } from '../types';

export function RolePermissions() {
  const [roles, setRoles] = useState<Role[]>([]);
  const [permissions, setPermissions] = useState<Permission[]>([]);
  const [selectedRole, setSelectedRole] = useState<number | null>(null);
  const [selectedPermissions, setSelectedPermissions] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [rolesData, permsData] = await Promise.all([adminApi.getRoles(), adminApi.getPermissions()]);
      setRoles(rolesData);
      setPermissions(permsData);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!selectedRole) return;
    try {
      await adminApi.updateRolePermissions(selectedRole, selectedPermissions);
      alert('Permissions updated successfully');
    } catch (error) {
      alert('Failed to update permissions');
    }
  };

  const togglePermission = (permId: number) => {
    setSelectedPermissions(prev =>
      prev.includes(permId) ? prev.filter(id => id !== permId) : [...prev, permId]
    );
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Role Permissions</h1>
      {loading ? (
        <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>
      ) : (
        <div className="grid grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-4">
            <h3 className="font-semibold mb-4">Roles</h3>
            <div className="space-y-2">
              {roles.map((role) => (
                <button
                  key={role.id}
                  onClick={() => setSelectedRole(role.id)}
                  className={`w-full text-left px-4 py-2 rounded ${selectedRole === role.id ? 'bg-primary text-white' : 'bg-gray-100 hover:bg-gray-200'}`}
                >
                  {role.display_name}
                </button>
              ))}
            </div>
          </div>
          <div className="col-span-2 bg-white rounded-lg shadow p-4">
            <h3 className="font-semibold mb-4">Permissions</h3>
            {selectedRole ? (
              <>
                <div className="space-y-2 max-h-96 overflow-y-auto mb-4">
                  {permissions.map((perm) => (
                    <label key={perm.id} className="flex items-center gap-2 p-2 hover:bg-gray-50 rounded cursor-pointer">
                      <input
                        type="checkbox"
                        checked={selectedPermissions.includes(perm.id)}
                        onChange={() => togglePermission(perm.id)}
                        className="rounded"
                      />
                      <div className="flex-1">
                        <div className="font-medium text-sm">{perm.name}</div>
                        <div className="text-xs text-gray-500">{perm.description}</div>
                      </div>
                    </label>
                  ))}
                </div>
                <button onClick={handleSave} className="px-6 py-2 bg-primary text-white rounded hover:bg-primary/90">Save Permissions</button>
              </>
            ) : (
              <p className="text-gray-500 text-center py-8">Select a role to manage permissions</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
