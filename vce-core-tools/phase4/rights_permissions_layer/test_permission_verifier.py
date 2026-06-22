from phase4.rights_permissions_layer.permission_verifier import (
    PermissionVerifier,
)


class MockPermission:

    def __init__(self, granted):
        self.granted = granted


def test_granted_permission():

    permission = MockPermission(True)

    assert PermissionVerifier.verify(permission) is True


def test_denied_permission():

    permission = MockPermission(False)

    assert PermissionVerifier.verify(permission) is False
