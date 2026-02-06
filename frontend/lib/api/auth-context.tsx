'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { apiClient } from '@/lib/api/api-client';

interface User {
  id: string;
  email: string;
  name?: string | null;
  createdAt: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on initial load
    const checkAuthStatus = async () => {
      try {
        const userData: User = await apiClient.getProfile();
        setUser(userData);
      } catch (error: unknown) {
        // User is not authenticated
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      console.log('Attempting login with email:', email);
      const response = await apiClient.login({ email, password });
      console.log('Login response:', response);
      setUser(response.user);
    } catch (error: unknown) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const signup = async (name: string, email: string, password: string) => {
    try {
      console.log('Attempting signup with email:', email);
      const response = await apiClient.register({ name, email, password });
      console.log('Signup response:', response);
      setUser(response.user);
    } catch (error: unknown) {
      console.error('Signup error:', error);
      throw error;
    }
  };

  const register = async (email: string, password: string, name?: string) => {
    try {
      const response: { user: User } = await apiClient.register({ email, password, name });
      setUser(response.user);
    } catch (error: unknown) {
      throw error;
    }
  };

  const logout = async () => {
    try {
      await apiClient.logout();
      setUser(null);
    } catch (error: unknown) {
      // Even if logout fails on backend, clear local state
      setUser(null);
    }
  };

  const refreshUser = async () => {
    try {
      const userData: User = await apiClient.getProfile();
      setUser(userData);
    } catch (error: unknown) {
      setUser(null);
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    signup,
    register,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}