from collections import Counter


class CryptographicMigrationAudit:

    def __init__(self, proofs):

        self._proofs = proofs

    def total_proofs(self):

        return len(
            self._proofs
        )

    def algorithm_distribution(self):

        counter = Counter()

        for proof in self._proofs:

            for algorithm in proof.algorithms():

                counter[
                    algorithm
                ] += 1

        return dict(counter)

    def epoch_distribution(self):

        counter = Counter()

        for proof in self._proofs:

            for signature in proof.signatures:

                counter[
                    signature.cryptographic_epoch
                ] += 1

        return dict(counter)

    def migration_report(self):

        return {
            "total_proofs":
                self.total_proofs(),
            "algorithm_distribution":
                self.algorithm_distribution(),
            "epoch_distribution":
                self.epoch_distribution(),
        }
