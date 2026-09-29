SECURITY_ADMISSION_PORTABLE_UINT64_MAX = (1 << 64) - 1


def validate_security_admission_positive_uint64(
    *,
    value: object,
    field: str,
) -> int:
    """Return one positive integer exactly representable as portable u64."""

    _validate_field_name(field)

    if type(value) is not int:
        raise TypeError(f"{field} must be an integer")
    if value <= 0:
        raise ValueError(f"{field} must be positive")
    if value > SECURITY_ADMISSION_PORTABLE_UINT64_MAX:
        raise ValueError(
            f"{field} must not exceed portable uint64 maximum"
        )

    return value


def validate_security_admission_non_negative_uint64(
    *,
    value: object,
    field: str,
) -> int:
    """Return one non-negative integer exactly representable as portable u64."""

    _validate_field_name(field)

    if type(value) is not int:
        raise TypeError(f"{field} must be an integer")
    if value < 0:
        raise ValueError(f"{field} must be non-negative")
    if value > SECURITY_ADMISSION_PORTABLE_UINT64_MAX:
        raise ValueError(
            f"{field} must not exceed portable uint64 maximum"
        )

    return value


def _validate_field_name(field: object) -> None:
    if not isinstance(field, str):
        raise TypeError("field must be a string")
    if not field.strip():
        raise ValueError("field must not be blank")
