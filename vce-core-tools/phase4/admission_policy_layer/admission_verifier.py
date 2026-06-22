class AdmissionVerifier:

    @staticmethod
    def verify(
        state,
    ) -> bool:

        return (
            state.admission_state
            == "ADMITTED"
        )
