from collections import deque


def unique_results(cache_size=100):
    """
    Decorator that caches last cache_size results and
    ensures that result of the call doesn't exist in cache already
    :param cache_size: int
    :return: decorated function
    """
    cache = deque(maxlen=cache_size)

    def decorator(fn):
        def wrapper(*args, **kwargs):
            while True:
                result = fn(*args, **kwargs)
                if result not in cache:
                    cache.append(result)
                    break
                else:
                    pass
            return result
        return wrapper

    return decorator
