"""Utility functions for string and data processing."""

import re
from hashlib import sha256


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def truncate(text: str, max_len: int = 100, suffix: str = "...") -> str:
    """Truncate text to max_len, adding suffix if truncated."""
    if len(text) <= max_len:
        return text
    return text[: max_len - len(suffix)] + suffix


def hash_text(text: str) -> str:
    """Return SHA-256 hex digest of input text."""
    return sha256(text.encode("utf-8")).hexdigest()


def chunk_list(items: list, size: int) -> list[list]:
    """Split a list into chunks of given size."""
    return [items[i : i + size] for i in range(0, len(items), size)]


def flatten(nested: list) -> list:
    """Flatten a nested list one level deep."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result
