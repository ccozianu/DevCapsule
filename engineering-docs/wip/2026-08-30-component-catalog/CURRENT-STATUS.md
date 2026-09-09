# Workstream Current Status: Component Catalog

Mnemonic: `component-catalog`

Start date: `2026-08-30` (unchanged).

State: **paused 2026-09-09 at the product owner's direction**, with v0.2.11
accepted as a good milestone. The workstream stays open for future components.

Integration target: `main`

Working branch: `component-catalog/antigravity-cli`

Standing outbox: `component-catalog/outbox`

Delivery method: pull request, one per validated component (unit tests and a
product-owner smoke); follow the repository's configured PR merge policy.

Requirements: `R-PRODUCT-001`, `R-PRODUCT-002`, `R-SCOPE-001`, `R-DOCKER-001`.

## Pause And Next Resumable Task

The owner replaced the proposed closure with a pause. The unmerged archive and
registry removal are withdrawn; this mnemonic and its WIP records remain in
use. v0.2.11 is shipped, and no release or implementation work remains for that
milestone. All work is committed. No new component implementation is started.

**Planned next step on resume:** the owner selects the next component and its
scope; reverify main, this handoff and intake, then continue the catalog work.
The separately registered `eclipse-surface` workstream retains its current
routing until the owner changes it. Existing coordination questions stay with
project management and are not an automatic component backlog.

The owner's earlier checkout-selection instruction remains: after recording the
pause, move this clean checkout to `project-management/coordination`. Publishing
this workstream's pause records uses its standing outbox. GitHub connector PR
creation last failed with HTTP 403, while Git SSH pushes work; a pushed pause
record is pending main delivery until its PR merges.

## Delivered Milestone

VSCodium is a neutral `codium` interactive surface on the normal project path.
Antigravity CLI is a pinned, locally acquired agent component with developer
acquisition authorization and checkout-scoped `~/.gemini` persistence. Codex
uses its complete npm distribution and declared managed-state seeds.

Recipe 7 bases contain OS/developer tools. Materialization delivers the
launcher's exact PEX and includes its checksum in formation identity.
Independent BuildKit contributions install once per cache identity and copy
outputs into different formations. Immutable RC tags stage releases away from
main; final publication promotes accepted source after main integration.

Implementation and validation reached main through PRs
[#50](https://github.com/ccozianu/devcapsule/pull/50),
[#62](https://github.com/ccozianu/devcapsule/pull/62),
[#63](https://github.com/ccozianu/devcapsule/pull/63), and
[#65](https://github.com/ccozianu/devcapsule/pull/65).
PR #65 merged at `b7e6086029429d1f60668ef37338b57317576fc6`.
The release-branch naming intake reached workflow-improvements through
[PR #64](https://github.com/ccozianu/devcapsule/pull/64).

Canonical records: [release process](../../implementation-notes/devcapsule/2026-09-01-release-and-validation-process.md),
[Antigravity analysis](antigravity-cli-license-and-redistribution-analysis.md),
[home/state ownership](../../design-notes/devcapsule/state-slots-home-overlay-and-ownership.md),
and [resolution-matrix decision](../../decisions/product/d-0007-resolution-matrix-model-and-interface.md).

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

## Intake And Historical Correction

Intake is empty at pause. [PR #69](https://github.com/ccozianu/devcapsule/pull/69)
merged the standing-outbox acknowledgment of the correction delivered by
PR #67. Its [disposition log](intake-dispositions.md) remains here in WIP.

The 2026-09-06 inside/outside-runtime intake had not reached main despite this
workstream's earlier send/pause claims. Original commit
`802adafa3d545895b979288a57cf1363329b94c7` is readable locally but not reachable
from a current branch. Its content is also preserved in the published history
at [recovery checkpoint f2c1034](https://github.com/ccozianu/devcapsule/blob/f2c1034/engineering-docs/archive/2026-08-30-component-catalog/recovered-sync-intake.md).
The original alternatives were tag-based base selection and build-mnemonic
equality; project-management's reconstruction introduced an explicit
compatibility-policy option. That is its analysis, not the sender's original
wording. The owner's later choice of launcher PEX delivery shipped in v0.2.11.
The lost-mail workflow concern is separate from that completed implementation.

## Open Threads

- **Awaiting the owner:** which component to take next, and when to resume;
  future component scope is not selected by this pause.
- **Weighed and unresolved:** coordinate PyCharm's generic-slot migration,
  component updates/matrix cleanup, checkout-local needs and experimental
  validation with project management. Recheck deprecated Codex sandbox fallback
  at the next pin advance; authenticated-provider/sample acceptance is not
  inferred from the automated release results.
- **Deliberately not preserved as current work:** the long rolling chronology,
  superseded closure/pending-release claims, and temporary logs/download caches.
  Git preserves the chronology at [6ff3d8c](https://github.com/ccozianu/devcapsule/tree/6ff3d8c/engineering-docs/wip/2026-08-30-component-catalog).
  Retained test resources above remain intentionally available; no pruning or
  unrelated-container changes accompany this pause.

## Workstream Document Index

- [Current handoff](CURRENT-STATUS.md).
- [Intake dispositions](intake-dispositions.md).
- [Antigravity CLI acquisition analysis](antigravity-cli-license-and-redistribution-analysis.md).
- [Release-candidate proposal](release-candidates-proposal.md) (historical accepted
  design; the permanent release process and published v0.2.11 supersede its
  pending-promotion checkpoint).
