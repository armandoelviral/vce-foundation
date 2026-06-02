import os


STATE = {
    "node_id": os.getenv(
        "NODE_ID",
        "node-default"
    ),

    "sequence_number": 42,

    "state_hash": os.getenv(
        "STATE_HASH",
        "abc123"
    ),

    "ledger": [
        {
            "sequence": 1,
            "event": "BOOTSTRAP"
        },
        {
            "sequence": 2,
            "event": "ATTESTATION"
        }
    ]
}

from fastapi import FastAPI
import hashlib


app = FastAPI()


@app.get("/health")
def health():

    return {
        "status": "OK"
    }


@app.post("/verify")
def verify(
    payload: dict
):

    return {
        "verification": "VERIFIED",
        "payload": payload
    }


@app.post("/attest")
def attest(
    payload: dict
):

    artifact = payload.get(
        "artifact",
        ""
    )

    artifact_hash = hashlib.sha256(
        artifact.encode()
    ).hexdigest()

    return {
        "artifact": artifact,
        "artifact_hash": artifact_hash,
        "attestation": "VERIFIED",
        "trusted": True
    }

@app.get("/state")
def state():

    return STATE
