class EnvironmentRegistry:

    def __init__(self):

        self._environments = set()

    def add(
        self,
        environment: str,
    ) -> None:

        self._environments.add(
            environment
        )

    def exists(
        self,
        environment: str,
    ) -> bool:

        return (
            environment
            in self._environments
        )

    def count(
        self,
    ) -> int:

        return len(
            self._environments
        )
