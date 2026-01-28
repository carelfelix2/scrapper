from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.models import ScrapingPlatform, ScrapingStatus, ProductStatus

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication Schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user: UserResponse

# Scraping Task Schemas
class ScrapingTaskInput(BaseModel):
    platform: ScrapingPlatform
    task_type: str  # 'keyword_search', 'url_scrape', 'shop_monitor'
    input_data: Dict[str, Any]
    expires_at: Optional[datetime] = None

class ScrapingTaskResponse(BaseModel):
    id: int
    platform: ScrapingPlatform
    task_type: str
    status: ScrapingStatus
    results_count: int
    celery_task_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True

class ScrapingTaskDetailResponse(ScrapingTaskResponse):
    input_data: Dict[str, Any]
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

# Product Schemas
class ProductBase(BaseModel):
    product_name: str
    price: Optional[float] = None
    original_price: Optional[float] = None
    discount_percentage: Optional[int] = None
    sold_count: Optional[int] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    shop_name: Optional[str] = None
    shop_location: Optional[str] = None

class ProductCreate(ProductBase):
    platform: ScrapingPlatform
    external_id: str
    product_url: Optional[str] = None
    image_urls: Optional[List[str]] = None
    description: Optional[str] = None
    category: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None

class ProductResponse(ProductBase):
    id: int
    platform: ScrapingPlatform
    external_id: str
    product_url: Optional[str] = None
    image_urls: Optional[List[str]] = None
    description: Optional[str] = None
    category: Optional[str] = None
    status: ProductStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProductDetailResponse(ProductResponse):
    shop_id: Optional[str] = None
    shop_rating: Optional[float] = None
    raw_data: Optional[Dict[str, Any]] = None

# Price History Schemas
class PriceHistoryResponse(BaseModel):
    price: Optional[float]
    discount_percentage: Optional[int]
    sold_count: Optional[int]
    rating: Optional[float]
    recorded_at: datetime
    
    class Config:
        from_attributes = True

class ProductWithHistoryResponse(ProductResponse):
    price_history: List[PriceHistoryResponse]

# Collection Schemas
class CollectionBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False

class CollectionCreate(CollectionBase):
    pass

class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None

class CollectionResponse(CollectionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CollectionDetailResponse(CollectionResponse):
    products: List[ProductResponse]

# Alert Schemas
class AlertBase(BaseModel):
    alert_type: str
    threshold_value: Optional[float] = None
    is_active: bool = True

class AlertCreate(AlertBase):
    product_id: Optional[int] = None

class AlertResponse(AlertBase):
    id: int
    product_id: Optional[int] = None
    last_triggered_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Pagination
class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[Any]

# Generic Response
class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
