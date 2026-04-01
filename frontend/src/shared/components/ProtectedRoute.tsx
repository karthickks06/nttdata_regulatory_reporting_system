import { Navigate, Outlet } from 'react-router-dom';
import { useAppSelector } from '../store/store';

interface ProtectedRouteProps {
  redirectPath?: string;
  children?: React.ReactNode;
}

export function ProtectedRoute({
  redirectPath = '/login',
  children
}: ProtectedRouteProps) {
  const { isAuthenticated, loading } = useAppSelector((state) => state.auth);

  if (loading === 'loading') {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to={redirectPath} replace />;
  }

  return children ? <>{children}</> : <Outlet />;
}
