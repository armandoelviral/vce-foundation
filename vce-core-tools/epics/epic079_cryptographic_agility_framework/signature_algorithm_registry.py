from dataclasses import dataclass


@dataclass(frozen=True)
class SignatureAlgorithm:
    algorithm_id: str
    algorithm_name: str
    cryptographic_epoch: str
    active: bool


class SignatureAlgorithmRegistry:

    def __init__(self):

        self._algorithms = {}

    def register(
        self,
        algorithm: SignatureAlgorithm,
    ):

        self._algorithms[
            algorithm.algorithm_id
        ] = algorithm

    def get(
        self,
        algorithm_id: str,
    ):

        return self._algorithms.get(
            algorithm_id
        )

    def list_all(self):

        return list(
            self._algorithms.values()
        )
