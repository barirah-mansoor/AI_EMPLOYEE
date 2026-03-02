#!/usr/bin/env python3
"""
Retry Handler - Exponential backoff retry decorator and error classes
"""

import time
import functools
import logging
from typing import Callable, Any, Type, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransientError(Exception):
    """Exception for transient errors that should be retried."""
    pass


class AuthError(Exception):
    """Exception for authentication errors that should NOT be retried."""
    pass


def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (TransientError, ConnectionError, TimeoutError)
):
    """
    Decorator that adds exponential backoff retry to a function.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        base_delay: Initial delay in seconds (default: 1.0)
        max_delay: Maximum delay cap in seconds (default: 60.0)
        exceptions: Tuple of exception types to catch and retry

    Usage:
        @with_retry(max_attempts=5, base_delay=2)
        def my_function():
            # function code
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempt = 0

            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)

                except AuthError:
                    # Do NOT retry authentication errors
                    logger.error(f"Authentication error - not retrying: {func.__name__}")
                    raise

                except exceptions as e:
                    attempt += 1

                    if attempt >= max_attempts:
                        logger.error(f"Max attempts ({max_attempts}) reached for {func.__name__}")
                        raise

                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)

                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )

                    time.sleep(delay)

            # This should never be reached, but just in case
            raise RuntimeError(f"All retry attempts failed for {func.__name__}")

        return wrapper
    return decorator


def with_retry_async(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (TransientError, ConnectionError, TimeoutError)
):
    """
    Async version of with_retry decorator.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            import asyncio

            attempt = 0

            while attempt < max_attempts:
                try:
                    return await func(*args, **kwargs)

                except AuthError:
                    logger.error(f"Authentication error - not retrying: {func.__name__}")
                    raise

                except exceptions as e:
                    attempt += 1

                    if attempt >= max_attempts:
                        logger.error(f"Max attempts ({max_attempts}) reached for {func.__name__}")
                        raise

                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)

                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )

                    await asyncio.sleep(delay)

            raise RuntimeError(f"All retry attempts failed for {func.__name__}")

        return wrapper
    return decorator


# Test / demo
if __name__ == "__main__":
    print("=== Retry Handler Test ===\n")

    # Test 1: Successful function
    @with_retry(max_attempts=3, base_delay=0.5)
    def successful_function():
        return "Success!"

    result = successful_function()
    print(f"Test 1 - Successful: {result}")

    # Test 2: Function with transient error that succeeds on retry
    call_count = [0]

    @with_retry(max_attempts=3, base_delay=0.5)
    def retry_success_function():
        call_count[0] += 1
        if call_count[0] < 2:
            raise TransientError("Temporary failure")
        return "Success after retry!"

    result = retry_success_function()
    print(f"Test 2 - Retry success: {result} (attempts: {call_count[0]})")

    # Test 3: Function that always fails
    @with_retry(max_attempts=2, base_delay=0.5)
    def always_fail_function():
        raise TransientError("Permanent failure")

    try:
        always_fail_function()
    except TransientError as e:
        print(f"Test 3 - Always fails: Correctly raised exception after retries")

    # Test 4: AuthError should not retry
    @with_retry(max_attempts=3, base_delay=0.5)
    def auth_fail_function():
        raise AuthError("Invalid credentials")

    try:
        auth_fail_function()
    except AuthError as e:
        print(f"Test 4 - Auth error: Correctly did NOT retry")

    # Test 5: Custom exceptions
    class MyTransientError(Exception):
        pass

    @with_retry(max_attempts=3, base_delay=0.5, exceptions=(MyTransientError,))
    def custom_exception_function():
        raise MyTransientError("Custom transient error")

    try:
        custom_exception_function()
    except MyTransientError:
        print(f"Test 5 - Custom exception: Correctly handled")

    print("\n=== All tests passed! ===")
