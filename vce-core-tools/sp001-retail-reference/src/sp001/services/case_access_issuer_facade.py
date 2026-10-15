from sp001.services.authenticated_case_access_issuance import (
    AuthenticatedCaseAccessIssuance,
)


class CaseAccessIssuerFacade:
    """Narrow public API; not a sandbox against hostile in-process code."""

    __slots__ = ("__service",)

    def __init__(self, *, service):
        if not isinstance(service, AuthenticatedCaseAccessIssuance):
            raise TypeError("service must be authenticated issuance")
        self.__service = service

    def prepare_request(self, *, credential, request):
        return self.__service.prepare_request(
            credential=credential, request=request,
        )

    def complete(self, *, credential, request_id):
        return self.__service.complete(
            credential=credential, request_id=request_id,
        )
