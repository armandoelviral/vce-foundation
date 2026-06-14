class PromotionPolicy:

    ALLOWED_PATHS = {
        (
            "development",
            "staging",
        ),
        (
            "staging",
            "production",
        ),
    }

    def allow(
        self,
        source: str,
        target: str,
    ) -> bool:

        return (
            source,
            target,
        ) in self.ALLOWED_PATHS
