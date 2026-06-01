import hashlib
import json
import time


class ConsensusTranscript:

    def create(
        self,
        artifact_hash,
        votes,
        quorum_result
    ):

        transcript = {
            "artifact_hash": artifact_hash,
            "votes": votes,
            "quorum": quorum_result,
            "timestamp": int(
                time.time()
            )
        }


        canonical = json.dumps(
            transcript,
            sort_keys=True,
            separators=(",", ":")
        )


        digest = hashlib.sha256(
            canonical.encode()
        ).hexdigest()


        return {
            "transcript": transcript,
            "transcript_hash": digest
        }


    def verify(
        self,
        proof
    ):

        transcript = proof[
            "transcript"
        ]


        expected = hashlib.sha256(
            json.dumps(
                transcript,
                sort_keys=True,
                separators=(",", ":")
            ).encode()
        ).hexdigest()


        return (
            expected
            ==
            proof["transcript_hash"]
        )
