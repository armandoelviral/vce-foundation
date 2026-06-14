class PQCBufferLimits:

    MAX_SIGNATURE_SIZE_BYTES = 65536

    @classmethod
    def allow(
        cls,
        signature_size_bytes: int,
    ) -> bool:

        return (
            signature_size_bytes
            <= cls.MAX_SIGNATURE_SIZE_BYTES
        )
