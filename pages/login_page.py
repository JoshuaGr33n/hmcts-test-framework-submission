from selenium.webdriver.common.by import By
from .base_page import BasePage
import logging
from typing import Any, Tuple, Optional


class LoginPage(BasePage):
    """Page Object for Login Page"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    LOGO = (By.CLASS_NAME, "login_logo")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    def navigate_to_login(self, base_url: str) -> bool:
        """Navigate to login page"""
        try:
            self.driver.get(base_url)
            self.logger.info(f"Navigated to: {base_url}")
            return self.is_login_page_loaded()
        except Exception as e:
            self.logger.error(f"Failed to navigate to login page: {e}")
            return False
    
    def is_login_page_loaded(self) -> bool:
        """Check if login page is loaded"""
        return (
            self.is_element_visible(self.USERNAME_INPUT) and
            self.is_element_visible(self.PASSWORD_INPUT) and
            self.is_element_visible(self.LOGIN_BUTTON)
        )
    
    def login(self, username: str, password: str) -> None:
        """Perform login action"""
        self.logger.info(f"Attempting login with username: {username}")
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> Optional[str]:
        """Get error message text if present"""
        return self.get_element_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE)