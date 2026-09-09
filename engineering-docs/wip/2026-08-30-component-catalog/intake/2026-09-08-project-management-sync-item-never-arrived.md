# Intake: The Sync Item Never Arrived; Two Records Say It Did

Delivered 2026-09-08 by `project-management`.

## What Is Being Reported

The intake item `2026-09-06-component-catalog-one-devcapsule-inside-and-outside.md`
was never delivered to `project-management` on `main`. Two of this
workstream's records state or imply that it was:

1. `CURRENT-STATUS.md` on `main`, *Release Target*, "Sync question,
   2026-09-06 night" (commit `4e00985`, merged in PR #61): "went to
   `project-management` as intake … (outbox `802adaf`)".
2. The pause note on `component-catalog/outbox` at `47b4442`, item at
   the head of *Next Resumable Task*: "PR #61 … and the outbox (intake
   `one-devcapsule-inside-and-outside`) merged to `main`".

Verified 2026-09-08 against every ref in this clone: the commit
`802adaf` is not a valid object, the filename appears in no tree on any
branch, and `component-catalog/outbox` at `47b4442` was reset from
`main` at `8d7d2fa` carrying only the registry row and the handoff
copy. `47b4442` is itself still unmerged, so statement 2 is also wrong
about the outbox having landed.

This is the failure family answered on 2026-08-29 under
`2026-08-17-recursive-e2e-audit-undelivered-work.md`: an outbox reset
destroys undelivered mail, and the protocol as specified permits it.
Nothing in the loss reflects on how this workstream did its work — the
send appears to have been made and then overwritten by the next reset,
which is exactly the specified behaviour.

## What `project-management` Has Already Done

It reconstructed the item into its own intake under the original
filename, so the pointer in `4e00985` resolves. The reconstruction is
labelled as such: the owner's question, the diagnosis, the recommended
shape (the launcher delivers its own PEX into the formation at
materialization), and the 0.2.10 advice are recovered from this
workstream's handoff record; the two non-preferred shapes did not
survive anywhere and were reconstructed by `project-management`. One
mechanism fact was added — the inside/outside contract in
`devcapsule/container_runtime/contract.py` is already explicitly
versioned (`RuntimePlan.version` and `ComponentRuntimeTemplate.version`
are written as `1` and refuse any other value), so what is missing is a
compatibility policy rather than a synchronization mechanism.

The item is undispositioned and now queued with the release-candidate
and internal-naming items.

## What This Workstream Is Asked To Do

On resume, through its own outbox:

1. **Correct the two records** so they say what is true of `main`.
   `project-management` did not edit them: restriction 11's carve-out
   protects this workstream's handoff, and only this workstream can
   restate its own account.
2. **Check the two non-preferred shapes** in the reconstructed item
   against whatever the pair actually weighed on 2026-09-06, and
   correct them through `project-management`'s intake if the
   reconstruction misrepresents them. The recommendation and diagnosis
   should not need correcting.

Nothing here changes the workstream's paused state or its resume order,
and neither task blocks the sync disposition.

## Also Observed, For The Owner Rather Than This Workstream

`component-catalog/outbox` at `47b4442` is unmerged, so `main`'s
registry still shows this workstream as active with the 0.2.10 walk
mid-flight rather than paused with it complete. That needs a pull
request the product owner opens.
