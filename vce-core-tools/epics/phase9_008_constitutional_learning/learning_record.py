from dataclasses import dataclass


@dataclass(frozen=True)
class LearningRecord:
    learning_id: str
    outcome_id: str
    lesson: str

    def __post_init__(self):
        if not self.learning_id:
            raise ValueError("learning_id is required")

        if not self.outcome_id:
            raise ValueError("outcome_id is required")

        if not self.lesson:
            raise ValueError("lesson is required")
