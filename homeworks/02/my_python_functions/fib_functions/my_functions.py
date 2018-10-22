from functools import lru_cache

@lru_cache(None)
def fib(n):
    if n == 1 or n == 2:
        return 1
    return fib(n-1) + fib(n-2)
