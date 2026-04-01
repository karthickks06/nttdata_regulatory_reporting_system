import { useAppSelector } from '@/shared/store/store';
import { useAuth } from '@/features/auth/hooks/useAuth';

export function Header() {
  const { user } = useAppSelector((state) => state.auth);
  const { logout } = useAuth();

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <a href="/" className="flex items-center">
              <div className="w-8 h-8 bg-primary rounded flex items-center justify-center text-white font-bold">
                NTT
              </div>
              <span className="ml-2 text-xl font-bold text-gray-900">
                Regulatory Reporting
              </span>
            </a>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex space-x-8">
            <a
              href="/dashboard"
              className="text-gray-700 hover:text-primary px-3 py-2 text-sm font-medium"
            >
              Dashboard
            </a>
            <a
              href="/regulatory-updates"
              className="text-gray-700 hover:text-primary px-3 py-2 text-sm font-medium"
            >
              Documents
            </a>
            <a
              href="/requirements"
              className="text-gray-700 hover:text-primary px-3 py-2 text-sm font-medium"
            >
              Requirements
            </a>
            <a
              href="/development"
              className="text-gray-700 hover:text-primary px-3 py-2 text-sm font-medium"
            >
              Development
            </a>
            <a
              href="/reporting"
              className="text-gray-700 hover:text-primary px-3 py-2 text-sm font-medium"
            >
              Reports
            </a>
            <a
              href="/agents"
              className="text-gray-700 hover:text-primary px-3 py-2 text-sm font-medium"
            >
              Agents
            </a>
          </nav>

          {/* User Menu */}
          <div className="flex items-center gap-4">
            {user && (
              <div className="flex items-center gap-3">
                <div className="text-right hidden sm:block">
                  <div className="text-sm font-medium text-gray-700">
                    {user.full_name || user.username}
                  </div>
                  <div className="text-xs text-gray-500">{user.email}</div>
                </div>
                <div className="relative">
                  <button className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100">
                    <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white font-medium">
                      {(user.full_name || user.username).charAt(0).toUpperCase()}
                    </div>
                  </button>
                </div>
                <button
                  onClick={logout}
                  className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
