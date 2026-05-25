import os
import logging
from pathlib import Path
from typing import Any, Dict, Optional
import yaml
import json


class Config:
    """Configuration management system for Realtor Agent"""

    _instance = None
    _config = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Load configuration from environment and config files"""
        base_dir = Path(__file__).parent.parent.parent

        # Default configuration
        self._config = {
            "app": {
                "name": "Realtor Agent",
                "version": "1.0.0",
                "debug": os.getenv("DEBUG", "False").lower() == "true",
                "secret_key": os.getenv("SECRET_KEY", "dev-secret-key-change-in-production"),
            },
            "database": {
                "url": os.getenv("DATABASE_URL", f"sqlite:///{base_dir}/data/realtor_agent.db"),
                "echo": os.getenv("DB_ECHO", "False").lower() == "true",
                "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
                "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),
            },
            "redis": {
                "host": os.getenv("REDIS_HOST", "localhost"),
                "port": int(os.getenv("REDIS_PORT", "6379")),
                "db": int(os.getenv("REDIS_DB", "0")),
                "password": os.getenv("REDIS_PASSWORD"),
            },
            "celery": {
                "broker_url": os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
                "result_backend": os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
            },
            "security": {
                "jwt_secret": os.getenv("JWT_SECRET", "jwt-secret-change-in-production"),
                "jwt_algorithm": "HS256",
                "jwt_expiration_hours": int(os.getenv("JWT_EXPIRATION_HOURS", "24")),
                "password_min_length": 8,
                "max_login_attempts": 5,
                "lockout_duration_minutes": 30,
            },
            "api": {
                "rate_limit_per_minute": int(os.getenv("API_RATE_LIMIT", "60")),
                "max_request_size_mb": int(os.getenv("MAX_REQUEST_SIZE_MB", "10")),
            },
            "bots": {
                "max_retries": int(os.getenv("BOT_MAX_RETRIES", "3")),
                "retry_delay_seconds": int(os.getenv("BOT_RETRY_DELAY", "60")),
                "timeout_seconds": int(os.getenv("BOT_TIMEOUT", "300")),
            },
            "logging": {
                "level": os.getenv("LOG_LEVEL", "INFO"),
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": os.getenv("LOG_FILE", f"{base_dir}/logs/realtor_agent.log"),
            },
        }

        # Load from config file if exists
        config_file = base_dir / "config.yaml"
        if config_file.exists():
            with open(config_file, "r") as f:
                file_config = yaml.safe_load(f)
                self._deep_update(self._config, file_config)

    def _deep_update(self, base_dict: Dict, update_dict: Dict) -> Dict:
        """Deep update dictionary"""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict:
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
        return base_dict

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation key"""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any):
        """Set configuration value by dot notation key"""
        keys = key.split(".")
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    def to_dict(self) -> Dict:
        """Return configuration as dictionary"""
        return self._config.copy()

    @property
    def version(self):
        return self.get("app.version")

    @property
    def bots(self):
        return self.get("bots", {})

    @property
    def database(self):
        return self.get("database", {})

    @property
    def redis(self):
        return self.get("redis", {})

    @property
    def celery(self):
        return self.get("celery", {})


# Global config instance
config = Config()

# Alias for compatibility
SystemConfig = Config


def load_config(config_path=None):
    """Load configuration from file or return global config"""
    if config_path and Path(config_path).exists():
        # Load from specific file
        with open(config_path, "r") as f:
            file_config = yaml.safe_load(f)
            config._deep_update(config._config, file_config)
    return config
