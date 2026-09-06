# Intake: Clarify The Semantics Of `init --regenerate` Versus The `config` Family

Delivered 2026-09-06 by `component-catalog`, at the product owner's
direction, after a systematic walk through what `project init
--regenerate` tells the user and what it does. The owner ruled that the
current behaviour is acceptable for now, in the interest of speed, and
that the semantics be settled here rather than patched case by case.

## The Principle The Owner Stated

`init` exists to help a contributor operate on the `.devcapsule` in the
source tree — the project-owned manifest and platform lock. That it also
updates the local configuration that serves `project run` (the
developer-owned checkout record and its resolution) is a convenience,
not its purpose. The `config` family owns the local configuration.
Today the two overlap in ways the messages do not admit.

## What Is Being Handed Over

A design ruling on the boundary, and the message and flag changes that
follow from it. The discrepancies found on 2026-09-06, all verified
against the code:

1. `--regenerate --need …` derives the lock from the flagged need but
   never rewrites the manifest's authored `need` line, and nothing checks
   the lock's `capabilities-digest` against the manifest. The two diverge
   silently. `config need` is the only path that keeps them together.
2. Identity flags (`--name`, `--slug`, `--creator`, `--project-mount`) on
   a re-init are accepted, printed in the report as if applied, and never
   written to the standing manifest.
3. The design note says `--regenerate` "does not touch the
   developer-owned checkout records". It rewrites the owner's own record:
   every project recommendation is re-authorized for the owner's checkout
   without a question, and the base-image acceptance is re-asked because
   the lock digest changed. The behaviour may be right; the sentence is
   not.
4. The init report prints "Recommended docker-daemon = <justification>"
   where the value belongs.
5. Two messages still name `init --regenerate` as the sole remedy — for a
   hand-edited manifest and for a legacy lock met at run time — which is
   only right once item 1 is settled.

Candidate directions the owner did not choose between: `--regenerate`
refuses `--need` and identity flags on a standing manifest and names
`config need` (and a future manifest-editing verb) instead; or
`--regenerate` becomes the manifest-editing verb and rewrites the
authored lines it is given, with `config` confined to the local half.
Either way the help text, the fully-initialized refusal, the design
note's `--regenerate` section, and the README should say the same thing.

## Why It Belongs To `project-management`

The boundary between project-owned and developer-owned configuration is
the V1 user-experience design's spine ("Four Things With Different
Owners"); changing which command writes which artifact is a product
ruling that every workstream's users meet, not a `component-catalog`
matter. It also intersects the open checkout-local-needs ruling (whether
`config need` defaults to a local experiment) already with the owner.

## Evidence

- `initialize_project` in `project_operations.py`: the flag only disables
  the "already fully initialized" refusal and the "keep the existing
  lock" branch; identity and need are re-elicited into the derivation but
  `_write_manifest` appends only new recommendations to an existing
  manifest.
- The 2026-09-05 scratch reproduction: `init --regenerate --unverified
  --need <six capabilities>` on a copy of this repository's `.devcapsule`
  produced a six-capability lock beside a five-capability manifest with
  no warning.
- The `--regenerate` section of the V1 user-experience design note versus
  the owner-record writes at the end of `initialize_project`.

## What Accepting Would Mean

Owning the ruling and its sequencing; the implementation is small once
the direction is chosen (message text, flag refusals or manifest
rewrites, one design-note paragraph, one report line). Nothing blocks on
it: the owner has accepted current `init` for now.
