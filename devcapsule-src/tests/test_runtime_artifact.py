from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from devcapsule.compat import CliError
from devcapsule.materialization import ArtifactSpec, formation_descriptor, formation_identity
from devcapsule.runtime_artifact import runtime_artifact
from tests.test_base_image import pex_fixture


def test_packaged_launcher_supplies_itself_despite_source_override(tmp_path: Path, monkeypatch) -> None:
    launcher = pex_fixture(tmp_path / "launcher.pex")
    monkeypatch.setenv("SCIE", str(launcher))
    monkeypatch.setenv("DEVCAPSULE_RUNTIME_PEX", str(tmp_path / "different.pex"))
    assert runtime_artifact() == launcher


def test_source_launcher_requires_explicit_built_runtime(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("SCIE", raising=False)
    monkeypatch.delenv("PEX", raising=False)
    monkeypatch.setenv("DEVCAPSULE_RUNTIME_PEX", str(tmp_path / "missing.pex"))
    with pytest.raises(CliError, match="DEVCAPSULE_RUNTIME_PEX"):
        runtime_artifact()
    launcher = pex_fixture(tmp_path / "runtime.pex")
    monkeypatch.setenv("DEVCAPSULE_RUNTIME_PEX", str(launcher))
    assert runtime_artifact() == launcher


def test_runtime_update_changes_formation_identity_without_changing_components() -> None:
    artifact = ArtifactSpec("1", "https://example.test/ide", "a" * 64)
    before = formation_descriptor(platform="linux-amd64", base_identity="sha256:base", artifact=artifact,
                                  runtime_sha256=hashlib.sha256(b"old").hexdigest())
    after = formation_descriptor(platform="linux-amd64", base_identity="sha256:base", artifact=artifact,
                                 runtime_sha256=hashlib.sha256(b"new").hexdigest())
    assert before["components"] == after["components"]
    assert formation_identity(before) != formation_identity(after)
