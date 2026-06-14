from epics.epic092_deterministic_execution_policy.module_admission_gate import (
    ModuleAdmissionGate,
)


def test_admits_pure_compute_module():

    assert ModuleAdmissionGate.admit(
        {
            "memory",
            "arithmetic",
        }
    )


def test_rejects_clock_module():

    assert not ModuleAdmissionGate.admit(
        {
            "clock",
        }
    )


def test_rejects_network_module():

    assert not ModuleAdmissionGate.admit(
        {
            "network",
        }
    )


def test_rejects_filesystem_module():

    assert not ModuleAdmissionGate.admit(
        {
            "filesystem",
        }
    )


def test_rejects_mixed_module():

    assert not ModuleAdmissionGate.admit(
        {
            "memory",
            "clock",
        }
    )
