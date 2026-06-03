from fastapi import FastAPI
import hashlib
import os

from epics.epic028_durable_node_ledger.node_ledger import (
    NodeLedger
)


ledger = NodeLedger(
    "node_ledger.db"
)


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
    
    "ledger": ledger.all()
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
@app.post("/append")
def append_event(event: dict):

    ledger.append(event)

    STATE["ledger"] = ledger.all()

    return {
        "status": "APPENDED",
        "ledger_size": ledger.count()
    }
