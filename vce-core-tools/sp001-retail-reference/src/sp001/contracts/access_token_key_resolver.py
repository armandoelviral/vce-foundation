from typing import Protocol, runtime_checkable


@runtime_checkable
class AccessTokenKeyResolver(Protocol):
    def resolve(
        self, *, issuer: str, key_id: str, algorithm: str
    ) -> object | None:
        """Return a trusted verification key for the exact configured tuple.

        None means no accepted key. Infrastructure failures must raise.
        Token-supplied URLs do not establish trust or configure this resolver.
        """
        ...
