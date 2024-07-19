#!/usr/bin/env python3
"""Module"""
import redis
from functools import wraps
import uuid
from typing import Union, Callable


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count calls of a method.

    Args:
        method: The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to record call history.

    Args:
        method: The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function."""
        key = method.__qualname__
        input_data = str(args)
        self._redis.rpush(f"{key}:inputs", input_data)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(f"{key}:outputs", output)
        return output

    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of a function's calls.

    Args:
        method: The function whose history is to be replayed.

    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
    call_count = cache.get(name)
    call_count = call_count.decode("utf-8") if call_count else "0"
    print(f"{name} was called {call_count} times:")

    inputs = cache.lrange(f"{name}:inputs", 0, -1)
    outputs = cache.lrange(f"{name}:outputs", 0, -1)

    for input_data, output in zip(inputs, outputs):
        print(f"{name}(*{input_data.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    """
    Cache class for storing and retrieving data.
    """

    def __init__(self):
        """
        Initialize Redis client and flush database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data with a unique key and return the key.

        Args:
            data: Data to store.

        Returns:
            str: The generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Union[Callable[[bytes], any], None] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve and optionally convert value from cache.

        Args:
            key: The key to retrieve.
            fn: Optional conversion function.

        Returns:
            The value from cache, converted if a function is provided.
        """
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Get a string value from cache.

        Args:
            key: The key to retrieve.

        Returns:
            str: The value as a string.
        """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Get an integer value from cache.

        Args:
            key: The key to retrieve.

        Returns:
            int: The value as an integer.
        """
        return self.get(key, int)

