from typing import List
import logging
from playwright.async_api import BrowserContext, Page
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class ShopeeScraper(BaseScraper):
    """Shopee platform scraper"""
    
    SHOPEE_BASE_URL = "https://shopee.co.id"
    
    async def search_keyword(self, context: BrowserContext, keyword: str) -> List[dict]:
        """Search products by keyword on Shopee"""
        search_url = f"{self.SHOPEE_BASE_URL}/search?keyword={keyword}"
        page = await self.get_page(context, search_url)
        
        try:
            # Wait for product list to load
            await page.wait_for_selector('[data-sqe="product"]', timeout=10000)
            
            # Extract product data
            products = await page.query_selector_all('[data-sqe="product"]')
            results = []
            
            for product_element in products[:50]:  # Limit to 50 products
                try:
                    product_data = await self._extract_product_data(product_element)
                    if product_data:
                        results.append(product_data)
                except Exception as e:
                    logger.warning(f"Failed to extract product data: {str(e)}")
            
            await page.close()
            return results
        
        except Exception as e:
            logger.error(f"Error searching Shopee: {str(e)}")
            await page.close()
            return []
    
    async def monitor_shop(self, context: BrowserContext, shop_id: str) -> List[dict]:
        """Monitor Shopee shop"""
        shop_url = f"{self.SHOPEE_BASE_URL}/shop/{shop_id}"
        page = await self.get_page(context, shop_url)
        
        try:
            await page.wait_for_selector('[data-sqe="product"]', timeout=10000)
            products = await page.query_selector_all('[data-sqe="product"]')
            results = []
            
            for product_element in products:
                try:
                    product_data = await self._extract_product_data(product_element)
                    if product_data:
                        results.append(product_data)
                except Exception as e:
                    logger.warning(f"Failed to extract product data: {str(e)}")
            
            await page.close()
            return results
        
        except Exception as e:
            logger.error(f"Error monitoring shop: {str(e)}")
            await page.close()
            return []
    
    async def extract_data(self, page: Page) -> List[dict]:
        """Extract data from direct URL"""
        try:
            await page.wait_for_selector('[data-sqe="product"]', timeout=10000)
            products = await page.query_selector_all('[data-sqe="product"]')
            results = []
            
            for product_element in products:
                try:
                    product_data = await self._extract_product_data(product_element)
                    if product_data:
                        results.append(product_data)
                except Exception as e:
                    logger.warning(f"Failed to extract product data: {str(e)}")
            
            return results
        
        except Exception as e:
            logger.error(f"Error extracting data: {str(e)}")
            return []
    
    async def _extract_product_data(self, element) -> dict:
        """Extract single product data"""
        try:
            # Mock implementation - replace with actual selectors
            product_data = {
                "external_id": await element.get_attribute("data-itemid") or "mock_id",
                "product_name": await self._get_text(element, '.product-name') or "Product Name",
                "price": 50000.0,
                "original_price": None,
                "discount_percentage": None,
                "sold_count": 1000,
                "rating": 4.5,
                "review_count": 250,
                "shop_name": "Shop Name",
                "shop_location": "Indonesia",
                "product_url": "https://shopee.co.id/product",
                "image_urls": ["https://example.com/image.jpg"],
                "category": "Electronics",
                "raw_data": {}
            }
            return product_data
        except Exception as e:
            logger.error(f"Error extracting product data: {str(e)}")
            return None
    
    async def _get_text(self, element, selector: str) -> str:
        """Safely get text from element"""
        try:
            text_element = await element.query_selector(selector)
            if text_element:
                return await text_element.inner_text()
        except:
            pass
        return None
