from phase3.authority_governance.authority_registry import (
    AuthorityRegistry,
)


class AuthorityQuery:

    def __init__(
        self,
        registry: AuthorityRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        authority_id: str,
    ):

        return self.registry.get(authority_id)
