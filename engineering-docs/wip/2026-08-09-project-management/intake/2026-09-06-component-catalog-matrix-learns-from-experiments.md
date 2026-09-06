# Intake: The Matrix Learns From Adopters' Experiments, Then Gates On Claims

Delivered 2026-09-06 by `component-catalog`, at the product owner's
direction, given while ruling on the refusal UX (D-0007 amendment of the
same date).

## What Is Being Handed Over

Two design problems, in sequence:

1. **Learning from experience.** An owner or adopter who runs a
   combination the matrix has not validated does so as an *experiment*
   (`--unverified`), and the generated lock records exactly which
   component versions ran on which base. When such an experiment works,
   that fact should be able to reach the matrix — today the only path is
   the owner hand-editing `resolution_matrix.py` with an evidence string.
   Design the channel: what an adopter submits (the lock's
   `unverified-combinations`, the known-good generation D-0008 already
   records on a successful run, a formation identity?), what counts as
   "ran successfully", how a submission becomes a matrix entry, and how
   provisional entries are told apart from evidenced ones.
2. **Gating, later.** Once claims exist, a change to the matrix on
   mainline should be gated on the existence of a claim, for every
   combination the change adds, that it has run successfully. Design
   where that gate lives (pull-request check, release process, both) and
   what a claim must carry to count.

## Why It Belongs To `project-management`

It spans the resolution matrix (`component-catalog` hosts the data), the
release and validation process (recorded 2026-09-01), D-0008's known-good
history, the CLI's message surface, and the upgrade-experience feature
already in this intake (2026-09-03) — of which this is the "who verifies,
what evidence gates the advance" strand made concrete. The owner framed
the sequencing: warn owners and collaborators the same way for now, learn
from experience next, gate afterwards.

## Evidence

- The 2026-09-05 case: PyCharm was validated only on the older base
  generation, Antigravity only on the newer; the owner had in fact run
  PyCharm on the newer base all day, and the matrix learned it only by
  hand, as a provisional entry citing that session.
- Every agent CLI pin advanced this week carries a provisional entry
  whose evidence is "pending the owner's smoke"; there is no way for the
  smoke, when it happens, to convert the entry except by another hand
  edit.
- The lock already carries the fact an experiment would report
  (`unverified-combinations`), and D-0008 already records successful
  runs; the pieces of a claim exist, the channel does not.

## What Accepting Would Mean

Owning the two designs above and their sequencing against the rest of
V1. Nothing here blocks current work: the refusal-UX ruling is
implemented without it.
