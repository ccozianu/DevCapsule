from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from tests.test_base_image import pex_fixture


SPEC = importlib.util.spec_from_file_location(
    "release_manifest", Path(__file__).parents[1] / "scripts" / "release-manifest.py",
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_manifest_checks_release_identity_and_records_pinned_bases(tmp_path: Path) -> None:
    pex = pex_fixture(tmp_path / "devcapsule.pex", build_mnemonic="v0.1.0")
    result = MODULE.manifest(pex, "v0.1.0", "a" * 40)
    assert result["artifacts"]["devcapsule.pex"]
    assert all("@sha256:" in base for base in result["base-references"])
    with pytest.raises(ValueError, match="identity disagrees"):
        MODULE.manifest(pex, "v0.2.11", "a" * 40)
    with pytest.raises(ValueError, match="identity disagrees"):
        MODULE.manifest(pex, "v0.1.0", "b" * 40)
