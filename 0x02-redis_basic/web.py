#!/usr/bin/env python3
"""
Module for fetching and caching HTML content from a URL.
"""
import requests
import redis
from functools import wraps
from typing import Callable


def track_page_access(fn: Callable[[str], str]) -> Callable[[str], str]:
    """
    Decorator to track access count and cache results.

    Args:
        fn: The function to decorate.

    Returns:
        Callable: The decorated function with caching and counting.
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """Wrapper to handle caching and access counting."""
        client = redis.Redis()
        count_key = f"count:{url}"
        result_key = f"result:{url}"

        # Increment access count
        client.incr(count_key)

        # Check cache
        cached_page = client.get(result_key)
        if cached_page:
            return cached_page.decode("utf-8")

        # Fetch and cache the result
        response = fn(url)
        client.setex(result_key, 10, response)

        return response

    return wrapper


@track_page_access
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL.

    Args:
        url: The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
