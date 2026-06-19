class AuthorityReport:

    def __init__(
        self,
        authorities,
    ):

        self.authorities = authorities

    def authority_count(
        self,
    ) -> int:

        return len(
            self.authorities
        )

    def authority_ids(
        self,
    ):

        return list(
            self.authorities.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "authority_count":
                self.authority_count(),
            "authority_ids":
                self.authority_ids(),
        }
