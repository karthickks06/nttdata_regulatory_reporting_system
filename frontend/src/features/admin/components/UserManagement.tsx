import { useState, useEffect } from 'react';
import { adminApi } from '../services/adminApi';
import type { User } from '../types';

export function UserManagement() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ username: '', email: '', full_name: '', department: '' });

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const data = await adminApi.getUsers();
      setUsers(data);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await adminApi.createUser(formData);
      setShowForm(false);
      setFormData({ username: '', email: '', full_name: '', department: '' });
      loadUsers();
    } catch (error) {
      alert('Failed to create user');
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure?')) return;
    try {
      await adminApi.deleteUser(id);
      loadUsers();
    } catch (error) {
      alert('Failed to delete user');
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">User Management</h1>
        <button onClick={() => setShowForm(!showForm)} className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90">{showForm ? 'Cancel' : 'Add User'}</button>
      </div>
      {showForm && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <form onSubmit={handleCreate} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <input type="text" placeholder="Username" value={formData.username} onChange={(e) => setFormData({ ...formData, username: e.target.value })} required className="px-4 py-2 border rounded" />
              <input type="email" placeholder="Email" value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} required className="px-4 py-2 border rounded" />
              <input type="text" placeholder="Full Name" value={formData.full_name} onChange={(e) => setFormData({ ...formData, full_name: e.target.value })} className="px-4 py-2 border rounded" />
              <input type="text" placeholder="Department" value={formData.department} onChange={(e) => setFormData({ ...formData, department: e.target.value })} className="px-4 py-2 border rounded" />
            </div>
            <button type="submit" className="px-6 py-2 bg-primary text-white rounded hover:bg-primary/90">Create User</button>
          </form>
        </div>
      )}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="flex justify-center p-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>
        ) : (
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Username</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Full Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {users.map((user) => (
                <tr key={user.id}>
                  <td className="px-6 py-4 text-sm font-medium">{user.username}</td>
                  <td className="px-6 py-4 text-sm">{user.email}</td>
                  <td className="px-6 py-4 text-sm">{user.full_name}</td>
                  <td className="px-6 py-4"><span className={`px-2 py-1 rounded text-xs ${user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>{user.is_active ? 'Active' : 'Inactive'}</span></td>
                  <td className="px-6 py-4 text-sm"><button onClick={() => handleDelete(user.id)} className="text-red-600 hover:text-red-900">Delete</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
