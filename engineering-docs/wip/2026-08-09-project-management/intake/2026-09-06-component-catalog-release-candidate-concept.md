# Intake: A Real Release-Candidate Concept

Delivered 2026-09-06 by `component-catalog`, at the product owner's
direction, after the 0.2.9 mishap: "it feels like we need a real release
candidate concept to avoid future mishaps."

## What Happened

v0.2.9 was tagged, its PEX published to GitHub Releases, and its base
image pushed to Docker Hub on 2026-09-05, with Codex effectively broken
inside every capsule (one binary plucked from a multi-file npm package;
every sandboxed command panicked). The fix landed on `main` the same
day, after the tag. The base tag `v0.2.9` was then re-pushed with a
recipe-6 rebuild, so the registry tag and the matrix pin named different
digests. The owner decided to withdraw 0.2.9 from GitHub and Docker Hub
and make 0.2.10 the target, validated first on the two sample projects
(trading-research, PyCharm with three agents; tictactoe, Codium with
three agents) and only then on the dogfood project. There were no
adopters to hurt; next time there may be.

## What Is Being Handed Over

Design of a release-candidate stage for the release process recorded in
`engineering-docs/implementation-notes/devcapsule/2026-09-01-release-and-validation-process.md`,
answering at least:

1. **What a candidate is.** A tag (`v0.2.10-rc.1`?) that the release
   workflow builds exactly like a release but publishes as a
   pre-release; a base image tagged for the candidate; a matrix that
   pins the candidate base. Note the constraints already in the tree:
   `release-pex.yml` fires on every `v[0-9]*` tag, so an rc tag would
   trigger it as-is; the workflow asserts the embedded mnemonic equals
   the tag; `bump-version.py` accepts only `x.y.z`, so the candidate
   suffix must live in the tag or the mnemonic, not the version field.
2. **What promotes it.** The owner's smokes on the sample projects and
   the dogfood project, each producing a known-good generation (D-0008)
   and converting the provisional matrix entries the candidate carries.
   This is the "claim" of the matrix-learning item delivered today: a
   candidate becomes a release when every combination it pins has a
   claim of a successful run.
3. **How promotion happens under immutable tags.** The final tag points
   at the candidate's commit; the final base tag is the candidate's
   digest under a new name (same digest, so the pin holds), or the
   matrix pins the digest and the final tag is only human addressing.
   The dependency cycle the release note describes (the matrix pins the
   base digest; the released PEX embeds the matrix; the base embeds a
   PEX) must be walked once per candidate, not once per release.
4. **What withdrawal means.** Deleting a GitHub release, a git tag, or a
   Docker Hub tag after publication — when it is acceptable (no
   adopters), what it breaks (every lock pinning the withdrawn digest
   cannot pull; the tag `v0.2.9` in the matrix history), and how the
   record says it happened.
5. **Who runs the candidate.** Today the owner smokes by hand and the
   agent cannot see a GUI; the automated per-component validation
   research already in this intake is the other half.

## Why It Belongs To `project-management`

The release process is repository-wide and crosses every workstream's
deliverables; the candidate stage changes when integration is "done"
for all of them, and it composes three items already in this intake:
the upgrade experience, automated component-version validation, and
the matrix learning from experiments.

## What Accepting Would Mean

Owning the design and amending the release process note; 0.2.10 will be
cut by hand along the lines of point 3 before the concept exists, and
is the case study to design against.
