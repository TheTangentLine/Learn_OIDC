import api from './api';

export const authService = {
  // Sign up a new user
  signup: async (username, email, password) => {
    const response = await api.post('/auth/signup', {
      username,
      email,
      password,
    });
    return response.data;
  },

  // Login with username and password
  login: async (username, password) => {
    const response = await api.post('/auth/login', {
      username,
      password,
    });
    
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }
    
    return response.data;
  },

  // Logout
  logout: () => {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },

  // Google OAuth login
  googleLogin: () => {
    window.location.href = 'http://localhost:8000/auth/login/google';
  },

  // Refresh access token
  refreshToken: async () => {
    const response = await api.post('/auth/refresh');
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }
    return response.data;
  },
};


