from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Numeric, ForeignKey, Enum, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    enterprise = "enterprise"

class ScrapingPlatform(str, enum.Enum):
    shopee = "shopee"
    tokopedia = "tokopedia"
    tiktok_shop = "tiktok_shop"

class ScrapingStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

class ProductStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    deleted = "deleted"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.user)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255))
    avatar_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    scraping_tasks = relationship("ScrapingTask", back_populates="user", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="user", cascade="all, delete-orphan")
    collections = relationship("Collection", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("UserSubscription", back_populates="user", cascade="all, delete-orphan")

class ScrapingTask(Base):
    __tablename__ = "scraping_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    platform = Column(Enum(ScrapingPlatform), nullable=False, index=True)
    task_type = Column(String(50), nullable=False)  # 'keyword_search', 'url_scrape', 'shop_monitor'
    input_data = Column(JSON, nullable=False)
    status = Column(Enum(ScrapingStatus), default=ScrapingStatus.pending, index=True)
    results_count = Column(Integer, default=0)
    error_message = Column(Text)
    celery_task_id = Column(String(255), unique=True, index=True)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="scraping_tasks")
    products = relationship("Product", back_populates="task", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint('platform', 'external_id', 'user_id', name='uq_product_platform_id_user'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("scraping_tasks.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    platform = Column(Enum(ScrapingPlatform), nullable=False, index=True)
    external_id = Column(String(255), nullable=False, index=True)
    product_name = Column(String(500), nullable=False)
    price = Column(Numeric(15, 2))
    original_price = Column(Numeric(15, 2))
    discount_percentage = Column(Integer)
    sold_count = Column(Integer)
    rating = Column(Numeric(3, 2))
    review_count = Column(Integer)
    shop_id = Column(String(255))
    shop_name = Column(String(255))
    shop_rating = Column(Numeric(3, 2))
    shop_location = Column(String(255))
    product_url = Column(Text)
    image_urls = Column(JSON)  # Array of URLs
    description = Column(Text)
    category = Column(String(255))
    status = Column(Enum(ProductStatus), default=ProductStatus.active)
    raw_data = Column(JSON)  # Complete scraped data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="products")
    task = relationship("ScrapingTask", back_populates="products")
    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")
    collections = relationship("Collection", secondary="collection_products", back_populates="products")

class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    price = Column(Numeric(15, 2))
    discount_percentage = Column(Integer)
    sold_count = Column(Integer)
    rating = Column(Numeric(3, 2))
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    product = relationship("Product", back_populates="price_history")

class Collection(Base):
    __tablename__ = "collections"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="collections")
    products = relationship("Product", secondary="collection_products", back_populates="collections")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    alert_type = Column(String(50), nullable=False)  # 'price_drop', 'stock_alert', 'new_product'
    threshold_value = Column(Numeric(15, 2))
    is_active = Column(Boolean, default=True)
    last_triggered_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="alerts")

class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    key_hash = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="api_keys")

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price_monthly = Column(Numeric(10, 2))
    price_yearly = Column(Numeric(10, 2))
    max_scraping_jobs = Column(Integer)
    max_products = Column(Integer)
    features = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class UserSubscription(Base):
    __tablename__ = "user_subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    subscription_start = Column(DateTime(timezone=True), server_default=func.now())
    subscription_end = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan")
