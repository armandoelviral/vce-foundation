"""Bounded ASGI body reader for PRODUCT-001 MVP1 laboratory.

No authentication, authorization, persistence, or HTTP routes.
"""

import asyncio

from collections.abc import Awaitable, Callable
from typing import Any

from sp001.infrastructure.product001_mvp1_http_json_parser import (
    MAX_PRODUCT001_MVP1_BODY_BYTES,
)


MAX_PRODUCT001_MVP1_EMPTY_FRAGMENTS = 64


async def read_product001_mvp1_bounded_body(
    receive: Callable[[], Awaitable[dict[str, Any]]],
    *,
    content_length: str | None,
) -> bytes:
    """Read a complete ASGI HTTP body within the laboratory byte limit."""

    expected_length = None

    if content_length is not None:
        if (
            type(content_length) is not str
            or not content_length
            or not content_length.isascii()
            or not content_length.isdecimal()
        ):
            raise ValueError("invalid Content-Length")

        expected_length = int(content_length)

        if expected_length > MAX_PRODUCT001_MVP1_BODY_BYTES:
            raise ValueError("Content-Length exceeds body limit")

    chunks = []
    total = 0
    empty_fragments = 0

    while True:
        try:
            message = await receive()
        except RuntimeError as exc:
            if isinstance(exc.__cause__, StopIteration):
                raise ValueError("ASGI body incomplete") from exc
            raise

        if type(message) is not dict:
            raise TypeError("invalid ASGI message")

        if message.get("type") == "http.disconnect":
            raise ValueError("HTTP client disconnected")

        if message.get("type") != "http.request":
            raise ValueError("unexpected ASGI message")

        body = message.get("body", b"")

        if type(body) is not bytes:
            raise TypeError("ASGI body must be bytes")

        more_body = message.get("more_body", False)

        if type(more_body) is not bool:
            raise TypeError("invalid ASGI more_body flag")

        if more_body and not body:
            empty_fragments += 1
            if empty_fragments > MAX_PRODUCT001_MVP1_EMPTY_FRAGMENTS:
                raise ValueError("ASGI body made no progress")
        else:
            empty_fragments = 0

        total += len(body)

        if total > MAX_PRODUCT001_MVP1_BODY_BYTES:
            raise ValueError("HTTP body exceeds size limit")

        if expected_length is not None and total > expected_length:
            raise ValueError("body exceeds declared Content-Length")

        chunks.append(body)

        if not more_body:
            break
        await asyncio.sleep(0)

    if expected_length is not None and total != expected_length:
        raise ValueError("Content-Length mismatch")

    return b"".join(chunks)
