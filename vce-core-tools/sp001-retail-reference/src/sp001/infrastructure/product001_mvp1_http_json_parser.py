"""Strict JSON parser for PRODUCT-001 MVP1 laboratory transport.

Pure validation. No authentication, authorization, or persistence.
"""

import json
import math
import re


MAX_PRODUCT001_MVP1_BODY_BYTES = 65_536
MAX_PRODUCT001_MVP1_JSON_DEPTH = 64
MAX_PRODUCT001_MVP1_INTEGER_DIGITS = 256


def _check_structural_depth(source):
    depth = 0
    in_string = False
    escaped = False

    for char in source:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char in "[{":
            depth += 1
            if depth > MAX_PRODUCT001_MVP1_JSON_DEPTH:
                raise ValueError("JSON nesting limit exceeded")
        elif char in "]}":
            depth -= 1
            if depth < 0:
                raise ValueError("unbalanced JSON structure")


def _reject_duplicate_keys(pairs):
    result = {}

    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value

    return result


def _reject_nonstandard_constant(value):
    raise ValueError("nonstandard JSON numeric constant")


def _parse_integer(value):
    digits = value.lstrip("-")

    if len(digits) > MAX_PRODUCT001_MVP1_INTEGER_DIGITS:
        raise ValueError("JSON integer digit limit exceeded")

    return int(value)


def _parse_float(value):
    result = float(value)

    if not math.isfinite(result):
        raise ValueError("nonfinite JSON number")

    return result


def _check_unicode(value):
    if isinstance(value, str):
        for char in value:
            if 0xD800 <= ord(char) <= 0xDFFF:
                raise ValueError("unpaired Unicode surrogate")
    elif isinstance(value, list):
        for item in value:
            _check_unicode(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            _check_unicode(key)
            _check_unicode(item)


def parse_product001_mvp1_json_body(body: bytes) -> dict:
    if type(body) is not bytes:
        raise TypeError("JSON body must be bytes")

    if len(body) > MAX_PRODUCT001_MVP1_BODY_BYTES:
        raise ValueError("JSON body exceeds size limit")

    try:
        decoded = body.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("invalid UTF-8") from exc

    _check_structural_depth(decoded)

    try:
        result = json.loads(
            decoded,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonstandard_constant,
            parse_int=_parse_integer,
            parse_float=_parse_float,
        )
    except (json.JSONDecodeError, OverflowError) as exc:
        raise ValueError("invalid JSON") from exc

    if type(result) is not dict:
        raise TypeError("JSON root must be an object")

    _check_unicode(result)

    return result
