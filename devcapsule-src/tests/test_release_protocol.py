from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import subprocess

import pytest

SPEC = importlib.util.spec_from_file_location("release_protocol", Path(__file__).parents[1] / "scripts/release-protocol.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


@pytest.mark.parametrize("tag,expected", [("v0.2.11", ("0.2.11", "0.2.11", False)),
                                          ("v0.2.11-rc0", ("0.2.11", "0.2.11rc0", True))])
def test_identity(tag, expected):
    assert MODULE.identity(tag) == expected


@pytest.mark.parametrize("tag", ["v01.2.3", "v1.2.3-rc01", "v1.2.3-rc", "1.2.3", "v1.2.3\n", "v1.2.3-rc0-extra"])
def test_invalid_identity(tag):
    with pytest.raises(ValueError):
        MODULE.identity(tag)


@pytest.fixture
def history(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    def git(*args):
        return subprocess.check_output(["git", *args], text=True).strip()
    git("init", "-q", "-b", "main")
    git("config", "user.name", "Tests")
    git("config", "user.email", "tests@example.invalid")
    git("commit", "--allow-empty", "-qm", "baseline")
    baseline = git("rev-parse", "HEAD")
    git("checkout", "-qb", "release-0.2.11")
    (tmp_path / "fix").write_text("release fix")
    git("add", "fix")
    git("commit", "-qm", "fix")
    revision = git("rev-parse", "HEAD")
    git("tag", "v0.2.11-rc0")
    git("tag", "v0.2.11")
    record = {"schema-version": 1, "tag": "v0.2.11", "candidate-tag": "v0.2.11-rc0",
              "source-revision": revision, "candidate-sha256": "a" * 64,
              "accepted-by": "operator", "evidence": ["Exact candidate smoke passed"],
              "integration": {"method": "ancestry", "baseline": baseline}}
    return git, revision, record


def test_main_can_advance_and_need_not_be_first_parent(history):
    git, revision, record = history
    git("checkout", "-q", "main")
    git("commit", "--allow-empty", "-qm", "unrelated work")
    git("merge", "--no-ff", "-qm", "integrate", "release-0.2.11")
    git("commit", "--allow-empty", "-qm", "more work")
    MODULE.validate_promotion("v0.2.11", revision, record, "main")


def test_unintegrated_release_requires_scoped_exception(history):
    _, revision, record = history
    with pytest.raises(ValueError, match="not been merged"):
        MODULE.validate_promotion("v0.2.11", revision, record, "main")
    record["integration"].update(method="exception", **{"authorized-by": "owner", "rationale": "main is broken",
        "forward-port-owner": "team", "follow-up": "tracked forward-port"})
    MODULE.validate_promotion("v0.2.11", revision, record, "main")
    del record["integration"]["follow-up"]
    with pytest.raises(ValueError, match="follow-up"):
        MODULE.validate_promotion("v0.2.11", revision, record, "main")


def test_reviewed_cherry_pick_requires_main_evidence_and_whole_delta(history):
    git, revision, record = history
    git("checkout", "-q", "main")
    git("commit", "--allow-empty", "-qm", "unrelated")
    git("cherry-pick", revision)
    main = git("rev-parse", "HEAD")
    record["integration"].update(method="reviewed", **{"reviewed-by": "owner", "rationale": "entire fix cherry-picked",
        "main-commits": [main], "covers-release-delta": True})
    MODULE.validate_promotion("v0.2.11", revision, record, "main")
    record["integration"]["main-commits"] = [revision]
    with pytest.raises(ValueError, match="absent from main"):
        MODULE.validate_promotion("v0.2.11", revision, record, "main")


@pytest.mark.parametrize("key,value", [("source-revision", "b" * 40), ("candidate-tag", "v0.2.12-rc0"),
    ("candidate-sha256", "bad"), ("accepted-by", ""), ("evidence", [])])
def test_acceptance_is_bound_to_exact_candidate(history, key, value):
    _, revision, record = history
    record = copy.deepcopy(record)
    record[key] = value
    with pytest.raises(ValueError):
        MODULE.validate_promotion("v0.2.11", revision, record, "main")


def test_candidate_can_publish_before_main_integration(history, tmp_path):
    git, revision, _ = history
    git("remote", "add", "origin", str(tmp_path))
    result = MODULE.gate("v0.2.11-rc0", tmp_path / "gate.json")
    assert result["prerelease"] is True
    assert result["source-revision"] == revision
    git("checkout", "--detach", "-q", revision)
    git("update-ref", "-d", "refs/remotes/origin/release-0.2.11")
    git("update-ref", "refs/heads/release-0.2.11", git("rev-parse", "main"))
    with pytest.raises(ValueError, match="belong"):
        MODULE.gate("v0.2.11-rc0", tmp_path / "gate.json")
