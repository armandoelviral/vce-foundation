def validate_lsn(events):
    expected = 1

    for event in events:
        if event["lsn"] != expected:
            return False

        expected += 1

    return True
