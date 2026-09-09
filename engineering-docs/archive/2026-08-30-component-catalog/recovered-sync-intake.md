# Intake: One DevCapsule Inside And Outside The Capsule

Delivered 2026-09-06 by `component-catalog`, at the product owner's
direction, at the end of the 0.2.10 walk: "do we have a solution to
have devcapsule the self-contained CLI be in absolute sync with the
base image (and the devcapsule build inside the docker base image be
the same version of the devcapsule outside)?"

## What Happened

The base image embeds the release PEX at `/opt/devcapsule/bin/devcapsule.pex`
(`base_image.py`, `PEX_DESTINATION`); every formation's entrypoint runs that
embedded PEX's `runtime` command (`materialization.py`, `ENTRYPOINT_CONTRACT`),
and the host-open bridge calls it too. The PEX carries the resolution matrix,
and the matrix pins the base by registry digest (D-0007). Walking 0.2.10 in
the order the release note prescribes produced three artifacts named 0.2.10:

| Artifact | Pins base digest | Carries the v0.2.9 pin |
|---|---|---|
| Released PEX (GitHub, tag `v0.2.10` at `2415029`) | `76a07cb9…` (first push) | yes |
| PEX inside the base the tag now names (`4bb691b5…`) | `76a07cb9…` (byte-identical to the released PEX) | yes |
| `main` after the workstream branch merges | `4bb691b5…` | no |

The inside and the released outside are identical today. What is not in
sync is the released PEX with the image it sits in, and `main` with the
release. The release workflow (`release-pex.yml`) re-run on an existing
tag compares the rebuilt PEX byte-for-byte with the published asset and
fails on any difference, so "rebuild 0.2.10 to capture the change" means
moving the tag and deleting the release: a withdrawal in miniature. The
workstream's advice to the owner was to leave 0.2.10 as released and let
the change ship as the next version.

## Why No Walk Order Can Fix It

The base's digest covers the layer holding the PEX, and the PEX holds the
digest. A PEX that pins the digest of the image that embeds it is a fixed
point of a content hash, and it does not exist. Every ordering gives one of
two outcomes: the embedded PEX pins the previous push, or the released PEX
and the embedded PEX differ. The 0.2.10 walk hit both; the second base push
over the same tag was the symptom. The release-candidate concept delivered
earlier today makes the walk safer but cannot escape this.

What sync actually has to cover is narrower than the artifact. The runtime
package that runs inside the container (`devcapsule_runtime`) imports
nothing from the host-side package and never reads the matrix; it executes
the runtime plan and the host-open bridge. The matrix bytes inside the base
are dead weight. The mismatch that hurts is the host CLI writing a plan
vocabulary the inside runtime does not understand, which is what made the
v026 base unusable for the vscode adapter and forced the runtime-PEX
override volume during the codium smokes.

## What Is Being Handed Over

The decision on how "one DevCapsule inside and outside" is achieved. The
workstream's diagnosis names three shapes, in its order of preference;
the sender assigns no priority or release target.

1. **The launcher delivers its own PEX into the formation.** Materialization
   copies the running PEX into the local environment image the way the base
   recipe copies it today, with the PEX's sha256 in the materialization
   identity so a CLI upgrade rebuilds the thin layer. Inside equals outside
   by construction, for every base. The base becomes a plain toolchain
   image; base releases and CLI releases decouple, so the matrix pin never
   needs a same-version base, and a CLI-only fix (the 0.2.9 codex fix) never
   again forces a base rebuild and a withdrawal. The runtime-PEX override
   volume proved the mechanics; a bind mount needs a host path, which a
   remote daemon lacks, so copying at materialization is the robust form.
   Touches: the base recipe and its `v<client-version>` tag convention, the
   materialization identity and the entrypoint contract, D-0007's pin
   vocabulary, the release process note, `images inspect` labels.
2. **Keep embedding, pin the self-base by tag.** The matrix pins the base
   tag equal to its own version and the digest is read from the registry at
   `init`. The fixed point closes at version level. It breaks D-0007's
   offline, daemon-free resolution and depends on tag immutability, which
   the 0.2.10 walk itself violated.
3. **Keep everything, define sync as build-mnemonic equality and enforce
   it.** The base already carries `devcapsule.pex.build-mnemonic`; the
   launcher refuses a base whose label differs from its own version. Catches
   drift, gives no "absolute" sync, and leaves every released PEX pinning
   the previous push.

Two facts stand regardless of the choice: `main` must not remain at the
tagged version after a tag, or a PEX built from it is mislabeled; and
under shape 1 the repin commit this workstream just made would not exist,
because the CLI would carry no self-referential digest.

## Why It Belongs To `project-management`

It changes what a base release is, what a CLI release contains, and how
the two are validated, so it crosses `component-catalog` (the matrix and
materialization), `contained-display` (the entrypoint and the runtime
contract the inside PEX executes), and the release process. It also
reshapes the release-candidate concept delivered earlier today: under
shape 1 a candidate is a PEX alone, and bases are validated on their own
cadence.

## What Accepting Would Mean

Deciding the shape, recording it as a product decision (an amendment to
D-0007 at least), and sequencing the implementation with the
release-candidate and upgrade-experience items already in this intake.
The evidence is in the `component-catalog` handoff (*Release Target:
v0.2.10*, walk status entries of 2026-09-06) and in
`engineering-docs/implementation-notes/devcapsule/2026-09-01-release-and-validation-process.md`.
