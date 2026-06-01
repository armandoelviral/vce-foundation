from epics.epic016_production_verification.coverage_gate import (
    CoverageGate
)


gate = CoverageGate(
    minimum=90
)


good = gate.validate(
    95
)


bad = gate.validate(
    80
)


print(
    good["passed"]
)


print(
    bad["passed"]
)
