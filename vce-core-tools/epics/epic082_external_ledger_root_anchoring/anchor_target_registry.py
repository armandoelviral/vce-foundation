from dataclasses import dataclass


@dataclass(frozen=True)
class AnchorTarget:
    target_id: str
    target_type: str
    active: bool


class AnchorTargetRegistry:

    def __init__(self):

        self._targets = {}

    def register(
        self,
        target: AnchorTarget,
    ):

        self._targets[
            target.target_id
        ] = target

    def get(
        self,
        target_id: str,
    ):

        return self._targets.get(
            target_id
        )

    def active_targets(self):

        return [
            target
            for target in self._targets.values()
            if target.active
        ]
