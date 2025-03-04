"""
Configuration manager for the application.
Handles loading, saving, and managing configurations.
"""
import os
import json
from typing import Dict, Optional
from models.config_model import ConfigModel

class ConfigManager:
    """
    Manages application configurations.
    Provides methods for loading, saving, and managing configurations.
    """
    
    def __init__(self, config_dir=None):
        """
        Initialize the configuration manager.
        
        Args:
            config_dir: Directory to store configurations. If None, uses default.
        """
        if config_dir is None:
            # Use default config directory in user's home directory
            home_dir = os.path.expanduser("~")
            self.config_dir = os.path.join(home_dir, ".flexipy", "configs")
        else:
            self.config_dir = config_dir
            
        # Create config directory if it doesn't exist
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Cache for loaded configurations
        self.configs = {}
    
    def load_all_configs(self):
        """
        Load all configurations from the config directory.
        
        Returns:
            Dict: Dictionary of configuration names and their models
        """
        self.configs = {}
        
        # Get all JSON files in the config directory
        if not os.path.exists(self.config_dir):
            return self.configs
            
        for filename in os.listdir(self.config_dir):
            if filename.endswith(".json"):
                config_name = filename[:-5]  # Remove .json extension
                config_path = os.path.join(self.config_dir, filename)
                
                try:
                    with open(config_path, "r") as f:
                        config_data = json.load(f)
                        self.configs[config_name] = ConfigModel.from_dict(config_data)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error loading configuration {config_name}: {e}")
        
        return self.configs
    
    def get_config(self, name):
        """
        Get a configuration by name.
        
        Args:
            name: Name of the configuration
            
        Returns:
            ConfigModel: Configuration model, or None if not found
        """
        return self.configs.get(name)
    
    def save_config(self, name, config):
        """
        Save a configuration.
        
        Args:
            name: Name of the configuration
            config: Configuration model to save
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        config_path = os.path.join(self.config_dir, f"{name}.json")
        
        try:
            with open(config_path, "w") as f:
                json.dump(config.to_dict(), f, indent=2)
                
            # Update cache
            self.configs[name] = config
            return True
        except IOError as e:
            print(f"Error saving configuration {name}: {e}")
            return False