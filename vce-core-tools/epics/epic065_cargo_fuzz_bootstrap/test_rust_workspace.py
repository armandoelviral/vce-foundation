from pathlib import Path


def test_rust_workspace_exists():

    assert Path("fuzz-runtime/Cargo.toml").exists()
    assert Path("fuzz-runtime/src/lib.rs").exists()


def test_rust_workspace_has_package_name():

    content = Path("fuzz-runtime/Cargo.toml").read_text()

    assert 'name = "vce-fuzz-runtime"' in content
