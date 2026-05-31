import hashlib


def calculate_hash(record):

    raw = (
        str(record["lsn"])
        + record["opcode"]
        + record["payload"]
        + record["previous_hash"]
    )

    return hashlib.sha256(
        raw.encode()
    ).hexdigest()


def verify_chain(records):

    expected_previous = "GENESIS"

    for record in records:

        if record["previous_hash"] != expected_previous:
            return False

        expected_current = calculate_hash(record)

        if record["current_hash"] != expected_current:
            return False

        expected_previous = record["current_hash"]

    return True
