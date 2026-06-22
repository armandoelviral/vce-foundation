class ResponseTrustVerifier:

    @staticmethod
    def verify(
        response_state,
    ) -> bool:

        return (
            response_state.response_state
            in (
                "VALID",
                "RECOVERED",
            )
        )
