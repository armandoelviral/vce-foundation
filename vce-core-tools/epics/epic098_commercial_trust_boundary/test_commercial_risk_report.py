from epics.epic098_commercial_trust_boundary.commercial_risk_report import (
    CommercialRiskReport,
)


def test_contains_liability_risk():

    report = CommercialRiskReport.generate()

    assert "liability_risk" in report


def test_contains_network_risk():

    report = CommercialRiskReport.generate()

    assert "network_admission_risk" in report


def test_contains_jurisdiction_risk():

    report = CommercialRiskReport.generate()

    assert "jurisdiction_risk" in report


def test_contains_compliance_risk():

    report = CommercialRiskReport.generate()

    assert "compliance_risk" in report


def test_report_is_mitigated():

    report = CommercialRiskReport.generate()

    assert report["mitigated"] is True
