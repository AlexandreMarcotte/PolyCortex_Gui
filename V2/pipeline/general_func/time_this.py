import time
from functools import wraps


def time_this(func):
    """Decorator that reports the execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        time_interval = end-start
        return time_interval
    return wrapper
