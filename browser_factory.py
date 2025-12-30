"""
Multi-Browser WebDriver Factory
Supports Chrome, Firefox, Edge for cross-browser testing
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

import logging

# Try to import webdriver_manager
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False
    print("Warning: webdriver-manager not installed. Install with: pip install webdriver-manager")

from config import HEADLESS_MODE, WINDOW_SIZE, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT

logger = logging.getLogger(__name__)


class BrowserFactory:
    """Factory class to create WebDriver instances for different browsers"""
    
    @staticmethod
    def get_driver(browser_name: str = "chrome", headless: bool = None):
        """
        Create and return a WebDriver instance for the specified browser
        
        Args:
            browser_name: 'chrome', 'firefox', or 'edge'
            headless: Run in headless mode (overrides config if specified)
        
        Returns:
            WebDriver instance
        """
        browser = browser_name.lower()
        is_headless = headless if headless is not None else HEADLESS_MODE
        
        if browser == "chrome":
            return BrowserFactory._create_chrome_driver(is_headless)
        elif browser == "firefox":
            return BrowserFactory._create_firefox_driver(is_headless)
        elif browser == "edge":
            return BrowserFactory._create_edge_driver(is_headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}. Use 'chrome', 'firefox', or 'edge'")
    
    @staticmethod
    def _create_chrome_driver(headless: bool):
        """Create Chrome WebDriver"""
        options = ChromeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={WINDOW_SIZE[0]},{WINDOW_SIZE[1]}")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        
        try:
            if USE_WEBDRIVER_MANAGER:
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            else:
                driver = webdriver.Chrome(options=options)
            
            driver.implicitly_wait(IMPLICIT_WAIT)
            driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            logger.info("✓ Chrome WebDriver created successfully")
            return driver
            
        except Exception as e:
            logger.error(f"✗ Failed to create Chrome driver: {e}")
            raise
    
    @staticmethod
    def _create_firefox_driver(headless: bool):
        """Create Firefox WebDriver"""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument(f"--width={WINDOW_SIZE[0]}")
        options.add_argument(f"--height={WINDOW_SIZE[1]}")
        
        try:
            if USE_WEBDRIVER_MANAGER:
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)
            else:
                driver = webdriver.Firefox(options=options)
            
            driver.implicitly_wait(IMPLICIT_WAIT)
            driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            logger.info("✓ Firefox WebDriver created successfully")
            return driver
            
        except Exception as e:
            logger.error(f"✗ Failed to create Firefox driver: {e}")
            raise
    
    @staticmethod
    def _create_edge_driver(headless: bool):
        """Create Edge WebDriver"""
        options = EdgeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={WINDOW_SIZE[0]},{WINDOW_SIZE[1]}")
        
        try:
            # Try webdriver-manager first
            if USE_WEBDRIVER_MANAGER:
                try:
                    service = EdgeService(EdgeChromiumDriverManager().install())
                    driver = webdriver.Edge(service=service, options=options)
                except Exception as wdm_error:
                    # Fallback to local Edge driver if webdriver-manager fails
                    logger.warning(f"webdriver-manager failed for Edge: {wdm_error}")
                    logger.info("Trying local Edge driver...")
                    driver = webdriver.Edge(options=options)
            else:
                driver = webdriver.Edge(options=options)
            
            driver.implicitly_wait(IMPLICIT_WAIT)
            driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            logger.info("✓ Edge WebDriver created successfully")
            return driver
            
        except Exception as e:
            logger.error(f"✗ Failed to create Edge driver: {e}")
            raise
    
    @staticmethod
    def get_all_drivers(headless: bool = None) -> dict:
        """
        Create WebDriver instances for all supported browsers
        
        Returns:
            Dictionary with browser names as keys and drivers as values
        """
        drivers = {}
        browsers = ["chrome", "firefox", "edge"]
        
        for browser in browsers:
            try:
                drivers[browser] = BrowserFactory.get_driver(browser, headless)
            except Exception as e:
                logger.warning(f"Could not create {browser} driver: {e}")
                drivers[browser] = None
        
        return drivers
