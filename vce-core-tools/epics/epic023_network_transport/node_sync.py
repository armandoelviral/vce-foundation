class NodeSynchronization:

    def compare(
        self,
        local_state_hash,
        remote_state_hash
    ):

        return {
            "in_sync":
                local_state_hash
                ==
                remote_state_hash,

            "local":
                local_state_hash,

            "remote":
                remote_state_hash
        }


    def synchronize(
        self,
        local_state_hash,
        remote_state_hash
    ):

        if (
            local_state_hash
            ==
            remote_state_hash
        ):

            return {
                "synchronized": True,
                "action": "NONE"
            }


        return {
            "synchronized": False,
            "action": "REPLAY_REQUIRED"
        }
