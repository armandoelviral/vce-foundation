from dataclasses import dataclass


@dataclass(frozen=True)
class HashAlgorithm:
    algorithm_id: str
    algorithm_name: str
    digest_length_bits: int
    cryptographic_epoch: str
    active: bool


class HashAlgorithmRegistry:

    def __init__(self):

        self._algorithms = {}

    def register(
        self,
        algorithm: HashAlgorithm,
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
