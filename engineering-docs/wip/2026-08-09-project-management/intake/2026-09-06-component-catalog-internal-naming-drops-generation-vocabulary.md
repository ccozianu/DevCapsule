# Intake: Internal Naming Drops The Generation Vocabulary

Delivered 2026-09-06 by `component-catalog`, at the product owner's
direction, prompted by the commit subject `feat: PyCharm gains a
provisional gen2 edge (matrix embedded-15)`: "we need to drop gen2 as we
are inside a pre-release 0.x and I am not aware of any gen1 still active
in the codebase."

## What Is Being Handed Over

A naming ruling for internal records — commit messages, handoffs, bug
records, decision amendments, code comments and identifiers — that
complements the adopter-facing ruling of the same day (D-0007 amendment
2026-09-06: adopters read *validated / not yet validated*, components,
versions, bases; never *edge* or *substrate*). The internal vocabulary
has spread: 2 of the last 40 commit subjects on `main` and 9 permanent
documents carry `gen1`/`gen2`/`substrate`, and the words carry almost no
information at this stage of the project.

The facts to rule on:

1. **`gen1` is still active, in one place.** The `postgresql-client`
   component (delivery policy `base-image`; the base's apt list ships
   it) has exactly one matrix entry, on the older generation. Every need
   containing `postgresql-client` therefore still resolves to the v026
   base — the `pycharm-full` golden lock does. The newer bases ship the
   same package, so the missing entry is evidence, not capability.
   Adding it, then retiring the v026 pin and its entries (D-0007 makes
   retirement an explicit act), leaves a single generation.
2. **With one generation, the concept says nothing.** The substrate was
   introduced on 2026-09-02 so that a base rebuild would not orphan every
   validation; that purpose stands, but the *name* of the single current
   generation need not appear anywhere. Options: keep the field with a
   neutral value derived from the OS release (`ubuntu-24.04`), rename it
   to something an engineer reads without a glossary (*base family*,
   *base line*), or fold it into the base pin until a second generation
   exists.
3. **Commit subjects and records name what changed for whom.** The
   subject above becomes, for instance, `feat: PyCharm is validated on
   the v0.2.9 base (provisional)`; the matrix version stays in the body.
   A short house style for matrix commits (component, version, base,
   evidence status) would make the log readable to someone outside the
   workstream.
4. **Where the rename reaches.** Code identifiers (`_VerifiedEdge`,
   `substrate`, `_SUBSTRATE_GEN2`) and tests are the resolution-matrix
   cleanup already on the backlog; D-0007's text is a decision record and
   is amended, not rewritten; handoffs and bug records are history and
   stay as written.

## Why It Belongs To `project-management`

Naming that crosses every workstream's commits and records is a house
style, not a `component-catalog` matter, and the ruling on retiring the
older generation is a matrix-wide product decision that touches the
release process (which bases stay on Docker Hub) and the withdrawal of
0.2.9 decided today.

## What Accepting Would Mean

Ruling on points 1 and 2 and recording the house style of point 3 where
commit conventions live; `component-catalog` can add the
`postgresql-client` entry and retire the older base in the same matrix
advance as the 0.2.10 repin once ruled.
