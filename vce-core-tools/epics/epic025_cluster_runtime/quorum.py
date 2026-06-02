class Quorum:

    def evaluate(self, membership):

        total = len(
            membership.members
        )

        alive = len(
            membership.alive_nodes()
        )

        required = (
            total // 2
        ) + 1

        return {
            "total": total,
            "alive": alive,
            "required": required,
            "commit": alive >= required
        }
