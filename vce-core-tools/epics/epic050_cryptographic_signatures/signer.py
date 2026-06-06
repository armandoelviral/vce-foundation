import hmac
import hashlib


class Signer:

    def __init__(self, secret):
        self.secret = secret.encode("utf-8")

    def sign(self, payload):
        return hmac.new(
            self.secret,
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def verify(self, payload, signature):
        expected = self.sign(payload)

        return hmac.compare_digest(
            expected,
            signature,
        )
