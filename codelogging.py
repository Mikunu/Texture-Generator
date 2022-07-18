import logging
from time import perf_counter
from functools import wraps


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        total_time = end_time - start_time
        logging.info(f'Function {func.__name__} took {total_time} seconds') # total_time:.4f
        return result
    return timeit_wrapper
