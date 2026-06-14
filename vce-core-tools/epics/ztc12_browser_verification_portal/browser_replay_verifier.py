class BrowserReplayVerifier:

    @staticmethod
    def verify(
        historical_state_root: str,
        recomputed_state_root: str,
    ) -> bool:

        if not historical_state_root:
            return False

        if not recomputed_state_root:
            return False

        return (
            historical_state_root
            == recomputed_state_root
        )
