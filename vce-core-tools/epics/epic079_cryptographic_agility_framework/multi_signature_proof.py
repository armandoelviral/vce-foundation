from dataclasses import dataclass


@dataclass(frozen=True)
class ProofSignature:
    signature_id: str
    algorithm_id: str
    signature_value: str
    cryptographic_epoch: str


@dataclass(frozen=True)
class MultiSignatureProof:
    artifact_hash: str
    signatures: list[ProofSignature]

    def signature_count(self):

        return len(
            self.signatures
        )

    def algorithms(self):

        return [
            signature.algorithm_id
            for signature in self.signatures
        ]

    def has_algorithm(
        self,
        algorithm_id: str,
    ):

        return algorithm_id in self.algorithms()
