import { useAppSelector } from '@/shared/store/store';

interface UsePermissionsReturn {
  hasPermission: (permission: string) => boolean;
  hasAnyPermission: (permissions: string[]) => boolean;
  hasAllPermissions: (permissions: string[]) => boolean;
  canAccessResource: (resource: string, action: string) => boolean;
}

export function usePermissions(): UsePermissionsReturn {
  const { user } = useAppSelector((state) => state.auth);

  const hasPermission = (permission: string): boolean => {
    if (!user) return false;
    if (user.is_superuser) return true;
    return user.permissions?.some((p) => p.name === permission) || false;
  };

  const hasAnyPermission = (permissions: string[]): boolean => {
    if (!user) return false;
    if (user.is_superuser) return true;
    return permissions.some(hasPermission);
  };

  const hasAllPermissions = (permissions: string[]): boolean => {
    if (!user) return false;
    if (user.is_superuser) return true;
    return permissions.every(hasPermission);
  };

  const canAccessResource = (resource: string, action: string): boolean => {
    if (!user) return false;
    if (user.is_superuser) return true;

    const permissionName = `${resource}:${action}`;
    return user.permissions?.some(
      (p) => p.resource === resource && p.action === action
    ) || false;
  };

  return {
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    canAccessResource
  };
}
