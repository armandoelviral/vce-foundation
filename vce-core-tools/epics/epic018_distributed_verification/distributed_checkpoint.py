import hashlib
import json


class DistributedCheckpoint:

    def __init__(self):

        self.chain = []


    def append(
        self,
        transcript_hash
    ):

        previous = (
            self.chain[-1]["checkpoint_hash"]
            if self.chain
            else
            "GENESIS"
        )


        checkpoint = {
            "index": len(
                self.chain
            )
            +
            1,

            "previous_hash": previous,

            "transcript_hash": transcript_hash
        }


        digest = hashlib.sha256(
            json.dumps(
                checkpoint,
                sort_keys=True,
                separators=(",", ":")
            ).encode()
        ).hexdigest()


        checkpoint[
            "checkpoint_hash"
        ] = digest


        self.chain.append(
            checkpoint
        )


        return checkpoint


    def verify_chain(
        self
    ):

        previous = "GENESIS"


        for checkpoint in self.chain:

            if checkpoint[
                "previous_hash"
            ] != previous:

                return False


            stored = checkpoint[
                "checkpoint_hash"
            ]


            data = dict(
                checkpoint
            )

            del data[
                "checkpoint_hash"
            ]


            expected = hashlib.sha256(
                json.dumps(
                    data,
                    sort_keys=True,
                    separators=(",", ":")
                ).encode()
            ).hexdigest()


            if expected != stored:

                return False


            previous = stored


        return True
