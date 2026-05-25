import time
import functools
from typing import Callable, Any, Optional
from ..core.logger import get_logger
from ..core.config import config

logger = get_logger(__name__)


class RetryStrategy:
    """Retry strategy for bot operations"""

    def __init__(self, max_retries: int = None, delay: int = None, backoff: float = 2.0):
        self.max_retries = max_retries or config.get("bots.max_retries", 3)
        self.delay = delay or config.get("bots.retry_delay_seconds", 60)
        self.backoff = backoff

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            retries = 0
            current_delay = self.delay

            while retries <= self.max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries > self.max_retries:
                        logger.error(f"Max retries ({self.max_retries}) exceeded for {func.__name__}: {e}")
                        raise

                    logger.warning(f"Retry {retries}/{self.max_retries} for {func.__name__} after error: {e}")
                    time.sleep(current_delay)
                    current_delay *= self.backoff

        return wrapper


class BotErrorHandler:
    """Centralized error handling for bots"""

    @staticmethod
    def handle_error(bot_name: str, error: Exception, context: dict = None):
        """Handle bot errors with logging and optional persistence"""
        error_info = {
            "bot_name": bot_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {},
        }

        logger.error(f"Bot error in {bot_name}: {error_info}")

        # TODO: Persist error to database for tracking
        return error_info

    @staticmethod
    def is_retryable(error: Exception) -> bool:
        """Determine if an error is retryable"""
        retryable_errors = (
            ConnectionError,
            TimeoutError,
            IOError,
        )
        return isinstance(error, retryable_errors)


class RateLimiter:
    """Rate limiter for bot operations"""

    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.calls = []

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            now = time.time()

            # Remove calls older than 1 minute
            self.calls = [call_time for call_time in self.calls if now - call_time < 60]

            # Check if rate limit exceeded
            if len(self.calls) >= self.calls_per_minute:
                sleep_time = 60 - (now - self.calls[0])
                if sleep_time > 0:
                    logger.info(f"Rate limit reached, sleeping for {sleep_time:.2f} seconds")
                    time.sleep(sleep_time)
                    self.calls = []

            # Record this call
            self.calls.append(time.time())

            return func(*args, **kwargs)

        return wrapper


def with_timeout(seconds: int = None):
    """Decorator to add timeout to bot operations"""
    timeout_seconds = seconds or config.get("bots.timeout_seconds", 300)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            import signal

            def timeout_handler(signum, frame):
                raise TimeoutError(f"Operation timed out after {timeout_seconds} seconds")

            # Set the signal handler and alarm
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout_seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)  # Disable the alarm

            return result

        return wrapper

    return decorator
