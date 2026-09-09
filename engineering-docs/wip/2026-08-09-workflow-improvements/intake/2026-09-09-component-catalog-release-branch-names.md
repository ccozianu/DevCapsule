# Distinguish workstream branches from release and maintenance refs

Sender: `component-catalog`. Recipient: `workflow-improvements`.

The owner requests a naming convention identifying workstream branches rather
than treating every non-main branch as a workstream branch. The registry already
records workstream names and associations; real repositories also have release,
maintenance, and legacy refs. This is a reusable workflow question, owned here.

The immediate case is v0.2.11: prepare on `release-0.2.11`, publish immutable
`v0.2.11-rcN` prereleases, then promote accepted source to `v0.2.11` after main
integration or a scoped engineering exception. Retain the release branch for
maintenance. A later patch may start from the previous release tag when main is
not shippable. Release refs must outlive the implementation workstream and must
not be rebased onto advancing main after candidate testing.

WORKFLOW.md's blanket branch ownership, prefix, main-origin and synchronization
rules need this distinction. The issue is not an exact two-branch limit: the
protocol already permits multiple working branches alongside the outbox.
Please define recognition, editing ownership/routing, lifetime, and maintenance
rules for non-workstream refs while preserving explicit workstream selection.

Owner ruling on 2026-09-09: send this item, assume the general issue will be
resolved, and proceed with the release experiment under bias for action. For
this release, `component-catalog` remains the selected implementation workstream;
`release-*` refs are release anchors, not new workstreams. This instruction
authorizes the exception now without editing the frozen WORKFLOW.md here.

Acceptance means incorporating this distinction into the reusable workflow and
its embedded templates, with examples covering an ordinary release and a patch
from a prior tag. Priority and sequencing remain the recipient's decision.
