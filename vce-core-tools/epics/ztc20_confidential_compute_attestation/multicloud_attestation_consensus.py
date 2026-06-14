class MultiCloudAttestationConsensus:

    def has_consensus(
        self,
        total_witnesses: int,
        attested_witnesses: int,
    ) -> bool:

        required = (
            total_witnesses // 2
        ) + 1

        return (
            attested_witnesses
            >= required
        )
