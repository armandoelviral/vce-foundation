import hashlib
import json

from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)


class StateTransitionApplier:

    def apply(
        self,
        state: RuntimeState,
        event: dict,
    ) -> RuntimeState:

        material = {
            "previous_state_hash": state.state_hash,
            "lsn": event["lsn"],
            "opcode": event["opcode"],
        }

        state_hash = hashlib.sha256(
            json.dumps(
                material,
                sort_keys=True,
            ).encode(
                "utf-8"
            )
        ).hexdigest()

        return RuntimeState(
            events_applied=(
                state.events_applied + 1
            ),
            last_lsn=event["lsn"],
            state_hash=state_hash,
        )
