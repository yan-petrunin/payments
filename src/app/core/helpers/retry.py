import asyncio
import functools

def webhook_retry(attempts: int = 5, min_wait: float = 2, max_wait: float = 30):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            delay = min_wait
            for attempt in range(1, attempts + 1):
                try:
                    result = await func(*args, **kwargs)
                    if result:
                        return result
                except Exception as e:
                    if attempt == attempts:
                        raise
                    await asyncio.sleep(delay)
                    delay = min(delay * 2, max_wait)
        return wrapper
    return decorator
