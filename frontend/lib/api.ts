import axios from 'axios';
import { useAuthStore } from '@/store/authStore';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const api = {
  // Auth endpoints
  login: (email: string, password: string) =>
    apiClient.post('/api/v1/auth/login', { email, password }),
  getCurrentUser: () =>
    apiClient.get('/api/v1/auth/me'),

  // Tasks endpoints
  createScrapingTask: (data: any) =>
    apiClient.post('/api/v1/tasks', data),
  getTask: (taskId: number) =>
    apiClient.get(`/api/v1/tasks/${taskId}`),
  listTasks: (skip = 0, limit = 10) =>
    apiClient.get(`/api/v1/tasks?skip=${skip}&limit=${limit}`),

  // Products endpoints
  listProducts: (platform?: string, skip = 0, limit = 20) =>
    apiClient.get(`/api/v1/products?platform=${platform || ''}&skip=${skip}&limit=${limit}`),
  getProduct: (productId: number) =>
    apiClient.get(`/api/v1/products/${productId}`),
  getProductHistory: (productId: number, limit = 50) =>
    apiClient.get(`/api/v1/products/${productId}/history?limit=${limit}`),
  searchProducts: (query: string, skip = 0, limit = 20) =>
    apiClient.get(`/api/v1/products/search/${query}?skip=${skip}&limit=${limit}`),

  // Health check
  healthCheck: () =>
    apiClient.get('/health'),
};

export default apiClient;
