class GossipDivergenceDetector:

    @staticmethod
    def detect(
        root_a: str,
        root_b: str,
    ) -> bool:

        if not root_a:
            return True

        if not root_b:
            return True

        return root_a != root_b
