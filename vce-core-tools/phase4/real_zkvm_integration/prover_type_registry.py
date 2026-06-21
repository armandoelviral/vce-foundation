class ProverTypeRegistry:

    def __init__(self):

        self._provers = []

    def register(
        self,
        prover_type: str,
    ) -> None:

        self._provers.append(
            prover_type
        )

    def contains(
        self,
        prover_type: str,
    ) -> bool:

        return (
            prover_type
            in self._provers
        )

    def count(
        self,
    ) -> int:

        return len(
            self._provers
        )

    def prover_types(
        self,
    ):

        return list(
            self._provers
        )
