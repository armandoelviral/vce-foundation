def validate_transitions(events):

    has_evidence = False

    for event in events:

        opcode = event["opcode"]

        if opcode == "APPEND_EVIDENCE":
            has_evidence = True

        elif opcode == "SEAL_SNAPSHOT":

            if not has_evidence:
                return False

    return True
