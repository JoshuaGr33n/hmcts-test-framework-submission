import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from pages.login_page import LoginPage
from utilities.config_reader import ConfigReader
import os
from datetime import datetime


def setup_logging():
    """Configure logging"""
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(
        log_dir, 
        f"test_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()


@pytest.fixture(scope="session")
def config():
    """Fixture to load configuration"""
    return ConfigReader()


@pytest.fixture(scope="function")
def driver(config):
    """WebDriver fixture with setup and teardown"""
    browser_name = config.get_browser()
    base_url = config.get_base_url()
    
    driver = None
    try:
        if browser_name.lower() == "chrome":
            chrome_options = ChromeOptions()
            chrome_options.binary_location = "/Applications/Chromium.app/Contents/MacOS/Chromium"
            if config.config.getboolean('BROWSER', 'HEADLESS'):
                chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # driver = webdriver.Chrome(
            #     service=ChromeService(ChromeDriverManager().install()),
            #     options=chrome_options
            # )
            driver = webdriver.Chrome(options=chrome_options)
        elif browser_name.lower() == "firefox":
            firefox_options = FirefoxOptions()
            if config.config.getboolean('BROWSER', 'HEADLESS'):
                firefox_options.add_argument("--headless")
            driver = webdriver.Firefox(
                executable_path=GeckoDriverManager().install(),
                options=firefox_options
            )
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        driver.implicitly_wait(config.get_timeout())
        driver.maximize_window()
        logger.info(f"{browser_name} browser started")
        
        # Navigate to base URL
        driver.get(base_url)
        logger.info(f"Navigated to base URL: {base_url}")
        
        yield driver
        
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        raise
    finally:
        if driver:
            driver.quit()
            logger.info("Browser closed")


@pytest.fixture(scope="function")
def login_page(driver):
    """Fixture to initialize LoginPage"""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def valid_credentials(config):
    """Fixture to provide valid credentials"""
    return config.get_credentials()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to take screenshot on test failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs.get('driver')
            if driver:
                login_page = LoginPage(driver)
                screenshot_name = f"failure_{item.name}_{datetime.now().strftime('%H%M%S')}"
                login_page.take_screenshot(screenshot_name)
                logger.info(f"Screenshot taken for failed test: {item.name}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")