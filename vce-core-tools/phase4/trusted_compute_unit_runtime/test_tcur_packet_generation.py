from phase4.trusted_compute_unit_runtime.tcur_packet_generator import (
    TcurPacketGenerator,
)


def test_generates_complete_packet():

    packet = TcurPacketGenerator.generate()

    assert "payload_hash" in packet

    assert "decision" in packet
    assert "evidence" in packet
    assert "signatures" in packet
    assert "proof" in packet
    assert "transparency" in packet


def test_payload_hash_is_valid():

    packet = TcurPacketGenerator.generate()

    assert len(packet["payload_hash"]) == 64
