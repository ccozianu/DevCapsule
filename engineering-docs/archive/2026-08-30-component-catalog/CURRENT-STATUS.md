# Workstream Archive: Component Catalog

Mnemonic: `component-catalog`

Start date: `2026-08-30` (unchanged).

State: concluded successfully at the owner's direction on 2026-09-09;
finalization is provisional until its closure PR merges to main.

## Outcome And Integration

Delivered regular IDE/agent catalog components and published v0.2.11. The owner
explicitly froze implementation scope, accepted the final release work, and
requested closure followed by selecting `project-management` in this checkout.
This mnemonic is retired; residual planning does not reopen this workstream.

Delivery method: pull request to `main`, using the repository's ordinary merge
policy. Implementation milestones include [PR #50](https://github.com/ccozianu/devcapsule/pull/50)
(VSCodium), [PR #62](https://github.com/ccozianu/devcapsule/pull/62)
(component installation/runtime delivery), [PR #63](https://github.com/ccozianu/devcapsule/pull/63)
(release protocol and candidate acceptance), and
[PR #65](https://github.com/ccozianu/devcapsule/pull/65) (final smoke harness).
PR #65 merged at `b7e6086029429d1f60668ef37338b57317576fc6`.
[PR #64](https://github.com/ccozianu/devcapsule/pull/64) delivered the release-branch
naming intake to workflow-improvements. Intake was empty at closure; its
[disposition log](intake-dispositions.md) is retained unchanged.
Closure delivery: [closure branch](https://github.com/ccozianu/devcapsule/compare/main...component-catalog/antigravity-cli) (PR reference recorded when available).

## Delivered Contract

VSCodium is a neutral `codium` interactive surface on the normal project path;
the bespoke `codium_with_claude` path is retired. Antigravity CLI is a pinned
agent contribution with explicit developer acquisition authorization and
checkout-scoped persistence covering `~/.gemini`. Agent binaries are acquired
for local materialization, not redistributed in base images. Codex uses its
complete npm distribution, including adjacent helpers, and declared state seeds
initialize only absent files in fresh managed slots.

Components declare runtime commands, environment, state and contributions.
Home overlays remain user-owned. Recipe 7 bases contain OS/developer tools;
materialization supplies the launcher's exact PEX, with its checksum included in
formation identity. Independent BuildKit stages install each contribution once
per cache identity and copy outputs into different formations. The release
protocol stages immutable candidates away from main, records exact acceptance,
and promotes identical source after integration while keeping a maintenance
release branch.

Permanent records:

- [Release and validation process](../../implementation-notes/devcapsule/2026-09-01-release-and-validation-process.md).
- [Antigravity acquisition analysis](../../implementation-notes/devcapsule/2026-09-02-antigravity-cli-license-and-redistribution-analysis.md) (dated evidence, including the state-footprint correction).
- [Component state slots and home ownership](../../design-notes/devcapsule/state-slots-home-overlay-and-ownership.md).
- [Capability/configuration decisions](../../decisions/product/d-0004-configuration-resolution-and-guided-run.md),
  [agent-neutral bases](../../decisions/product/d-0005-agent-neutral-base-and-optional-agent-components.md),
  [host/platform boundaries](../../decisions/product/d-0006-host-platform-friction-module.md),
  and [resolution matrix](../../decisions/product/d-0007-resolution-matrix-model-and-interface.md).
- [Developer commands and smoke invocation](../../../devcapsule-src/README.md).

## Release And Validation Evidence

[v0.2.11](https://github.com/ccozianu/devcapsule/releases/tag/v0.2.11) was published
2026-09-09 at 22:51:37 UTC and independently confirmed as GitHub Latest. Final
tag, accepted RC3, and retained `release-0.2.11` identify source
`94e798f1d1a7aaab93ae3e47d9636471448a8e66`, integrated into main by ancestry.
[Acceptance record](../../releases/v0.2.11.json).
[Release run 34413922358](https://github.com/ccozianu/devcapsule/actions/runs/34413922358)
passed every gate, including frozen-input comparison with RC3, source/type checks,
packaging, no-Python/no-network proof, component-cache reuse, runtime sessions,
and downloaded-byte verification. The downloaded executable and full manifest
were independently verified locally. Final executable SHA-256:

```text
0f5f6bce218076d8ab74881e32d502895f57a3a15279b182ce7d1cf1016d7dce
```

The final harness passed 579 unit tests, one existing xfail, 9 packaging tests,
and mypy on 128 files. Seven full-base Docker smokes and two preliminary
recursive tests passed. The RC3 executable itself built the complete recipe-7
base, including Node, Temurin and Maven contributions. The JDK installation
was shared with Maven's stage and the final base; subsequent installs were cached.

The real graphical successor ran the published RC3 executable on that new base,
passed exact-plan and toolchain inspection, and exited normally with code 0,
no OOM, at `2026-09-09T22:08:19.014764095Z`. An independent `docker wait` also
returned 0; the agent did not stop or kill it. Owner then accepted proceeding
with delivery. No additional provider-login checklist is claimed.

Retained evidence (do not confuse it with running infrastructure):

- Run ID `8d769574856fb2b7a7e3a296c04d7188`; stopped container
  `devcapsule-e2e-8d769574856fb2b7a7e3a296c04d7188-successor`, ID
  `89bbff543005849e35899b7d45dabc366be754c366a55e58c3f7b5f5927ed26f`.
- Base `devcapsule-base-e2e:v0.2.11-rc3-3e30c6c81a91`, ID
  `sha256:90eece0d93ab9c94265efc1ac77b363e4300d345c58761ab58bc31d20667639a`.
- Successor image `sha256:2e3b67566a8975e834caac5f80a34ef08a34c2818011e7d93a3501621e03b5df`.
- RC3 PEX SHA-256 `32f900903d8a1286c62aae72b0d8e71a3e6a25e68d91fae8464595da472bd6e6`.
- Owned run beneath the capsule's `~/.local/share/devcapsule/e2e-workspaces/`
  contains source, isolated state, manifests, expected plan, launch/inspection
  evidence and `candidate-command.py`. It remains intentionally retained.
  Earlier unrelated historical runs and the control capsule remain untouched.

## Open Threads At Closure

No release or integration feature work remains. Questions and deferred options
for project management, not automatic new implementation:

- Settle checkout-local experimental needs versus project-manifest promotion,
  `init --regenerate`/`config` layering, and base selection. Existing intake and
  the [UX design record](../../design-notes/devcapsule/v1-user-experience.md)
  retain those owner decisions; local-only need implementation was not delivered.
- Plan component updates, matrix data/model cleanup and learning from successful
  unverified combinations together. Collaborator-facing warnings on resolve/run and
  provisional validation evidence need review when that work is selected.
- PyCharm still uses named launcher state fields; its migration to generic slots
  and generic launcher naming remains separate work requiring owner smoke.
- The runtime half of home-ownership validation belongs to `contained-display`;
  its previously delivered coordination items remain with that workstream.
- Recheck deprecated Codex sandbox fallback at the next pin advance. Historical
  sample-project three-provider branches and provisional matrix evidence require
  external-state verification before any planning claim; this closure does not
  claim sample merges or fresh authenticated-provider acceptance.
- Base publication/repinning remains independent maintenance. The candidate base
  stayed local; the released catalog continues to recommend its existing base.
  `recursive-e2e run`/Nox still cover preliminary planning/clone/bootstrap; the
  graphical continuation uses `launch-successor` and `inspect-successor`.
- The user requested moving this checkout to project management after closure.
  No new implementation workstream is selected or proposed by this archive.

Deliberately not preserved as current work: the 1,400-line rolling chronology,
superseded pending-release claims, temporary logs/download caches, and the
superseded release-candidate proposal. Git retains them at
[checkpoint 6ff3d8c](https://github.com/ccozianu/devcapsule/tree/6ff3d8c/engineering-docs/wip/2026-08-30-component-catalog).
The permanent release process records the implemented protocol. Local test
resources listed above remain; this documentation closure performs no pruning.

## Archive Document Index

- [This outcome and evidence](CURRENT-STATUS.md).
- [Intake dispositions](intake-dispositions.md).
