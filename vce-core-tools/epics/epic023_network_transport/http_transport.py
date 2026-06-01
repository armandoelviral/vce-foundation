class HTTPTransport:

    def request(
        self,
        method,
        endpoint,
        payload
    ):

        if method not in [
            "GET",
            "POST"
        ]:
            return {
                "status": 405,
                "error": "METHOD_NOT_ALLOWED"
            }

        if not endpoint.startswith(
            "http"
        ):
            return {
                "status": 400,
                "error": "INVALID_ENDPOINT"
            }

        return {
            "status": 200,
            "endpoint": endpoint,
            "payload": payload
        }
