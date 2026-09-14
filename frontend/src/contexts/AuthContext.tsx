import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import type { User } from '../types';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('finora_token'));
  const [isLoading, setIsLoading] = useState(true);

  const fetchUser = async (currentToken: string) => {
    try {
      // In a real app we'd fetch the user profile from /auth/me
      // For now, if a token exists, we assume logged in. 
      // We will actually try to hit a light endpoint if possible, but for MVP, token presence is auth.
      // Let's actually fetch the user details to make it robust.
      const response = await apiClient.get('/auth/me', {
        headers: { Authorization: `Bearer ${currentToken}` }
      });
      setUser(response.data);
    } catch (err) {
      console.error('Auth verification failed', err);
      logout();
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchUser(token);
    } else {
      setIsLoading(false);
    }
  }, [token]);

  const login = (newToken: string) => {
    localStorage.setItem('finora_token', newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem('finora_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
