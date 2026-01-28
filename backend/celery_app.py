from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "scrapper",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes hard limit
    task_soft_time_limit=25 * 60,  # 25 minutes soft limit
)

@celery_app.task(bind=True, name="scraper.create_scraping_task")
def create_scraping_task_celery(self, task_id: int, user_id: int, platform: str, 
                                task_type: str, input_data: dict):
    """
    Celery task to handle scraping requests
    """
    from app.core.database import SessionLocal
    from app.services.scraping_service import ScrapingTaskService
    from app.models.models import ScrapingStatus, Product
    
    db = SessionLocal()
    try:
        # Update task status to running
        ScrapingTaskService.update_task_status(
            db, task_id, ScrapingStatus.running
        )
        
        # Import scraper based on platform
        from workers.scrapers.shopee_scraper import ShopeeScraper
        from workers.scrapers.tiktok_scraper import TikTokScraper
        
        # Route to appropriate scraper
        if platform == "shopee":
            scraper = ShopeeScraper()
            results = scraper.scrape(input_data, task_type)
        elif platform == "tiktok_shop":
            scraper = TikTokScraper()
            results = scraper.scrape(input_data, task_type)
        else:
            raise ValueError(f"Unknown platform: {platform}")
        
        # Store results in database
        product_count = 0
        for product_data in results:
            product_data["user_id"] = user_id
            product_data["task_id"] = task_id
            product_data["platform"] = platform
            
            # Check if product already exists
            existing = db.query(Product).filter(
                Product.platform == platform,
                Product.external_id == product_data.get("external_id"),
                Product.user_id == user_id
            ).first()
            
            if existing:
                # Update existing product
                for key, value in product_data.items():
                    setattr(existing, key, value)
            else:
                # Create new product
                product = Product(**product_data)
                db.add(product)
            
            product_count += 1
            db.commit()
        
        # Update task with results count
        task = db.query(ScrapingTaskService.__class__).filter(
            ScrapingTaskService.__class__.id == task_id
        ).first()
        
        # Complete task
        ScrapingTaskService.update_task_status(
            db, task_id, ScrapingStatus.completed
        )
        task = db.query(ScrapingTaskService.__class__).filter(
            ScrapingTaskService.__class__.id == task_id
        ).first()
        task.results_count = product_count
        db.commit()
        
        return {
            "status": "completed",
            "task_id": task_id,
            "products_scraped": product_count
        }
    
    except Exception as e:
        ScrapingTaskService.update_task_status(
            db, task_id, ScrapingStatus.failed, str(e)
        )
        return {
            "status": "failed",
            "task_id": task_id,
            "error": str(e)
        }
    finally:
        db.close()
