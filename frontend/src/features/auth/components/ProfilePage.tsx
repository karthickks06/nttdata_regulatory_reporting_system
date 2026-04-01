import { useState, useEffect } from 'react';
import { useAppSelector } from '@/shared/store/store';
import { authApi } from '../services/authApi';

export function ProfilePage() {
  const { user } = useAppSelector((state) => state.auth);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  const [formData, setFormData] = useState({
    full_name: '',
    department: '',
    email: ''
  });

  useEffect(() => {
    if (user) {
      setFormData({
        full_name: user.full_name || '',
        department: user.department || '',
        email: user.email || ''
      });
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      await authApi.updateProfile(formData);
      setSuccess('Profile updated successfully');
      setIsEditing(false);
    } catch (err: any) {
      setError(err.message || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    if (user) {
      setFormData({
        full_name: user.full_name || '',
        department: user.department || '',
        email: user.email || ''
      });
    }
    setIsEditing(false);
    setError('');
  };

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Profile</h1>
          {!isEditing && (
            <button
              onClick={() => setIsEditing(true)}
              className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90"
            >
              Edit Profile
            </button>
          )}
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
            {success}
          </div>
        )}

        {isEditing ? (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Username</label>
              <input
                type="text"
                value={user.username}
                disabled
                className="w-full px-4 py-2 border rounded bg-gray-100 cursor-not-allowed"
              />
              <p className="text-xs text-gray-500 mt-1">Username cannot be changed</p>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Full Name</label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Department</label>
              <input
                type="text"
                name="department"
                value={formData.department}
                onChange={handleChange}
                className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-2 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50"
              >
                {loading ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                type="button"
                onClick={handleCancel}
                className="px-6 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-600">Username</label>
                <p className="mt-1 text-lg">{user.username}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-600">Email</label>
                <p className="mt-1 text-lg">{user.email}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-600">Full Name</label>
                <p className="mt-1 text-lg">{user.full_name || 'Not set'}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-600">Department</label>
                <p className="mt-1 text-lg">{user.department || 'Not set'}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-600">Status</label>
                <p className="mt-1 text-lg">
                  {user.is_active ? (
                    <span className="text-green-600">Active</span>
                  ) : (
                    <span className="text-red-600">Inactive</span>
                  )}
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-600">Role</label>
                <p className="mt-1 text-lg">
                  {user.is_superuser ? 'Super Admin' : 'User'}
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-600">Member Since</label>
                <p className="mt-1 text-lg">
                  {new Date(user.created_at).toLocaleDateString()}
                </p>
              </div>

              {user.last_login && (
                <div>
                  <label className="block text-sm font-medium text-gray-600">Last Login</label>
                  <p className="mt-1 text-lg">
                    {new Date(user.last_login).toLocaleString()}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
