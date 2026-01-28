import asyncio
import random
from typing import List, Optional
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
import logging

logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
]

PROXY_LIST = [
    # Add your proxies here
    # "http://proxy1.com:port",
    # "http://proxy2.com:port",
]

class BrowserManager:
    """Manage browser instances with proxy rotation and user-agent switching"""
    
    def __init__(self, headless: bool = True, browser_timeout: int = 30000, 
                 proxy_list: Optional[List[str]] = None):
        self.headless = headless
        self.browser_timeout = browser_timeout
        self.proxy_list = proxy_list or PROXY_LIST
        self.browser: Optional[Browser] = None
        
    async def launch_browser(self) -> Browser:
        """Launch browser instance"""
        playwright = await async_playwright().start()
        
        launch_args = {
            "headless": self.headless,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
            ]
        }
        
        # Add proxy if available
        if self.proxy_list:
            proxy = random.choice(self.proxy_list)
            launch_args["proxy"] = {"server": proxy}
            logger.info(f"Using proxy: {proxy}")
        
        self.browser = await playwright.chromium.launch(**launch_args)
        return self.browser
    
    async def create_context(self) -> BrowserContext:
        """Create a new browser context with random user-agent"""
        if not self.browser:
            await self.launch_browser()
        
        user_agent = random.choice(USER_AGENTS)
        context = await self.browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1280, "height": 720},
            timezone_id="Asia/Jakarta",  # Indonesia timezone
            locale="id-ID",
            permissions=[],
        )
        
        # Add stealth scripts to avoid detection
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
        """)
        
        return context
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()

class BaseScraper:
    """Base scraper class with common functionality"""
    
    def __init__(self, headless: bool = True, browser_timeout: int = 30000,
                 proxy_list: Optional[List[str]] = None):
        self.browser_manager = BrowserManager(headless, browser_timeout, proxy_list)
        self.timeout = browser_timeout
    
    async def get_page(self, context: BrowserContext, url: str) -> Page:
        """Create and navigate to page"""
        page = await context.new_page()
        page.set_default_timeout(self.timeout)
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)
            await page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            logger.error(f"Failed to load {url}: {str(e)}")
        
        return page
    
    async def extract_data(self, page: Page) -> List[dict]:
        """Extract data from page (to be implemented by subclasses)"""
        raise NotImplementedError
    
    def scrape(self, input_data: dict, task_type: str) -> List[dict]:
        """Synchronous wrapper for async scraping"""
        return asyncio.run(self._scrape_async(input_data, task_type))
    
    async def _scrape_async(self, input_data: dict, task_type: str) -> List[dict]:
        """Async scraping implementation"""
        results = []
        context = None
        
        try:
            context = await self.browser_manager.create_context()
            
            if task_type == "url_scrape":
                url = input_data.get("url")
                if url:
                    page = await self.get_page(context, url)
                    results = await self.extract_data(page)
                    await page.close()
            
            elif task_type == "keyword_search":
                keyword = input_data.get("keyword")
                if keyword:
                    results = await self.search_keyword(context, keyword)
            
            elif task_type == "shop_monitor":
                shop_id = input_data.get("shop_id")
                if shop_id:
                    results = await self.monitor_shop(context, shop_id)
        
        except Exception as e:
            logger.error(f"Scraping error: {str(e)}")
        
        finally:
            if context:
                await context.close()
        
        return results
    
    async def search_keyword(self, context: BrowserContext, keyword: str) -> List[dict]:
        """Search for keyword (to be implemented by subclasses)"""
        raise NotImplementedError
    
    async def monitor_shop(self, context: BrowserContext, shop_id: str) -> List[dict]:
        """Monitor shop (to be implemented by subclasses)"""
        raise NotImplementedError
