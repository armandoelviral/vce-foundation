def calculate_credit_capacity(
    capital: int,
) -> int:

    if capital < 0:
        raise ValueError("capital cannot be negative")

    return capital
