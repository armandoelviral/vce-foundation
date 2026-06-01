from epics.epic014_runtime_hardening.fuzz_harness import FuzzHarness


fuzzer = FuzzHarness()

result = fuzzer.run(
    iterations=1000
)


print(
    result["completed"]
)

print(
    result["accepted"] + result["rejected"]
)
