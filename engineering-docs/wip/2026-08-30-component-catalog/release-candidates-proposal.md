# Release Candidates And Maintenance Branches

Status: accepted by the owner, 2026-09-09; implementation and first release
experiment in progress. `release-V` is used from candidate preparation onward.

## Owner's Requested Direction

Prepare a release away from main on a branch such as `rc-0.2.11`, push tags
`v0.2.11-rc0`, `v0.2.11-rc1`, and publish them as GitHub prereleases for smoke
and later fuller E2E testing. When accepted, retain `release-0.2.11` and publish
`v0.2.11` only after its changes have reached main through merge, cherry-pick,
or a documented engineering exception with rationale. Main remains open for
unrelated development. Future fixes can start from the released code even when
main is not shippable.

## Accepted Protocol

1. Cut the candidate from an identified mainline commit. For a maintenance
   release, cut from the exact previous release tag instead. Record that base;
   it bounds the changes that must be accounted for during main integration.
2. Stage release changes and push an immutable candidate tag. Candidate builds
   require membership in the matching candidate/release branch, not mainline.
   Each fix gets another commit and a new candidate number; never move tags or
   replace published candidate assets.
3. Run the mechanical gates, stage and download-verify artifacts, then publish
   the GitHub release with `prerelease=true` and `make_latest=false`. Preserve
   the candidate commit, artifact digests, build inputs, and validation results.
   Use package version `0.2.11rc0` for Git tag `v0.2.11-rc0`.
4. Accept one exact candidate, with smoke/E2E evidence naming its commit and
   artifact checksum. A moving branch or a general "smoke passed" is not the
   object of acceptance. Main may continue advancing; do not automatically merge
   it back into the candidate or rebase a tested candidate onto it.
5. Integrate the candidate changes into main by the repository's normal PR
   policy. Keep the release branch at the tested source commit. Resolve conflicts
   on the integration side; if any release source changes, cut another candidate.
6. Create `release-0.2.11` at the accepted candidate commit and push `v0.2.11`
   there. Keeping `release-0.2.11` from the beginning is a simpler equivalent:
   candidate status is already carried by tags and prerelease metadata. The
   separate `rc-0.2.11` branch remains a valid operator preference.
7. The final gate verifies candidate acceptance, matching source commit and
   inputs, membership in the required release branch, and recorded main
   integration or a scoped approved exception. The old first-parent-main
   requirement must be removed. Build final-version artifacts, rerun automated
   validation on the actual final bytes, and only then publish the stable release.

## Integration Evidence

An ordinary merge is mechanically identifiable through candidate-commit
ancestry in main. The histories/trees need not be identical: main can contain
additional work and even be unshippable.

Cherry-picks and squashes need an explicit record of the release delta and the
main commits/merged PR that carry it. Patch equivalence can help check simple
cases but does not prove semantic equivalence after conflict resolution,
refactoring, squashing, or subsequent reverts. Changed adaptations require
reviewed integration evidence; an unavailable fix uses the explicit exception
route instead of being silently called integrated. The gate verifies that the
referenced main revisions exist in main's history and that the reviewed record
covers the released changes.

An exception is scoped to a release/candidate, records who authorized it, why
main integration cannot precede publication, and the owner and follow-up for
forward-porting. Keep this evidence in engineering documentation and reference
it from the release manifest. Evidence added after candidate acceptance should
live outside the candidate source tree, so recording promotion does not alter
what was tested. A generic boolean bypass or an arbitrary markdown filename is
not sufficient evidence.

## Artifact Promotion Boundary

The PEX embeds version and source identity. A `0.2.11rc0` PEX is not byte-identical
to a `0.2.11` PEX. Recommended initial contract: same source revision and frozen
build/dependency inputs, with only intentional release-identity metadata changes,
followed by the full automated gate against the final artifact. This is source
promotion with a final packaging build, not literal reuse of candidate bytes.

If exact byte-for-byte promotion becomes mandatory, produce the final-shaped
artifact during candidate preparation and store candidate identity outside it.
That requires changing today's identity contract and clearly displaying candidate
status to testers; it should be a deliberate separate decision. Never rename a
candidate artifact while leaving an undisclosed rc version embedded inside it.

## Maintenance

