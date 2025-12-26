from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from typing import Any, Tuple, Optional


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.wait = WebDriverWait(
            driver, 
            20,  # Will be overridden by config
            poll_frequency=0.5
        )
    
    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> Optional[Any]:
        """
        Find element with explicit wait
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout
        Returns:
            WebElement or None
        """
        try:
            wait_timeout = self.wait._timeout if timeout is None else timeout
            element = WebDriverWait(self.driver, wait_timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.info(f"Found element with locator: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            return None
    
    def click_element(self, locator: Tuple[str, str]) -> bool:
        """Click on element with wait"""
        element = self.find_element(locator)
        if element:
            try:
                element.click()
                self.logger.info(f"Clicked element with locator: {locator}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to click element: {locator}. Error: {e}")
                return False
        return False
    
    def enter_text(self, locator: Tuple[str, str], text: str) -> bool:
        """Enter text into element"""
        element = self.find_element(locator)
        if element:
            try:
                element.clear()
                element.send_keys(text)
                self.logger.info(f"Entered text '{text}' into element: {locator}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to enter text into element: {locator}. Error: {e}")
                return False
        return False
    
    def get_element_text(self, locator: Tuple[str, str]) -> Optional[str]:
        """Get text from element"""
        element = self.find_element(locator)
        return element.text if element else None
    
    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """Check if element is visible"""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except TimeoutException:
            return False
    
    def take_screenshot(self, filename: str) -> bool:
        """Take screenshot and save to screenshots folder"""
        try:
            import os
            screenshot_dir = os.path.join(os.path.dirname(__file__), '..', 'screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)
            path = os.path.join(screenshot_dir, f"{filename}.png")
            self.driver.save_screenshot(path)
            self.logger.info(f"Screenshot saved: {path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")
            return False