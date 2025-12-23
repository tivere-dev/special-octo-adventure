import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';
import { setAccessToken, clearAccessToken } from '../services/api';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [business, setBusiness] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const data = await authService.getProfile();
      setUser(data.user);
      setBusiness(data.business || null);
    } catch (error) {
      clearAccessToken();
      setUser(null);
      setBusiness(null);
    } finally {
      setLoading(false);
    }
  };

  const signup = async (email, password, confirmPassword) => {
    try {
      setError(null);
      const data = await authService.signup(email, password, confirmPassword);
      return data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 
                          error.response?.data?.details?.email?.[0] ||
                          error.response?.data?.details?.password?.[0] ||
                          'Signup failed. Please try again.';
      setError(errorMessage);
      throw error;
    }
  };

  const login = async (email, password, rememberMe = false) => {
    try {
      setError(null);
      const data = await authService.login(email, password, rememberMe);
      setUser(data.user);
      setBusiness(data.business || null);
      return data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 
                          error.response?.data?.details?.email?.[0] ||
                          error.response?.data?.details?.password?.[0] ||
                          'Login failed. Please check your credentials.';
      setError(errorMessage);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
    } finally {
      setUser(null);
      setBusiness(null);
      clearAccessToken();
    }
  };

  const updateUser = (userData) => {
    setUser(userData);
  };

  const updateBusiness = (businessData) => {
    setBusiness(businessData);
  };

  const refreshProfile = async () => {
    try {
      const data = await authService.getProfile();
      setUser(data.user);
      setBusiness(data.business || null);
    } catch (error) {
      console.error('Failed to refresh profile:', error);
    }
  };

  const value = {
    user,
    business,
    loading,
    error,
    signup,
    login,
    logout,
    updateUser,
    updateBusiness,
    refreshProfile,
    isAuthenticated: !!user,
    hasCompletedBusinessSetup: !!business,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
