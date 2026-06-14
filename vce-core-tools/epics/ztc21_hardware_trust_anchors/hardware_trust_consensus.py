class HardwareTrustConsensus:

    def has_consensus(
        self,
        total_providers: int,
        trusted_providers: int,
    ) -> bool:

        required = (
            total_providers // 2
        ) + 1

        return (
            trusted_providers
            >= required
        )
