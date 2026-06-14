from epics.ztc23_security_validation_framework.fuzz_input_corpus import (
    FuzzInputCorpus,
)


class ReplayFuzzHarness:

    def __init__(
        self,
        corpus: FuzzInputCorpus,
    ):

        self.corpus = corpus

    def run(
        self,
        target,
    ):

        results = []

        for payload in self.corpus.all():

            try:
                target(payload)

                results.append(
                    {
                        "payload": payload,
                        "passed": True,
                        "error": None,
                    }
                )

            except Exception as exc:
                results.append(
                    {
                        "payload": payload,
                        "passed": False,
                        "error": str(exc),
                    }
                )

        return results
