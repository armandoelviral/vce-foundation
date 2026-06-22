class PermissionVerifier:

    @staticmethod
    def verify(permission) -> bool:

        return permission.granted is True

