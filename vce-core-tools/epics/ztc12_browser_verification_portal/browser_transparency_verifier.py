class BrowserTransparencyVerifier:

    @staticmethod
    def verify(
        anchor_id: str,
        proof_present: bool,
    ) -> bool:

        if not anchor_id:
            return False

        if not proof_present:
            return False

        return True
