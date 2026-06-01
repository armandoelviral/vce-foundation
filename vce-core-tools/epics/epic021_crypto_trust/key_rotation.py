from epics.epic021_crypto_trust.ed25519_signer import (
    Ed25519Signer
)


class KeyRotationManager:

    def __init__(self):

        self.signer = Ed25519Signer()

        self.active_key = None

        self.retired_keys = []


    def initialize(self):

        self.active_key = (
            self.signer.generate_keypair()
        )

        return self.active_key


    def rotate(self):

        if self.active_key:

            self.retired_keys.append(
                self.active_key
            )

        self.active_key = (
            self.signer.generate_keypair()
        )

        return self.active_key


    def active(self):

        return self.active_key


    def retired_count(self):

        return len(
            self.retired_keys
        )
