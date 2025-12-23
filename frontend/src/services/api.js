import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

let accessToken = null;
let tokenRefreshPromise = null;

export const setAccessToken = (token) => {
  accessToken = token;
};

export const getAccessToken = () => {
  return accessToken;
};

export const clearAccessToken = () => {
  accessToken = null;
};

const isTokenExpired = (token) => {
  if (!token) return true;
  try {
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    return decoded.exp < currentTime + 60;
  } catch (error) {
    return true;
  }
};

const refreshAccessToken = async () => {
  if (tokenRefreshPromise) {
    return tokenRefreshPromise;
  }

  tokenRefreshPromise = axios.post(
    `${API_BASE_URL}/auth/refresh/`,
    {},
    { withCredentials: true }
  ).then(response => {
    const newAccessToken = response.data.access_token;
    setAccessToken(newAccessToken);
    tokenRefreshPromise = null;
    return newAccessToken;
  }).catch(error => {
    tokenRefreshPromise = null;
    clearAccessToken();
    throw error;
  });

  return tokenRefreshPromise;
};

api.interceptors.request.use(
  async (config) => {
    if (accessToken && isTokenExpired(accessToken)) {
      try {
        await refreshAccessToken();
      } catch (error) {
        clearAccessToken();
        window.location.href = '/login';
        return Promise.reject(error);
      }
    }

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        await refreshAccessToken();
        return api(originalRequest);
      } catch (refreshError) {
        clearAccessToken();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
