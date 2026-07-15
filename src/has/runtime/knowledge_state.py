from enum import Enum


class KnowledgeState(str, Enum):
    OBSERVATION = "observation"

    HYPOTHESIS = "hypothesis"

    CANDIDATE_PRINCIPLE = "candidate_principle"

    PRINCIPLE = "principle"
