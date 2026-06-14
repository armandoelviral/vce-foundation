class FuelPolicy:

    def __init__(
        self,
        max_fuel: int,
    ):

        self.max_fuel = max_fuel

    def allow(
        self,
        consumed_fuel: int,
    ) -> bool:

        return (
            consumed_fuel
            <= self.max_fuel
        )
