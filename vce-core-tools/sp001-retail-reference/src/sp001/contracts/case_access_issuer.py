from typing import Protocol, runtime_checkable


@runtime_checkable
class CaseAccessIssuer(Protocol):
    """Authorized limited preparation and authenticated completion/recovery."""

    def prepare_request(self, *, credential, request):
        ...

    def complete(self, *, credential, request_id):
        ...
