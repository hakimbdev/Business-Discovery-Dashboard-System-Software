"""
Configuration Manager
Handles loading and accessing configuration from YAML files
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, List


class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.settings: Dict[str, Any] = {}
        self.keywords: Dict[str, Any] = {}
        self._load_configs()
    
    def _load_configs(self):
        """Load all configuration files"""
        try:
            # Load main settings
            settings_path = self.config_dir / "settings.yaml"
            if settings_path.exists():
                with open(settings_path, 'r', encoding='utf-8') as f:
                    self.settings = yaml.safe_load(f)
            
            # Load keywords configuration
            keywords_path = self.config_dir / "keywords.yaml"
            if keywords_path.exists():
                with open(keywords_path, 'r', encoding='utf-8') as f:
                    self.keywords = yaml.safe_load(f)
                    
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        Example: config.get('database.type')
        """
        keys = key_path.split('.')
        value = self.settings
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_keywords(self, category: str = None) -> Dict[str, Any]:
        """Get keywords for a specific category or all categories"""
        if category:
            return self.keywords.get('business_categories', {}).get(category, {})
        return self.keywords.get('business_categories', {})
    
    def get_location_signals(self) -> Dict[str, List[str]]:
        """Get all location signals for Nigeria"""
        return self.keywords.get('location_signals', {})
    
    def get_all_category_keywords(self) -> List[str]:
        """Get all keywords from all categories as a flat list"""
        keywords = []
        categories = self.keywords.get('business_categories', {})
        
        for category_data in categories.values():
            keywords.extend(category_data.get('keywords', []))
        
        return list(set(keywords))  # Remove duplicates
    
    def get_detection_settings(self) -> Dict[str, Any]:
        """Get detection-specific settings"""
        return self.keywords.get('detection', {})
    
    def get_api_key(self, service: str, key: str = None) -> str:
        """
        Get API key for a specific service
        Example: config.get_api_key('facebook', 'access_token')
        """
        api_keys = self.settings.get('api_keys', {}).get(service, {})
        
        if key:
            return api_keys.get(key, '')
        return api_keys
    
    def is_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled"""
        scheduler = self.settings.get('scheduler', {})
        return scheduler.get(f'enable_{feature}', False)
    
    def get_rate_limit(self, service: str) -> Dict[str, Any]:
        """Get rate limiting configuration for a service"""
        rate_limits = self.settings.get('rate_limiting', {})
        return {
            'rpm': rate_limits.get(f'{service}_rpm', 10),
            'delay_min': rate_limits.get('request_delay_min', 2),
            'delay_max': rate_limits.get('request_delay_max', 5)
        }
    
    def get_user_agents(self) -> List[str]:
        """Get list of user agents for rotation"""
        return self.settings.get('scraping', {}).get('user_agents', [])
    
    def reload(self):
        """Reload configuration files"""
        self._load_configs()


# Global configuration instance
config = ConfigManager()

