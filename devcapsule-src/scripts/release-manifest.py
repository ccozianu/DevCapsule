"""Create or verify the immutable inputs and outputs of a tag release."""

from __future__ import annotations

import argparse
import hashlib
import json
import tomllib
from pathlib import Path

from devcapsule.build_info import read_pex_build_info
from devcapsule.resolution_matrix import MATRICES
from devcapsule.platforms import Platform


def manifest(pex: Path, tag: str, revision: str) -> dict[str, object]:
    info = read_pex_build_info(pex)
    if (info.build_mnemonic, info.version, info.source_revision) != (tag, tag.removeprefix("v"), revision):
        raise ValueError("Release PEX identity disagrees with the selected tag and revision")
    # Resolve representative supported needs, recording each distinct base.
    bases = sorted({
        str(tomllib.loads(MATRICES[Platform.LINUX_AMD64].resolve([need]).render_lock())["base"]["reference"])
        for need in ("python-ide", "frontend-ide")
    })
    return {
        "schema-version": 1,
        "tag": tag,
        "source-revision": revision,
        "version": info.version,
        "base-references": bases,
        "artifacts": {pex.name: hashlib.sha256(pex.read_bytes()).hexdigest()},
    }


def main() -> None:
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("tag")
    parser.add_argument("revision")
    parser.add_argument("--verify", action="store_true")
    arguments = parser.parse_args()
    expected = manifest(Path("dist/devcapsule.pex"), arguments.tag, arguments.revision)
    path = Path("dist/release-manifest.json")
    if arguments.verify:
        if json.loads(path.read_text()) != expected:
            raise ValueError("Published release manifest does not match its artifacts and tagged source")
    else:
        path.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
