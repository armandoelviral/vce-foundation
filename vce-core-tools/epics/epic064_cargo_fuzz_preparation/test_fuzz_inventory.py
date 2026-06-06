from pathlib import Path


def test_fuzz_target_inventory_exists():

    path = Path(
        "epics/epic064_cargo_fuzz_preparation/fuzz_targets_inventory.md"
    )

    assert path.exists()


def test_fuzz_inventory_lists_core_targets():

    path = Path(
        "epics/epic064_cargo_fuzz_preparation/fuzz_targets_inventory.md"
    )

    content = path.read_text()

    assert "Replay Engine" in content
    assert "LSN Validator" in content
    assert "WAL Recovery" in content
    assert "Hash Chain" in content
    assert "Opcode Dispatch" in content
