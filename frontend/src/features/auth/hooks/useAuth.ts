import { useAppSelector, useAppDispatch } from '@/shared/store/store';
import { setUser, clearUser } from '../slices/authSlice';
import { authApi } from '../services/authApi';
import { useNavigate } from 'react-router-dom';

export function useAuth() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { user, isAuthenticated, loading } = useAppSelector((state) => state.auth);

  const login = async (username: string, password: string) => {
    try {
      const response = await authApi.login({ username, password });
      localStorage.setItem('access_token', response.access_token);
      
      const userData = await authApi.getCurrentUser();
      dispatch(setUser(userData));
      navigate('/');
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    await authApi.logout();
    localStorage.removeItem('access_token');
    dispatch(clearUser());
    navigate('/login');
  };

  return { user, isAuthenticated, loading, login, logout };
}
