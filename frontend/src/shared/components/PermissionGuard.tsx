import { ReactNode } from 'react';
import { useAppSelector } from '../store/store';

interface PermissionGuardProps {
  permission: string;
  children: ReactNode;
  fallback?: ReactNode;
}

export function PermissionGuard({
  permission,
  children,
  fallback = null
}: PermissionGuardProps) {
  const { user } = useAppSelector((state) => state.auth);

  // Superusers have all permissions
  if (user?.is_superuser) {
    return <>{children}</>;
  }

  // Check if user has the required permission
  const hasPermission = user?.permissions?.some(
    (p) => p.name === permission
  ) || false;

  if (!hasPermission) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}

interface UsePermissionReturn {
  hasPermission: (permission: string) => boolean;
  hasAnyPermission: (permissions: string[]) => boolean;
  hasAllPermissions: (permissions: string[]) => boolean;
}

export function usePermissions(): UsePermissionReturn {
  const { user } = useAppSelector((state) => state.auth);

  const hasPermission = (permission: string): boolean => {
    if (user?.is_superuser) return true;
    return user?.permissions?.some((p) => p.name === permission) || false;
  };

  const hasAnyPermission = (permissions: string[]): boolean => {
    if (user?.is_superuser) return true;
    return permissions.some(hasPermission);
  };

  const hasAllPermissions = (permissions: string[]): boolean => {
    if (user?.is_superuser) return true;
    return permissions.every(hasPermission);
  };

  return { hasPermission, hasAnyPermission, hasAllPermissions };
}
