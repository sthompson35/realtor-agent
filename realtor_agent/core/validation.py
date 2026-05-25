import re
import html
from typing import Any, Dict, List, Optional
from ..core.logger import get_logger

logger = get_logger(__name__)


class InputValidator:
    """Input validation and sanitization utilities"""

    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """Sanitize string input"""
        if not isinstance(value, str):
            return ""

        # Remove null bytes
        value = value.replace("\x00", "")

        # Trim whitespace
        value = value.strip()

        # Limit length
        value = value[:max_length]

        # Escape HTML
        value = html.escape(value)

        return value

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        # Remove common separators
        cleaned = re.sub(r"[\s\-\(\)\.]", "", phone)
        # Check if it's a valid phone number (10-15 digits)
        return bool(re.match(r"^\+?1?\d{10,15}$", cleaned))

    @staticmethod
    def validate_zipcode(zipcode: str) -> bool:
        """Validate US ZIP code format"""
        return bool(re.match(r"^\d{5}(-\d{4})?$", zipcode))

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        pattern = r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$"
        return bool(re.match(pattern, url))

    @staticmethod
    def sanitize_sql(value: str) -> str:
        """Sanitize input to prevent SQL injection"""
        # Remove SQL keywords and special characters
        dangerous_patterns = [
            r"(\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b|\bCREATE\b)",
            r"(--|;|\/\*|\*\/)",
            r"(\bOR\b|\bAND\b).*=.*",
        ]

        for pattern in dangerous_patterns:
            value = re.sub(pattern, "", value, flags=re.IGNORECASE)

        return value

    @staticmethod
    def validate_json_keys(data: Dict, allowed_keys: List[str]) -> bool:
        """Validate that JSON only contains allowed keys"""
        return all(key in allowed_keys for key in data.keys())

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to prevent directory traversal"""
        # Remove path separators and special characters
        filename = re.sub(r'[/\\:*?"<>|]', "", filename)
        # Remove leading dots
        filename = filename.lstrip(".")
        # Limit length
        filename = filename[:255]
        return filename

    @staticmethod
    def validate_integer(value: Any, min_val: int = None, max_val: int = None) -> bool:
        """Validate integer value with optional range"""
        try:
            int_val = int(value)
            if min_val is not None and int_val < min_val:
                return False
            if max_val is not None and int_val > max_val:
                return False
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_float(value: Any, min_val: float = None, max_val: float = None) -> bool:
        """Validate float value with optional range"""
        try:
            float_val = float(value)
            if min_val is not None and float_val < min_val:
                return False
            if max_val is not None and float_val > max_val:
                return False
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_required_fields(data: Dict, required_fields: List[str]) -> tuple[bool, List[str]]:
        """Validate that all required fields are present"""
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        return len(missing_fields) == 0, missing_fields


class CSRFProtection:
    """CSRF token generation and validation"""

    @staticmethod
    def generate_token() -> str:
        """Generate a CSRF token"""
        import secrets

        return secrets.token_urlsafe(32)

    @staticmethod
    def validate_token(token: str, session_token: str) -> bool:
        """Validate CSRF token"""
        import hmac

        return hmac.compare_digest(token, session_token)


# Global validator instance
input_validator = InputValidator()
csrf_protection = CSRFProtection()
