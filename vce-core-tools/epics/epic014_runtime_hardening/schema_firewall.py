class SchemaFirewall:

    REQUIRED_FIELDS = [
        "lsn",
        "opcode",
        "payload"
    ]

    def validate_event(self, event):

        if not isinstance(event, dict):
            return False

        for field in self.REQUIRED_FIELDS:
            if field not in event:
                return False

        if not isinstance(event["lsn"], int):
            return False

        if not isinstance(event["opcode"], str):
            return False

        if not isinstance(event["payload"], str):
            return False

        return True

    def validate_stream(self, events):

        if not isinstance(events, list):
            return False

        for event in events:
            if not self.validate_event(event):
                return False

        return True
