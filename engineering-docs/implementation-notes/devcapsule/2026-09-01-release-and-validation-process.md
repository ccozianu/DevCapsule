# DevCapsule Release And Validation Process

Originally recorded 2026-09-01. Revised for the owner's 2026-09-08 direction:
a version tag on mainline is the only ordinary release action; component
installations are reused across image builds.

## Release Identity And Trigger

After the content has landed on `main`, push `vMAJOR.MINOR.PATCH` at the desired
mainline commit. `.github/workflows/release-pex.yml` checks the exact tag and
requires its commit to appear in `main`'s first-parent history. It does not
require the commit to remain the tip while the release runs.

The tag supplies the package version. `scripts/build-pex.sh` stamps both the
package metadata and `_build_info.json` in its temporary build directory. The
tagged source is unchanged: there is no bump PR, repin commit, or follow-up
version commit. `pyproject.toml` remains the fallback version for source/local
builds; `nox -s bump` is optional maintenance of that baseline, not a release
step. Local mnemonics retain `-local` and official mnemonics equal the tag.

## Automated Release

The tag workflow:

1. Verifies source identity, runs syntax checks, unit tests and mypy.
2. Recovers the exact assets of an existing draft or published release, or
   builds the self-contained PEX once when no release has been staged.
3. Records the source revision, tag-derived version, selected base references
   and PEX checksum in `release-manifest.json`.
4. Runs packaging integration tests and the clean-machine proof with no Python
   or networking, plus Docker checks for component-install reuse and exact
   launcher delivery into both surface families, then pulls each selected base
   by digest and exercises runtime sessions against it. These use fixture IDEs;
   they do not claim a real GUI or authenticated provider smoke.
5. Retains build artifacts, creates a draft release with notes and checksums,
   downloads and compares the staged bytes, and proves the downloaded PEX.
6. Publishes the complete draft. A rerun verifies and tests staged bytes;
   it does not replace a published artifact with a fresh rebuild.

An incomplete or inconsistent existing asset set fails explicitly rather than
silently overwriting it. The Actions artifact retains the completed build for
recovery from a partial upload. A source defect requires a new commit and tag;
published tags and assets must never be moved or replaced. Tag creation does
not require a second manual publication approval.

## Runtime Delivery And Base Lifecycle

Recipe 7 produces a base containing the existing OS libraries and developer
tools, with no DevCapsule PEX or entrypoint added by the recipe. The builder's
source identity remains recorded as provenance; `--pex`, when supplied, selects
provenance metadata, not bytes to embed. Running the packaged builder uses its
own source identity by default. The public-revision checks still apply.

The launcher copies its exact executable PEX into the materialized environment
at `/opt/devcapsule/bin/devcapsule.pex`. Its SHA-256 is part of the formation
descriptor, so a launcher update creates a new local formation and cannot reuse
an image carrying an older runtime. Component installation stages are shared
between those formations. Source-form launches explicitly select a built PEX
through `DEVCAPSULE_RUNTIME_PEX`, or invoke the built artifact directly.

Ordinary CLI releases reuse the catalog's pinned base. In particular, v0.2.11
can use the published v0.2.10 base and replace its inherited runtime in the
derived image. Existing base tags and project locks are unchanged. This avoids
a mandatory Docker Hub publication, digest repin, sample migration, and owner
smoke cycle every time the CLI version advances.

Base maintenance has an independent cadence: update dependencies, build and
validate the base, publish under a fresh immutable name, then review its digest
pin as an ordinary catalog change. A base is not named after every CLI release.
This change does not introduce automatic base publication or choose a new
permanent base-naming scheme. Explicit dependency updates remain necessary for
security fixes; retaining a cached base is not a dependency-update policy.

## Independent Component Contributions

`ContributionComponent` describes installation steps and the paths they export.
The renderer emits a shared baseline stage, an independent stage for each
contribution, and a final image assembled with `COPY --link --from`.

- Base builds isolate Node, Temurin and Maven. Maven explicitly consumes the
  JDK stage for its installation-time verification; it exports only Maven.
- Environment builds isolate the IDE and each ancillary component. All of a
  component's npm packages remain one offline install, preserving the vendor's
  multi-file layout. Environment variables are composed in the final image.
- Component contexts have stable names independent of sibling ordering. A
  different IDE, agent or launcher does not invalidate another installer.
- BuildKit supplies cache identities from the parent image, platform, commands
  and file inputs. A version/recipe/parent change rebuilds the affected stage.
  Reuse lasts while that builder retains its cache; another host or cache
  pruning requires rebuilding. No component images or credentials are published.
- Only declared installation paths are exported. System-package side effects
  cannot be handled by copying an arbitrary installation directory; apt's
  shared baseline remains a complete filesystem layer.

The Docker regression test makes an installer emit a random identifier, builds
two different images with reordered/changed siblings and a changed launcher,
and verifies identical identifiers. A changed recipe must emit a new one.
This tests reuse itself rather than only the generated Dockerfile text.

## Validation And Integration

`nox -s build` remains the local gate. The explicit Docker cache/runtime check
is `python -m pytest --no-cov -m e2e tests/e2e/test_component_cache.py` after
building the local PEX and making `ubuntu:24.04` available. The release workflow
runs it against the actual release artifact. Packaging tests also build a tag
whose version differs from the source baseline and verify source remains clean.

Product-owner GUI/login acceptance for changed component behavior remains part
of development and integration. Fixture tests do not replace that evidence or
convert provisional matrix entries. Publishing an unchanged, accepted
component combination should not repeat the manual release walk.

Docker's behavior is documented in [multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
and [`COPY --link`](https://docs.docker.com/reference/dockerfile/#copy---link).
