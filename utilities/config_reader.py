import configparser
import os
from typing import Dict, Any


class ConfigReader:
    """Reads configuration from config.ini file"""
    
    def __init__(self, config_file: str = "config.ini"):
        self.config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), '..', config_file)
        self.config.read(config_path)
    
    def get_base_url(self) -> str:
        """Get the base URL from configuration"""
        return self.config.get('APPLICATION', 'BASE_URL')
    
    def get_browser(self) -> str:
        """Get browser name from configuration"""
        return self.config.get('BROWSER', 'BROWSER_NAME')
    
    def get_timeout(self) -> int:
        """Get implicit wait timeout"""
        return self.config.getint('WAIT', 'IMPLICIT_WAIT')
    
    def get_credentials(self) -> Dict[str, str]:
        """Get test credentials"""
        return {
            'username': os.getenv('SAUCE_USERNAME', 'standard_user'),
            'password': os.getenv('SAUCE_PASSWORD', 'secret_sauce')
        }