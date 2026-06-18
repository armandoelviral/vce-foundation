from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)


class StateHashVerifier:

    def verify(
        self,
        state: RuntimeState,
        expected_hash: str,
    ) -> bool:

        if not expected_hash:
            return False

        return (
            state.state_hash
            == expected_hash
        )
