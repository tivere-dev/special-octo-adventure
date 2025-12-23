import api, { setAccessToken, clearAccessToken } from './api';

export const authService = {
  signup: async (email, password, confirmPassword) => {
    const response = await api.post('/auth/signup/', {
      email,
      password,
      confirm_password: confirmPassword,
    });
    return response.data;
  },

  login: async (email, password, rememberMe = false) => {
    const response = await api.post('/auth/login/', {
      email,
      password,
      remember_me: rememberMe,
    });
    setAccessToken(response.data.access_token);
    return response.data;
  },

  logout: async () => {
    try {
      await api.post('/auth/logout/');
    } finally {
      clearAccessToken();
    }
  },

  refreshToken: async () => {
    const response = await api.post('/auth/refresh/');
    setAccessToken(response.data.access_token);
    return response.data;
  },

  verifyEmail: async (token) => {
    const response = await api.post('/auth/verify-email/', { token });
    return response.data;
  },

  resendVerificationEmail: async () => {
    const response = await api.post('/auth/resend-verification-email/');
    return response.data;
  },

  requestPasswordReset: async (email) => {
    const response = await api.post('/auth/password-reset-request/', { email });
    return response.data;
  },

  resetPassword: async (token, newPassword, confirmPassword) => {
    const response = await api.post('/auth/password-reset/', {
      token,
      new_password: newPassword,
      confirm_password: confirmPassword,
    });
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/auth/me/');
    return response.data;
  },

  updateProfile: async (data) => {
    const response = await api.put('/auth/profile/', data);
    return response.data;
  },

  changePassword: async (currentPassword, newPassword, confirmPassword) => {
    const response = await api.put('/auth/change-password/', {
      current_password: currentPassword,
      new_password: newPassword,
      confirm_password: confirmPassword,
    });
    return response.data;
  },
};
