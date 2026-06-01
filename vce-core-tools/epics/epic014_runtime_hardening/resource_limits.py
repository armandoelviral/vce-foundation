class ResourceLimits:

    def __init__(
        self,
        max_events=1000,
        max_payload_size=1024
    ):

        self.max_events = max_events
        self.max_payload_size = max_payload_size


    def validate_stream(
        self,
        events
    ):

        if len(events) > self.max_events:
            return False


        for event in events:

            payload = event.get(
                "payload",
                ""
            )

            if len(payload) > self.max_payload_size:
                return False


        return True
