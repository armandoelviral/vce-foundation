class DisputeResolution:

    @staticmethod
    def resolve(
        appeal_id: str,
        resolution: str,
    ):

        return {
            "appeal_id": appeal_id,
            "resolution": resolution,
        }
