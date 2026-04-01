#!/usr/bin/env python3
"""
Script to create all remaining project files with placeholder code
"""

import os
from pathlib import Path

# Base paths
FRONTEND_SRC = Path("frontend/src")
BACKEND_APP = Path("backend/app")

# Frontend files to create
FRONTEND_FILES = {
    # Auth feature
    "features/auth/types/auth.types.ts": """export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export interface LoginCredentials {
  username: string;
  password: string;
}
""",
    
    "features/auth/services/authApi.ts": """import { apiClient } from '@/shared/utils/api';
import type { LoginRequest, LoginResponse } from '@/shared/types/api.types';
import type { User } from '@/shared/types/common.types';

export const authApi = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/auth/login', credentials);
    return response.data;
  },

  logout: async (): Promise<void> => {
    await apiClient.post('/auth/logout');
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },
};
""",

    "features/auth/slices/authSlice.ts": """import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { User } from '@/shared/types/common.types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  loading: false,
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
      state.isAuthenticated = true;
    },
    clearUser: (state) => {
      state.user = null;
      state.isAuthenticated = false;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const { setUser, clearUser, setLoading, setError } = authSlice.actions;
export default authSlice.reducer;
""",

    "features/auth/hooks/useAuth.ts": """import { useAppSelector, useAppDispatch } from '@/shared/store/store';
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
""",

    "features/auth/components/LoginForm.tsx": """import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

export function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(username, password);
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div className="w-full max-w-md p-8">
      <h2 className="text-2xl font-bold mb-6">Login</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full px-4 py-2 border rounded"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-4 py-2 border rounded"
        />
        <button type="submit" className="w-full px-4 py-2 bg-primary text-white rounded">
          Login
        </button>
      </form>
    </div>
  );
}
""",

    "app/router.tsx": """import { createBrowserRouter } from 'react-router-dom';
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
""",
}

# Backend files to create
BACKEND_FILES = {
    "api/v1/endpoints/users.py": """from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, get_db
from app.models.user import User

router = APIRouter()

@router.get("/")
async def list_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"users": []}
""",

    "core/logging.py": """import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

logger = logging.getLogger(__name__)
""",

    "core/exceptions.py": """from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
""",
}

def create_file(path: Path, content: str):
    """Create a file with given content"""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content)
        print(f"Created: {path}")
    else:
        print(f"Skipped (exists): {path}")

def main():
    print("Creating frontend files...")
    for file_path, content in FRONTEND_FILES.items():
        create_file(FRONTEND_SRC / file_path, content)
    
    print("\nCreating backend files...")
    for file_path, content in BACKEND_FILES.items():
        create_file(BACKEND_APP / file_path, content)
    
    print("\nDone! Created all files.")

if __name__ == "__main__":
    main()
