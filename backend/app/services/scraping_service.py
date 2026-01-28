from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.models import ScrapingTask, Product, PriceHistory
from app.schemas.schemas import ScrapingTaskInput
from app.models.models import ScrapingStatus
from typing import Optional, List
from datetime import datetime
from celery_app import create_scraping_task_celery

class ScrapingTaskService:
    @staticmethod
    def create_task(db: Session, user_id: int, task_input: ScrapingTaskInput) -> ScrapingTask:
        """Create a new scraping task"""
        task = ScrapingTask(
            user_id=user_id,
            platform=task_input.platform,
            task_type=task_input.task_type,
            input_data=task_input.input_data,
            expires_at=task_input.expires_at
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        # Send task to Celery
        celery_task = create_scraping_task_celery.delay(
            task_id=task.id,
            user_id=user_id,
            platform=task_input.platform.value,
            task_type=task_input.task_type,
            input_data=task_input.input_data
        )
        
        # Update task with Celery task ID
        task.celery_task_id = celery_task.id
        task.status = ScrapingStatus.pending
        db.commit()
        db.refresh(task)
        
        return task
    
    @staticmethod
    def get_task_by_id(db: Session, task_id: int, user_id: int) -> Optional[ScrapingTask]:
        """Get a scraping task by ID (user-scoped)"""
        return db.query(ScrapingTask).filter(
            ScrapingTask.id == task_id,
            ScrapingTask.user_id == user_id
        ).first()
    
    @staticmethod
    def get_user_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[ScrapingTask]:
        """Get all tasks for a user"""
        return db.query(ScrapingTask).filter(
            ScrapingTask.user_id == user_id
        ).order_by(desc(ScrapingTask.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_tasks_count(db: Session, user_id: int) -> int:
        """Get total tasks count for a user"""
        return db.query(ScrapingTask).filter(
            ScrapingTask.user_id == user_id
        ).count()
    
    @staticmethod
    def update_task_status(db: Session, task_id: int, status: ScrapingStatus, 
                          error_message: Optional[str] = None) -> Optional[ScrapingTask]:
        """Update task status"""
        task = db.query(ScrapingTask).filter(ScrapingTask.id == task_id).first()
        if task:
            task.status = status
            if error_message:
                task.error_message = error_message
            if status == ScrapingStatus.running and not task.started_at:
                task.started_at = datetime.utcnow()
            elif status in [ScrapingStatus.completed, ScrapingStatus.failed]:
                task.completed_at = datetime.utcnow()
            db.commit()
            db.refresh(task)
        return task

class ProductService:
    @staticmethod
    def create_product(db: Session, user_id: int, product_data: dict) -> Product:
        """Create a new product"""
        product = Product(user_id=user_id, **product_data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: int, user_id: int) -> Optional[Product]:
        """Get product by ID (user-scoped)"""
        return db.query(Product).filter(
            Product.id == product_id,
            Product.user_id == user_id
        ).first()
    
    @staticmethod
    def get_user_products(db: Session, user_id: int, platform: Optional[str] = None,
                         skip: int = 0, limit: int = 20) -> List[Product]:
        """Get user's products with optional platform filter"""
        query = db.query(Product).filter(Product.user_id == user_id)
        if platform:
            query = query.filter(Product.platform == platform)
        return query.order_by(desc(Product.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_products_by_task(db: Session, task_id: int, user_id: int) -> List[Product]:
        """Get all products from a scraping task"""
        return db.query(Product).filter(
            Product.task_id == task_id,
            Product.user_id == user_id
        ).all()
    
    @staticmethod
    def get_price_history(db: Session, product_id: int, user_id: int, 
                         limit: int = 50) -> List[PriceHistory]:
        """Get price history for a product"""
        return db.query(PriceHistory).filter(
            PriceHistory.product_id == product_id,
            PriceHistory.user_id == user_id
        ).order_by(desc(PriceHistory.recorded_at)).limit(limit).all()
    
    @staticmethod
    def record_price_snapshot(db: Session, product_id: int, user_id: int) -> PriceHistory:
        """Record current product state to price history"""
        product = db.query(Product).filter(
            Product.id == product_id,
            Product.user_id == user_id
        ).first()
        
        if not product:
            return None
        
        history = PriceHistory(
            product_id=product_id,
            user_id=user_id,
            price=product.price,
            discount_percentage=product.discount_percentage,
            sold_count=product.sold_count,
            rating=product.rating
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history
    
    @staticmethod
    def search_products(db: Session, user_id: int, query: str, 
                       skip: int = 0, limit: int = 20) -> List[Product]:
        """Search products by name or category"""
        return db.query(Product).filter(
            Product.user_id == user_id,
            (Product.product_name.ilike(f"%{query}%") | 
             Product.category.ilike(f"%{query}%"))
        ).order_by(desc(Product.created_at)).offset(skip).limit(limit).all()

# Services package
