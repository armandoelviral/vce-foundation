from dataclasses import dataclass, field


@dataclass
class TcuRegistry:

    entries: list = field(default_factory=list)

    def add(self, entry):

        self.entries.append(entry)

    def to_dict(self):

        return {
            "entries": [
                entry.to_dict()
                for entry in self.entries
            ]
        }