For example, branch `rc-0.2.12` (or directly `release-0.2.12`) from `v0.2.11`,
apply the minimal dependency/security fix, test its candidate, forward-port the
fix to main or record the approved exception, then tag `v0.2.12`. The previous
release tag stays immutable. A branch per exact version is a convenient named
anchor; the immutable tag is the authoritative starting point for a patch.

This removes dependence on main being releasable. It does not promise that a
complete cold build/E2E run takes minutes; that requires measured build times,
retained caches and a deliberately chosen validation gate. Older maintenance
releases must not replace a newer supported line as GitHub's Latest release.

## Repository Protocol Changes Needed

WORKFLOW.md currently requires every non-main branch to belong to a workstream,
use its prefix, originate on main, and synchronize with main before work. The
proposed `rc-*`/`release-*` refs and maintenance releases need explicit supported
exceptions and an owner/routing rule. Release branches must be able to outlive
the implementation workstream. The protocol owner must receive this amendment;
creating miscellaneous unregistered workstreams is not the solution.

## References

- [GitHub prereleases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Python version conventions](https://packaging.python.org/en/latest/discussions/versioning/)
- [Git ancestry check](https://git-scm.com/docs/git-merge-base)
- [Git patch equivalence](https://git-scm.com/docs/git-cherry)

## Operator Commands And Promotion Record

The workstream remains selected on its working branch. Release branches are
persistent release anchors, authorized by the owner on 2026-09-09 while the
workflow owner resolves naming policy. The intake was pushed through
`component-catalog/outbox`; its main delivery is tracked in the handoff.

Create `release-0.2.11` and `v0.2.11-rc0` at the prepared commit, push both refs
atomically, and wait for Publish DevCapsule PEX to succeed. Download and smoke the
prerelease PEX. Do not accept a moving branch or use another artifact's evidence.
Use `scripts/prepare-promotion.py` to prepare the record from that prerelease:

```text
cd devcapsule-src
.venv/bin/python scripts/prepare-promotion.py v0.2.11-rc0 \
  --baseline FULL_PREPARATION_BASE_SHA --accepted-by OPERATOR \
  --evidence 'Exact candidate smoke result and/or Actions run URL'
```

The helper downloads the candidate manifest and PEX, checks its checksum, and
writes `engineering-docs/releases/v0.2.11.json`. Commit this on the integration
side, never on the tested release branch. Integrate the candidate and record
through normal PR delivery. The helper defaults to ancestry integration:

```json
{
  "schema-version": 1,
  "tag": "v0.2.11",
  "candidate-tag": "v0.2.11-rc0",
  "source-revision": "FULL_CANDIDATE_COMMIT_SHA",
  "candidate-sha256": "SHA256_OF_ACCEPTED_PEX",
  "accepted-by": "operator",
  "evidence": ["Exact artifact smoke result and Actions run URL"],
  "integration": {"method": "ancestry", "baseline": "FULL_PREPARATION_BASE_SHA"}
}
```

For a squash/cherry-pick, change `method` to `reviewed`, add `main-commits` (full
SHAs), `reviewed-by`, `rationale`, and `covers-release-delta: true`. The assertion
covers the entire baseline-to-candidate delta. Every referenced commit must be
reachable from main; review, rather than a patch-ID heuristic, vouches for any
adaptation. An `exception` instead requires `authorized-by`, `rationale`,
`forward-port-owner`, and `follow-up`. All records are reviewed engineering
records read from main; no arbitrary bypass input is accepted.

After integration:

```text
git tag v0.2.11 'v0.2.11-rc0^{commit}'
git push origin v0.2.11
```

The final workflow requires the published prerelease and verifies its PEX hash,
manifest identity, pinned bases, dependency distributions and embedded Python
fingerprints against the new final PEX. The manifest embeds the promotion record
and the main revision from which it was read. Main can advance afterward; an
unchanged acceptance remains valid on retries. Missing or partial staged assets
fail closed; recover from the retained Actions artifact rather than rebuilding
or overwriting a published candidate. Failures requiring source changes use the
next RC number.

This first implementation automates each tag's build/test/publication and checks
promotion. Candidate acceptance, PR integration, and pushing the final tag remain
operator/agent steps. It does not invent owner GUI acceptance or silently merge
PRs. Those steps can later be driven by a promotion workflow using the same gate.
