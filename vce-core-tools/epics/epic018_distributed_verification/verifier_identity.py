import hashlib


class VerifierIdentity:

    def create(
        self,
        public_key
    ):

        node_id = hashlib.sha256(
            public_key.encode()
        ).hexdigest()


        return {
            "node_id": node_id,
            "public_key": public_key,
            "active": True
        }


    def verify(
        self,
        identity
    ):

        expected = hashlib.sha256(
            identity[
                "public_key"
            ].encode()
        ).hexdigest()


        return (
            expected
            ==
            identity["node_id"]
            and
            identity["active"]
        )
