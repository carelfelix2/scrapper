export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string | null;
  role: "admin" | "user" | "enterprise";
  is_active: boolean;
  is_verified: boolean;
  avatar_url: string | null;
  created_at: string;
}

export interface ScrapingTask {
  id: number;
  platform: "shopee" | "tokopedia" | "tiktok_shop";
  task_type: string;
  status: "pending" | "running" | "completed" | "failed";
  results_count: number;
  celery_task_id: string | null;
  created_at: string;
  updated_at: string;
  error_message: string | null;
}

export interface Product {
  id: number;
  platform: "shopee" | "tokopedia" | "tiktok_shop";
  external_id: string;
  product_name: string;
  price: number | null;
  original_price: number | null;
  discount_percentage: number | null;
  sold_count: number | null;
  rating: number | null;
  review_count: number | null;
  shop_name: string | null;
  shop_location: string | null;
  product_url: string | null;
  image_urls: string[] | null;
  description: string | null;
  category: string | null;
  status: "active" | "inactive" | "deleted";
  created_at: string;
  updated_at: string;
}

export interface PriceHistory {
  price: number | null;
  discount_percentage: number | null;
  sold_count: number | null;
  rating: number | null;
  recorded_at: string;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T | null;
}

export interface PaginatedData<T> {
  total: number;
  page: number;
  page_size: number;
  items: T[];
}
