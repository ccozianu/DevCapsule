# Intake: A Development Blog Under `engineering-docs/blog/`

Delivered 2026-09-06 by `component-catalog`, at the product owner's
direction: "the development of this is a very interesting exercise,
probably as valuable as the software itself."

## What Is Being Handed Over

A new permanent folder, `engineering-docs/blog/`, travelling in this same
delivery, containing:

- a `README.md` stating the folder's purpose and the conventions the first
  entry follows (one Markdown file per entry, `YYYY-MM-DD-slug.md`,
  framework-neutral Markdown that reads well in any preview, permanent
  links into the repository by mainline commit SHA, quotations lightly
  edited and said so);
- the first entry, *When should a tool refuse? Taking stock of
  DevCapsule's refusal UX*: a preamble for a human reader, then the
  owner's question and the agent's answer on when DevCapsule refuses a
  configuration, on what grounds, to whom, and with what message;
- one new `index.md` section listing both.

And the decisions the owner asked `project-management` to orchestrate:

1. **Publishing target.** A GitHub-backed site (GitHub Pages from this
   repository or a sibling) or an account-storage-backed one. The owner
   named both as candidates and settled neither.
2. **Structure.** Flat files for now. Whether entries gain subfolders (by
   series, author, or year), a generated index, images, or front matter
   added at publish time. The README deliberately leaves this open.
3. **Process.** Who proposes an entry, who reviews before it is public,
   how a published entry is corrected (the README's stance: later entries
   correct, earlier ones are not rewritten), and how conversation
   excerpts are attributed.
4. **Cadence and scope.** Which moments of the development earn an entry.
   The owner's framing is "interesting aspects of developing this", not a
   changelog.

## Why It Belongs To `project-management`

The blog is repository-wide and outward-facing. It crosses every
workstream (any of them may produce an entry), and its publishing target
is an infrastructure and product-presentation decision, not a
`component-catalog` matter. `component-catalog` wrote the first entry only
because the conversation it records happened there.

## Evidence

The first entry itself. The conversation it reproduces began with a
resolution refusal met while regenerating the trading-research sample's
lock on 2026-09-05, moved through a data fix (PyCharm's missing gen2
matrix entry, on the workstream branch), and stopped at the owner's
request to first establish a shared understanding of the refusal UX
before choosing vocabulary. That shared-understanding discussion is still
open in `component-catalog` and is not part of this item.

## What Accepting Would Mean

Owning the four decisions above and recording them in the blog's README
(or a design note it links to); the folder and the first entry stand as
delivered. Nothing in this item blocks other work; the owner said the
"meat of the discussion" resumes after the folder exists.
