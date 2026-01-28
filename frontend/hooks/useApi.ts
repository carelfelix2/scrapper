import { useEffect, useState } from 'react';
import { useAuthStore } from '@/store/authStore';
import { api } from '@/lib/api';

export const useAuth = () => {
  const [loading, setLoading] = useState(true);
  const { user, token, setUser, setToken, logout } = useAuthStore();

  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          const response = await api.getCurrentUser();
          setUser(response.data.data);
        } catch (error) {
          logout();
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, [token, setUser, logout]);

  return { user, token, loading, setToken, logout };
};

export const useScrapingTasks = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const response = await api.listTasks();
      setTasks(response.data.data.items);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
    const interval = setInterval(fetchTasks, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return { tasks, loading, error, refetch: fetchTasks };
};

export const useProducts = (platform?: string) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [total, setTotal] = useState(0);

  const fetchProducts = async (skip = 0, limit = 20) => {
    setLoading(true);
    try {
      const response = await api.listProducts(platform, skip, limit);
      setProducts(response.data.data.items);
      setTotal(response.data.data.total);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, [platform]);

  return { products, loading, error, total, refetch: fetchProducts };
};
