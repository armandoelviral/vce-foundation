def read_wal(path):
    events = []

    with open(path, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            lsn, opcode, payload = line.split("|")

            events.append({
                "lsn": int(lsn),
                "opcode": opcode,
                "payload": payload
            })

    return events
