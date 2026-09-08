"""Locate the exact launcher artifact to deliver into a formation."""

from __future__ import annotations

import os
from pathlib import Path
import sys

from devcapsule.build_info import BuildInfoError, read_pex_build_info
from devcapsule.compat import CliError


def runtime_artifact() -> Path:
    # scie preserves the executable's path in SCIE; PEX points to the original
    # archive too. sys.argv[0] alone can name the extracted console script.
    # A source-form launcher must explicitly select its built runtime.
    selected = (os.environ.get("SCIE") or os.environ.get("PEX")
                or os.environ.get("DEVCAPSULE_RUNTIME_PEX") or sys.argv[0])
    path = Path(selected).expanduser().resolve()
    try:
        read_pex_build_info(path)
    except BuildInfoError as exc:
        raise CliError(
            "Environment materialization needs a DevCapsule PEX. Run the built PEX, "
            "or build with 'nox -s pex' and set DEVCAPSULE_RUNTIME_PEX to its path "
            "when running from source."
        ) from exc
    return path
