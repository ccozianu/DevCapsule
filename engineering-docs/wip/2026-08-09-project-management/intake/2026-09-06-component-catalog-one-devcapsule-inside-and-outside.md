# Intake: One DevCapsule, Inside And Outside

Delivered 2026-09-06 by `component-catalog`, at the product owner's
direction, from the 0.2.10 repin.

**Reconstructed 2026-09-08 by `project-management`; the original was
lost in transit.** The `component-catalog` handoff on `main` records
this item as sent at outbox commit `802adaf`
([`4e00985`](https://github.com/ccozianu/devcapsule/commit/4e00985)),
and the workstream's pause note records it as merged. Neither is true
of `main`: the commit exists in no ref, the file exists in no ref, and
`component-catalog/outbox` was reset from `main` on 2026-09-07 carrying
only the registry row and the handoff copy. This is the outbox-reset
loss already answered on 2026-08-29 under
`2026-08-17-recursive-e2e-audit-undelivered-work.md`, recurring. See
that disposition and this workstream's handoff.

What follows is recovered from the diagnosis preserved in the
`component-catalog` handoff on `main` (*Release Target*, "Sync
question, 2026-09-06 night"), plus mechanism read from the tree on
2026-09-08. **The owner's question, the diagnosis, the recommended
shape, and the 0.2.10 advice are recovered from that record. The
option space in *What Is Being Handed Over* below is reconstructed by
`project-management`, not the sender's original wording; the sender's
two non-preferred shapes were not written down anywhere that
survived.** Read the shapes as this workstream's reconstruction and
let `component-catalog` correct them on resume.

## The Question

Seeing the repin diff — the matrix pinning a base digest, the base
embedding a PEX built from a tagged revision — the product owner asked
whether the self-contained CLI and the runtime the base embeds can ever
be in absolute sync.

## The Diagnosis

Not while the CLI pins the base digest and the base embeds the CLI.
A PEX whose matrix pins the digest of the image that contains it is a
content-hash fixed point: changing the PEX changes the image digest,
which changes what the PEX must pin, which changes the PEX. The 0.2.10
walk demonstrates it concretely — the base had to be pushed, its digest
read back, and the matrix repinned, and the first push carried a
pre-tag PEX for exactly this reason.

The important half of the diagnosis is that **absolute sync is not what
is needed**, because the inside runtime never reads the matrix. What
the two halves actually share is narrow:

- `ENTRYPOINT_CONTRACT` in `devcapsule/materialization.py` — the
  formation's entry process is `/opt/devcapsule/bin/devcapsule.pex
  runtime`, so the inside PEX is invoked by one subcommand with one
  argument.
- The two JSON documents the outside writes and the inside reads:
  `/etc/devcapsule/runtime-plan.json` and
  `/etc/devcapsule/component-runtime-template.json`.

Everything else the outside CLI does — resolution, pinning, locks,
acquisition, authorization, image building — the inside PEX never
executes.

**A fact worth adding to the sender's diagnosis** (read from
`devcapsule/container_runtime/contract.py` on 2026-09-08): that narrow
surface is *already explicitly versioned*. `RuntimePlan.version` and
`ComponentRuntimeTemplate.version` are both written as `1` and both
refuse any other value with `RuntimePlanError`. So the inside/outside
coupling is a versioned data contract that has never advanced past its
first version, not an implicit whole-program coupling. That reframes
the question: what is missing is not a synchronization mechanism but a
**compatibility policy** — what an older inside runtime is required to
do when a newer outside writes a version it does not know, and what
carries the guarantee that a given base can host a given CLI.

## What Is Being Handed Over

A decision on which shape the project adopts. Reconstructed option
space:

1. **The launcher delivers its own PEX into the formation at
   materialization** — the sender's recorded preference. The base stops
   being the source of the runtime; whatever CLI the developer runs
   places itself into the formation, so inside and outside are the same
   build by construction and the fixed point disappears. Costs: the
   base still needs *some* runtime for the recipe-6 boot path, and
   `devcapsule.pex.sha256` / `devcapsule.pex.build-mnemonic` on the
   image stop describing what actually runs.
2. **Keep the embedded runtime, make the contract's compatibility
   policy explicit.** Advance `version` when the documents change,
   state the support window, and have the outside refuse or degrade
   deliberately against a base whose inside runtime is too old — the
   image labels already carry the build mnemonic needed to check this
   before launch. Costs: two supported versions of the contract, and
   the check has to exist.
3. **Break the pinning cycle instead** — the matrix addresses the base
   by tag or by a digest recorded outside the released PEX, so the PEX
   is not part of what it pins. Costs: weakens the immutability the
   digest pin buys, which D-0007 chose deliberately.

The `component-catalog` handoff notes that the outcome of this decision
"decides whether the matrix keeps pinning base digests at all", which
is option 3's stake.

## Recovered Advice On 0.2.10

Asked whether to rebuild a v0.2.10 CLI to capture the change: **no.**
The release workflow re-run on an existing tag compares the PEX
byte-for-byte with the published asset, so a rebuild means moving the
tag and deleting the release. The released 0.2.10 stays valid — the
digest its matrix pins is still served — the change ships with the next
version, and `main` should leave 0.2.10 behind.

## Why It Belongs To `project-management`

The shape decides what a release *is* — whether a base release and a
CLI release are one act or two — so it composes with the
release-candidate concept, the upgrade experience, and automated
component-version validation, all already in this intake. It also
reaches `contained-display`, which owns the supervisor core that the
entrypoint contract boots.

## What Accepting Would Mean

Ruling on the shape, amending D-0007 where it changes what the matrix
pins, and amending the release process note where it changes the
dependency cycle a release walks. `component-catalog` is paused and
holds the implementation; its handoff instructs it not to start any of
the three shapes without this disposition.
