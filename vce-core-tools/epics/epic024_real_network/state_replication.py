import requests


class StateReplication:

    def fetch_state(self, peer_url):

        response = requests.get(
            f"{peer_url}/state",
            timeout=5
        )

        return response.json()


    def compare(self, local_state_hash, remote_state_hash):

        return {
            "in_sync": local_state_hash == remote_state_hash,
            "local": local_state_hash,
            "remote": remote_state_hash
        }


    def sync_decision(self, local_state_hash, remote_state_hash):

        if local_state_hash == remote_state_hash:
            return "IN_SYNC"

        return "REPLAY_REQUIRED"
