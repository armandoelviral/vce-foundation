import hashlib


class TrustAnchorRegistry:

    def __init__(self):

        self.anchors = {}


    def register(
        self,
        name,
        public_key
    ):

        fingerprint = hashlib.sha256(
            str(public_key).encode()
        ).hexdigest()


        self.anchors[
            fingerprint
        ] = {
            "name": name,
            "public_key": public_key,
            "active": True
        }


        return fingerprint


    def revoke(
        self,
        fingerprint
    ):

        if fingerprint in self.anchors:

            self.anchors[
                fingerprint
            ]["active"] = False


    def verify_anchor(
        self,
        fingerprint
    ):

        if fingerprint not in self.anchors:

            return False


        return self.anchors[
            fingerprint
        ]["active"]


    def count(
        self
    ):

        return len(
            self.anchors
        )
