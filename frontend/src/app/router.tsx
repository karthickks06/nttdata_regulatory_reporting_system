import { createBrowserRouter } from 'react-router-dom';
import { ROUTES } from '@/shared/constants/routes';
import { LoginForm } from '@/features/auth/components/LoginForm';

export const router = createBrowserRouter([
  {
    path: ROUTES.HOME,
    element: <div>Home</div>,
  },
  {
    path: ROUTES.LOGIN,
    element: <LoginForm />,
  },
]);
