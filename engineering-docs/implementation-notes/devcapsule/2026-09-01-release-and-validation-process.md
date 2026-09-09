# DevCapsule Release And Validation Process

Originally recorded 2026-09-01. Revised for the owner's 2026-09-09 direction:
stage and validate immutable release candidates away from main, then promote
accepted source after main integration or a scoped engineering exception.
Component installations are reused across image builds.

## Release Identity And Trigger

Prepare a release on `release-MAJOR.MINOR.PATCH` and push an immutable candidate
tag such as `v0.2.11-rc1` at the prepared commit. A patch can start from the prior
release tag rather than current main. `release-*` refs are durable release
anchors, separate from workstream selection; the owner authorized this distinction
on 2026-09-09 and sent its general workflow rules to workflow-improvements.

```text
git branch release-0.2.11 HEAD
git tag -a v0.2.11-rc0 -m 'DevCapsule 0.2.11 candidate 0'
git push --atomic origin release-0.2.11 v0.2.11-rc0
```

Use a new commit and RC number for fixes, advance the release branch, and keep
previous tags unchanged. `.github/workflows/release-pex.yml` requires the tag's
commit to belong to the matching release branch. Candidates do not require main
integration. Main stays open; do not rebase tested release source onto it.

The tag supplies the package version. `scripts/build-pex.sh` stamps package
metadata and `_build_info.json` in a temporary directory: `v0.2.11-rc1` becomes
`0.2.11rc1`, and `v0.2.11` becomes `0.2.11`. No version-bump commit is needed.
The source version remains the local-build baseline.

## Automated Candidate Release

The tag workflow:

1. Verifies the tag/branch identity, runs syntax checks, unit tests and mypy.
2. Recovers exact existing assets, or builds the self-contained PEX.
3. Records source identity, base digests, checksum, build-input hashes, dependency
   distribution fingerprints and the embedded Python fingerprint in the manifest.
4. Runs packaging integration tests, a clean-machine proof with no Python or
   networking, Docker component-install reuse and exact launcher delivery tests
   for both surface families, and runtime-session tests on each pinned base.
   Fixture IDEs do not claim real GUI or authenticated provider smoke.
5. Retains build artifacts, creates a draft release, downloads and compares its
   bytes, and repeats the clean-machine proof against the download.
6. Publishes candidates as GitHub prereleases with Latest disabled.

An incomplete or inconsistent staged asset set fails explicitly. Recover partial
uploads from the retained Actions artifact. Reruns verify and test the existing
bytes; they never replace published candidate assets or move tags.

## Acceptance And Final Promotion

Accept an exact candidate's checksum and source commit with smoke/E2E evidence.
Generate the reviewable record on the integration side:

```text
cd devcapsule-src
.venv/bin/python scripts/prepare-promotion.py v0.2.11-rc1 \
  --baseline FULL_PREPARATION_BASE_SHA --accepted-by OPERATOR \
  --evidence 'Exact candidate smoke result and Actions run URL'
```

The helper downloads and checksum-verifies the candidate and creates
`engineering-docs/releases/v0.2.11.json`. It does not perform or invent smoke
acceptance. Commit the record and integrate the candidate through normal PR
delivery. Keep the release branch and accepted tag at their tested source commit;
main can additionally contain the acceptance record and unrelated development.

The record has schema version 1, `tag`, `candidate-tag`, `source-revision`,
`candidate-sha256`, `accepted-by`, a nonempty `evidence` list, and `integration`:

- `ancestry` (helper default): `baseline` identifies the preparation base; the
  accepted candidate must be an ancestor of main, including ordinary merge commits.
- `reviewed`: additionally supply `main-commits` (full SHAs), `reviewed-by`,
  `rationale`, and `covers-release-delta: true`. Every referenced commit must be
  reachable from main. The reviewed assertion covers the entire baseline-to-RC
  delta, including adaptations in a cherry-pick or squash; patch IDs alone do
  not establish that claim.
- `exception`: additionally supply `authorized-by`, `rationale`,
  `forward-port-owner`, and `follow-up`. This is a scoped authorization in a
  reviewed engineering record, not a boolean bypass. Baseline still applies.

After the record and integration reach main:

```text
git tag -a v0.2.11 'v0.2.11-rc1^{commit}' -m 'DevCapsule 0.2.11'
git push origin v0.2.11
```

The backend checks release-branch membership, reads the record from a captured
main revision, validates acceptance/integration, downloads the published candidate
and verifies its checksum, then builds final-version bytes from exactly the same
source SHA. It compares base, dependency and Python fingerprints with the candidate
and reruns all automated gates before final publication. The final manifest embeds
the record and its main revision. Later main commits do not invalidate retries if
the accepted record remains unchanged. Final publication uses GitHub's legacy
Latest selection, which considers semantic version; candidates explicitly disable
Latest. Tagging is the publication trigger and needs no second approval prompt.

This is source promotion with a final packaging build, not byte-for-byte PEX
promotion: version metadata changes intentionally. A new source fix requires a
new candidate. Neither a broken main nor unrelated main changes require bringing
that work into a maintenance release. The initial implementation automates each
tag's backend and promotion checks; acceptance, normal PR integration, and the
final tag remain operator/agent steps.

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
