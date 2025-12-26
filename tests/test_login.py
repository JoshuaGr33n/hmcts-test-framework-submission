import pytest
import logging
import allure
from typing import Dict
from utilities.config_reader import ConfigReader

logger = logging.getLogger(__name__)
config = ConfigReader()


@allure.feature("Login Functionality")
@allure.story("User Authentication")
class TestLogin:
    """Test suite for login functionality"""
    
    @allure.title("TC001 - Successful login with valid credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_successful_login(self, driver, login_page, valid_credentials):
        """
        Test successful login with valid credentials
        Expected: User should be redirected to products page
        """
        logger.info("Starting test: Successful login with valid credentials")
        
        # Navigate and login
        assert login_page.navigate_to_login(config.get_base_url()), \
            "Login page failed to load"
        
        login_page.login(
            valid_credentials['username'],
            valid_credentials['password']
        )
        
        # Verify login success by checking URL change
        current_url = driver.current_url
        assert "inventory.html" in current_url, \
            f"Login failed, not redirected to inventory. Current URL: {current_url}"
        
        logger.info("Login successful, user redirected to products page")
        allure.attach(driver.get_screenshot_as_png(), 
                     name="successful_login",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("TC002 - Login with invalid username")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    @pytest.mark.parametrize("username,password,expected_error", [
        ("invalid_user", "secret_sauce", "Username and password do not match"),
        ("", "secret_sauce", "Username is required"),
    ])
    def test_login_invalid_username(self, driver, login_page, username, password, expected_error):
        """
        Test login with invalid username
        Expected: Error message should be displayed
        """
        logger.info(f"Testing login with invalid username: {username}")
        
        assert login_page.navigate_to_login(config.get_base_url()), \
            "Login page failed to load"
        
        login_page.login(username, password)
        
        # Verify error message
        assert login_page.is_error_displayed(), \
            "Error message should be displayed for invalid username"
        
        error_text = login_page.get_error_message()
        assert error_text is not None, "Error message text should not be None"
        assert "Epic sadface" in error_text, \
            f"Expected error message not found. Got: {error_text}"
        
        logger.info(f"Login failed as expected with error: {error_text}")
        allure.attach(driver.get_screenshot_as_png(),
                     name=f"invalid_username_{username}",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("TC003 - Login with invalid password")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_login_invalid_password(self, driver, login_page):
        """
        Test login with invalid password
        Expected: Error message should be displayed
        """
        logger.info("Testing login with invalid password")
        
        assert login_page.navigate_to_login(config.get_base_url()), \
            "Login page failed to load"
        
        login_page.login("standard_user", "wrong_password")
        
        # Verify error message
        assert login_page.is_error_displayed(), \
            "Error message should be displayed for invalid password"
        
        error_text = login_page.get_error_message()
        assert error_text is not None, "Error message text should not be None"
        assert "Epic sadface" in error_text, \
            f"Expected error message not found. Got: {error_text}"
        
        logger.info(f"Login failed as expected with error: {error_text}")
    
    @allure.title("TC004 - Login with locked out user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_locked_user(self, driver, login_page):
        """
        Test login with locked out user
        Expected: User should see locked out error message
        """
        logger.info("Testing login with locked out user")
        
        assert login_page.navigate_to_login(config.get_base_url()), \
            "Login page failed to load"
        
        login_page.login("locked_out_user", "secret_sauce")
        
        # Verify specific error for locked user
        assert login_page.is_error_displayed(), \
            "Error message should be displayed for locked user"
        
        error_text = login_page.get_error_message()
        assert error_text is not None, "Error message text should not be None"
        assert "locked out" in error_text.lower(), \
            f"Expected 'locked out' in error message. Got: {error_text}"
        
        logger.info(f"Locked user login prevented with error: {error_text}")
        allure.attach(driver.get_screenshot_as_png(),
                     name="locked_user_error",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("TC005 - Login with empty credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_empty_credentials(self, driver, login_page):
        """
        Test login with empty username and password
        Expected: Error message for required fields
        """
        logger.info("Testing login with empty credentials")
        
        assert login_page.navigate_to_login(config.get_base_url()), \
            "Login page failed to load"
        
        # Click login without entering credentials
        login_page.click_element(login_page.LOGIN_BUTTON)
        
        # Verify error message
        assert login_page.is_error_displayed(), \
            "Error message should be displayed for empty credentials"
        
        error_text = login_page.get_error_message()
        assert error_text is not None, "Error message text should not be None"
        assert "Username is required" in error_text, \
            f"Expected 'Username is required' in error message. Got: {error_text}"
        
        logger.info(f"Empty credentials rejected with error: {error_text}")
    
    @allure.title("TC006 - Verify login page elements")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.smoke
    def test_login_page_elements(self, driver, login_page):
        """
        Verify all required elements are present on login page
        """
        logger.info("Verifying login page elements")
        
        assert login_page.navigate_to_login(config.get_base_url()), \
            "Login page failed to load"
        
        # Check all elements are visible
        assert login_page.is_element_visible(login_page.USERNAME_INPUT), \
            "Username input should be visible"
        assert login_page.is_element_visible(login_page.PASSWORD_INPUT), \
            "Password input should be visible"
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON), \
            "Login button should be visible"
        assert login_page.is_element_visible(login_page.LOGO), \
            "Logo should be visible"
        
        logger.info("All login page elements are present and visible")
        allure.attach(driver.get_screenshot_as_png(),
                     name="login_page_elements",
                     attachment_type=allure.attachment_type.PNG)