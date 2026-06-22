class RightsVerifier:

    @staticmethod
    def verify(bundle) -> bool:

        return all(
            permission.granted
            for permission in bundle.permissions
        )
