"""Release ref, acceptance and integration gates; no mutations of Git refs."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess

TAG = re.compile(r"v((?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*))(?:-rc(0|[1-9][0-9]*))?")


def identity(tag: str) -> tuple[str, str, bool]:
    match = TAG.fullmatch(tag)
    if not match:
        raise ValueError("Release tag must be vMAJOR.MINOR.PATCH[-rcN]")
    version, candidate = match.groups()
    return version, version + ("rc" + candidate if candidate is not None else ""), candidate is not None


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def ancestor(revision: str, ref: str) -> bool:
    result = subprocess.run(["git", "merge-base", "--is-ancestor", revision, ref], check=False)
    if result.returncode not in (0, 1):
        raise ValueError(f"Cannot check ancestry of {revision} in {ref}")
    return result.returncode == 0


def require_text(record: dict, key: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Promotion record requires {key}")
    return value


def commit(value: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ValueError("Evidence revisions must be full commit SHAs")
    if git("rev-parse", value + "^{commit}") != value:
        raise ValueError("Evidence does not identify a commit")
    return value


def validate_promotion(tag: str, revision: str, record: dict, main_ref: str) -> None:
    version, _, is_candidate = identity(tag)
    candidate = require_text(record, "candidate-tag")
    candidate_version, _, candidate_kind = identity(candidate)
    if is_candidate or not candidate_kind or candidate_version != version:
        raise ValueError("Promotion must name a candidate for this final version")
    if record.get("schema-version") != 1 or record.get("tag") != tag:
        raise ValueError("Promotion record schema/tag mismatch")
    if record.get("source-revision") != revision or git("rev-parse", f"refs/tags/{candidate}^{{commit}}") != revision:
        raise ValueError("Final source must equal the accepted candidate commit")
    if not re.fullmatch(r"[0-9a-f]{64}", require_text(record, "candidate-sha256")):
        raise ValueError("Candidate checksum must be SHA-256")
    require_text(record, "accepted-by")
    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(isinstance(x, str) and x.strip() for x in evidence):
        raise ValueError("Acceptance requires smoke/E2E evidence")
    integration = record.get("integration", {})
    if not isinstance(integration, dict):
        raise ValueError("Integration must be an object")
    baseline = commit(require_text(integration, "baseline"))
    if not ancestor(baseline, revision):
        raise ValueError("Integration baseline must be an ancestor of the candidate")
    method = integration.get("method")
    if method == "ancestry":
        if not ancestor(revision, main_ref):
            raise ValueError("Candidate source has not been merged to main")
    elif method == "reviewed":
        require_text(integration, "reviewed-by")
        require_text(integration, "rationale")
        # This is an explicit review assertion covering the entire baseline..RC
        # delta, not an automated claim of semantic patch equivalence.
        if integration.get("covers-release-delta") is not True:
            raise ValueError("Review must cover the complete release delta")
        revisions = integration.get("main-commits")
        if not isinstance(revisions, list) or not revisions:
            raise ValueError("Review requires integrated main commits")
        for item in revisions:
            if not ancestor(commit(item), main_ref):
                raise ValueError("Reviewed integration commit is absent from main")
    elif method == "exception":
        for key in ("authorized-by", "rationale", "forward-port-owner", "follow-up"):
            require_text(integration, key)
    else:
        raise ValueError("Integration method must be ancestry, reviewed, or exception")


def gate(tag: str, output: Path) -> dict:
    version, package_version, is_candidate = identity(tag)
    revision = git("rev-parse", f"refs/tags/{tag}^{{commit}}")
    if git("rev-parse", "HEAD") != revision:
        raise ValueError("Checkout must be the selected tag")
    branch = f"release-{version}"
    git("fetch", "origin", f"refs/heads/{branch}:refs/remotes/origin/{branch}",
        "refs/heads/main:refs/remotes/origin/main")
    if not ancestor(revision, f"refs/remotes/origin/{branch}"):
        raise ValueError(f"Tag must belong to {branch}")
    result: dict = {"tag": tag, "source-revision": revision, "version": package_version,
              "prerelease": is_candidate, "release-branch": branch}
    if not is_candidate:
        main_revision = git("rev-parse", "refs/remotes/origin/main")
        path = f"engineering-docs/releases/{tag}.json"
        record = json.loads(git("show", f"{main_revision}:{path}"))
        validate_promotion(tag, revision, record, main_revision)
        result["promotion"] = {"record": record, "main-revision": main_revision, "path": path}
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("tag")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = gate(args.tag, args.output)
    if env := os.environ.get("GITHUB_ENV"):
        with open(env, "a") as stream:
            stream.write(f"DEVCAPSULE_EXPECTED_RELEASE_VERSION={result['version']}\n")
            stream.write(f"RELEASE_PRERELEASE={str(result['prerelease']).lower()}\n")
            if "promotion" in result:
                stream.write(f"ACCEPTED_CANDIDATE={result['promotion']['record']['candidate-tag']}\n")


if __name__ == "__main__":
    main()
