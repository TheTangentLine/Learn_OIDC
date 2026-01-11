import React, { createContext, useState, useContext, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated on mount
    const checkAuth = () => {
      const authenticated = authService.isAuthenticated();
      setIsAuthenticated(authenticated);
      setLoading(false);
    };

    checkAuth();

    // Check for access token in URL (from OAuth callback)
    const urlParams = new URLSearchParams(window.location.search);
    const accessToken = urlParams.get('access_token');
    
    if (accessToken) {
      localStorage.setItem('access_token', accessToken);
      setIsAuthenticated(true);
      // Clean up URL
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  const login = async (username, password) => {
    try {
      await authService.login(username, password);
      setIsAuthenticated(true);
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      };
    }
  };

  const signup = async (username, email, password) => {
    try {
      await authService.signup(username, email, password);
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Signup failed' 
      };
    }
  };

  const logout = () => {
    authService.logout();
    setIsAuthenticated(false);
  };

  const googleLogin = () => {
    authService.googleLogin();
  };

  return (
    <AuthContext.Provider 
      value={{ 
        isAuthenticated, 
        login, 
        signup, 
        logout, 
        googleLogin,
        loading 
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};


