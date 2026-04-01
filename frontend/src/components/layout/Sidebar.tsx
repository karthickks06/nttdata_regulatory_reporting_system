import { useLocation } from 'react-router-dom';
import { usePermissions } from '@/features/auth/hooks/usePermissions';

interface MenuItem {
  name: string;
  path: string;
  icon: string;
  permission?: string;
}

const menuItems: MenuItem[] = [
  { name: 'Dashboard', path: '/dashboard', icon: '📊' },
  { name: 'Regulatory Updates', path: '/regulatory-updates', icon: '📄' },
  { name: 'Requirements', path: '/requirements', icon: '✓' },
  { name: 'Development', path: '/development', icon: '💻' },
  { name: 'Reporting', path: '/reporting', icon: '📈' },
  { name: 'Workflow', path: '/workflow', icon: '🔄' },
  { name: 'Agents', path: '/agents', icon: '🤖' },
  { name: 'Admin', path: '/admin', icon: '⚙️', permission: 'admin:access' }
];

export function Sidebar() {
  const location = useLocation();
  const { hasPermission } = usePermissions();

  const isActive = (path: string) => {
    return location.pathname.startsWith(path);
  };

  const canAccess = (item: MenuItem) => {
    if (!item.permission) return true;
    return hasPermission(item.permission);
  };

  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen">
      <div className="p-4">
        <div className="mb-8">
          <h2 className="text-lg font-semibold px-3">Navigation</h2>
        </div>
        <nav className="space-y-1">
          {menuItems
            .filter(canAccess)
            .map((item) => (
              <a
                key={item.path}
                href={item.path}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                  isActive(item.path)
                    ? 'bg-primary text-white'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                <span>{item.name}</span>
              </a>
            ))}
        </nav>
      </div>
    </aside>
  );
}
