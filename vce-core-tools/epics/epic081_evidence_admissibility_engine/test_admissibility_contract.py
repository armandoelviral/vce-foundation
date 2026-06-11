from pathlib import Path


CONTRACT = Path(
    "epics/epic081_evidence_admissibility_engine/admissibility_contract.md"
)


def test_admissibility_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_core_principle():

    content = CONTRACT.read_text()

    assert "Cryptographic validity is necessary but not sufficient" in content


def test_contract_defines_admission_rules():

    content = CONTRACT.read_text()

    assert "process is cataloged" in content
    assert "CPS threshold is satisfied" in content
    assert "operational context matches" in content
    assert "governance approval is active" in content


def test_contract_defines_rejection_reasons():

    content = CONTRACT.read_text()

    assert "PROCESS_NOT_CATALOGED" in content
    assert "CPS_THRESHOLD_NOT_MET" in content
    assert "CONTEXT_MISMATCH" in content
    assert "GOVERNANCE_NOT_ACTIVE" in content


def test_contract_blocks_unadmitted_evidence():

    content = CONTRACT.read_text()

    assert "Only admitted evidence may be written" in content
