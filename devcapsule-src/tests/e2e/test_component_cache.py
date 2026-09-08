"""Exercise cross-image contribution reuse on the actual Docker builder."""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import uuid

import pytest

from devcapsule.environment_realization import optional_local_image
from devcapsule.image_build import (
    BuildxImageBuilder, ContributionComponent, ExecComponent,
    FileComponent, ImageBuildSpec,
)
from devcapsule.materialization import ArtifactSpec, ensure_materialized_surface


def docker(*args: str) -> str:
    return subprocess.run(["docker", *args], check=True, text=True, capture_output=True).stdout.strip()


@pytest.mark.e2e
def test_installation_is_reused_across_images_and_invalidated_by_recipe(tmp_path: Path) -> None:
    token = uuid.uuid4().hex
    images = [f"devcapsule-cache-test:{token}-{index}" for index in range(3)]
    builder = BuildxImageBuilder()
    runtime = tmp_path / "runtime"
    observed = []
    # Random output proves that the install did not execute a second time.
    # The per-test token prevents borrowing a cache hit from an earlier test.
    def contribution(version: str) -> ContributionComponent:
        return ContributionComponent("jdk", (ExecComponent((
            "sh", "-c", f"mkdir -p /opt/jdk/{version} && "
            f"cat /proc/sys/kernel/random/uuid > /opt/jdk/{version}/installed-{token} && "
            f"ln -s {version} /opt/jdk/current",
        )),), ("/opt/jdk",))

    try:
        for index, image in enumerate(images):
            runtime.write_text(f"launcher-{index}")
            version = "1" if index < 2 else "2"
            sibling = ContributionComponent("another-component", (
                ExecComponent(("sh", "-c", f"mkdir -p /opt/other && echo {index} > /opt/other/version")),
            ), ("/opt/other",))
            stages = (contribution(version), sibling) if index == 0 else (sibling, contribution(version))
            builder.build(ImageBuildSpec(image, "ubuntu:24.04", (
                *stages, FileComponent(runtime, "/runtime"),
            )), network="none")
            observed.append(docker("run", "--rm", "--network=none", image,
                                   "cat", f"/opt/jdk/current/installed-{token}"))
            assert docker("run", "--rm", image, "cat", "/runtime") == f"launcher-{index}"
        assert observed[0] == observed[1]
        assert observed[2] != observed[1]
    finally:
        subprocess.run(["docker", "image", "rm", *images], capture_output=True)


@pytest.mark.e2e
@pytest.mark.parametrize("surface", ["pycharm", "codium"])
def test_formation_receives_exact_launcher_on_runtime_free_base(
    tmp_path: Path, built_pex: Path, surface: str,
) -> None:
    archive_path = tmp_path / "surface.tar.gz"
    names = ("bin/pycharm.sh",) if surface == "pycharm" else ("codium", "bin/codium", "chrome-sandbox")
    with tarfile.open(archive_path, "w:gz") as archive:
        for name in names:
            data = b"#!/bin/sh\nexit 0\n"
            member = tarfile.TarInfo(f"fixture/{name}")
            member.size, member.mode = len(data), 0o755
            archive.addfile(member, io.BytesIO(data))
    image = None
    try:
        base = json.loads(docker("image", "inspect", "ubuntu:24.04"))[0]
        image, created = ensure_materialized_surface(
            base_reference="ubuntu:24.04", base_identity=base["Id"],
            platform=f"{base['Os']}-{base['Architecture']}",
            artifact=ArtifactSpec("fixture", archive_path.as_uri(),
                                  hashlib.sha256(archive_path.read_bytes()).hexdigest(),
                                  "professional" if surface == "pycharm" else None),
            cache_root=tmp_path / "cache", inspect_image=optional_local_image,
            build=lambda spec: BuildxImageBuilder().build(spec, network="none"),
            recipe_id="jetbrains-local-materialization" if surface == "pycharm" else "vscode-local-materialization",
            recipe_version="1" if surface == "pycharm" else "2",
            component_id=surface, runtime_pex=built_pex,
        )
        assert created
        digest = docker("run", "--rm", "--entrypoint=sha256sum", image,
                        "/opt/devcapsule/bin/devcapsule.pex").split()[0]
        assert digest == hashlib.sha256(built_pex.read_bytes()).hexdigest()
        labels = json.loads(docker("image", "inspect", image))[0]["Config"]["Labels"]
        assert labels["devcapsule.pex.sha256"] == digest
        assert "usage: devcapsule runtime" in docker("run", "--rm", "--network=none", image, "--help")
        actual = json.loads(docker("run", "--rm", "--network=none",
                                   "--entrypoint=/opt/devcapsule/bin/devcapsule.pex", image, "version", "--json"))
        expected = json.loads(subprocess.check_output([str(built_pex), "version", "--json"], text=True))
        assert actual == expected
    finally:
        if image:
            subprocess.run(["docker", "image", "rm", image], capture_output=True)
