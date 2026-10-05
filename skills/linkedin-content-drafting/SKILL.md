---
name: linkedin-content-drafting
description: "Draft review-ready LinkedIn posts; never auto-publish."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [linkedin, social-media, content, drafting, cron, composio]
---

# LinkedIn content drafting (Celdel AI)

Turn source material — emails, links, notes, internal signals — into review-ready LinkedIn post drafts. The brand positioning and copy rules live in this profile's SOUL.md; THIS skill carries the workflow, the tool paths, and the pitfalls.

## When to Use

Load this skill when asked to write, prepare, draft, or schedule a LinkedIn post (for Celdel AI or this profile); when turning emails, notes, or links into LinkedIn content; or when setting up a recurring "source → post draft" automation. It also governs any request that touches publishing to LinkedIn — the draft-only gate always applies.

## Always-on rules

- **Drafts only.** Default status is « Brouillon à valider ». Never publish, schedule, or share a post without an explicit instruction naming that exact content AND its destination. Approval of an idea is not approval of the final text — always ask for a final read-through first.
- **Never claim** a draft was saved to LinkedIn or a post published unless you verified it in the connected tool.
- **Never invent** figures, client results, testimonials, or Celdel AI expertise that was not provided. Keep sources and facts-to-verify OUTSIDE the post text.
- Deliver, per draft: the post text, one hook variant, a visual suggestion, and the sources/facts to verify.
- Natural, credible French — no generic ad tone, no artificial hooks, no jargon, no emoji/hashtag spam.

## Workflow

1. **Reconnaissance before promising.** For any "is this feasible / set it up" request, verify EACH component against the live environment first (can you read the source? produce the output? where does the result land?). Report per-component status, never a blanket yes.
2. **Source the material.** For email sources read via the configured connection (see `references/composio-cli.md`). Confirm access with metadata (counts / ids) before pulling bodies; ask before reading message content the task does not require.
3. **Filter.** Apply the trigger (keyword / label). Drop obvious false positives explicitly; list anything ambiguous as "à examiner" rather than drafting it.
4. **Draft** per the always-on rules.
5. **Save & report.** Write each draft to a dated file; end with a recap — items analysed, drafts created (with file paths), items skipped and why — and restate that everything is "Brouillon à valider".

## Publishing reality (important)

- **The LinkedIn API has no draft endpoint.** You cannot "save a draft inside LinkedIn". Deliver the post as a copy-paste block / file for the user to publish.
- If a LinkedIn integration is connected, its create-post action PUBLISHES immediately — never call it while in draft mode, and only after the user explicitly confirms that exact post and destination.

## Images

- **Verify a generator is actually configured before promising an AI image.** The image toolset can be enabled yet gated off when no provider key is set — and a configured provider can still be blocked by the account's billing (402/429), so run one real test generation before promising an image.
- Reliable fallback needing no provider: a branded "card" visual (title + key quote) rendered **directly with Pillow** at 1200×627. Do NOT route it through HTML → browser screenshot (the bundled Chromium may fail to launch), and assume no system TTF fonts — `ImageFont.load_default(size=N)` gives a scalable font with no font file. Offer both paths and let the user choose.

## Scheduling a recurring source→draft job

- Use the cron tool with a **self-contained prompt**: cron runs start with no chat context and cannot ask questions.
- Set **continuity=true** and keep a processed-IDs log file in the workspace, so the same source item is not re-drafted every run.
- **Delivery caveat:** a cron job's output is only pushed somewhere if the profile has a messaging platform configured. Check first; if none, use deliver='local', have the job ALSO write a recap file to disk, and tell the user exactly where.
- The prompt must explicitly forbid publishing.

## Pitfalls

- **Generic keyword triggers flood you with false positives.** A common word in the source language (e.g. French "poste" also means a job posting) matches unrelated mail. Prefer a dedicated label or a distinctive marker over an everyday word.
- **Don't over-read a mailbox.** Metadata first; bodies only for the items the task needs.
- **Don't settle silently for a broken path.** If the obvious access method fails (e.g. stale credentials), look for an already-configured integration before telling the user it is impossible.

## References

- `references/composio-cli.md` — discover connected accounts and read Gmail / inspect tools via the Composio CLI.
