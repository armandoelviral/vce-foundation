"""
HAS Executable Knowledge Runtime

Master invariant suite.

This file intentionally introduces no new
domain concepts.

Its sole responsibility is to execute the
complete invariant set as one executable
release gate.
"""

import pytest


INVARIANT_MODULES = (

    "tests.runtime.test_invariant_state_monotonicity",

    "tests.runtime.test_invariant_event_continuity",

    "tests.runtime.test_invariant_replay_determinism",

    "tests.runtime.test_invariant_history_integrity",

    "tests.runtime.test_invariant_runtime_determinism",

    "tests.runtime.test_invariant_runtime_input_immutability",

    "tests.runtime.test_invariant_verification_closure",

    "tests.runtime.test_invariant_pipeline_closure",

)


@pytest.mark.parametrize(
    "module_name",
    INVARIANT_MODULES,
)
def test_invariant_module_imports(
    module_name,
):
    __import__(module_name)
