---
name: linkedin-post-drafting
description: "Use when drafting LinkedIn posts for Celdel AI."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [linkedin, content, drafting, celdel, email]
    related_skills: []
---

# LinkedIn post drafting (Celdel AI)

Prepare LinkedIn publications as ready-to-review drafts. The user posts himself; automation never publishes.

## When to Use

- The user asks for a LinkedIn post, draft, or publication for Celdel AI.
- An idea, note, link, or email must be turned into a publication.
- The weekly source-email review runs (mails from `<adresse-de-l-expediteur@exemple.com>` to `<boite-de-reception@exemple.com>`).
- Anything touching the LinkedIn integration, the draft folder, or the visual for a publication.

## Hard rules (apply to every instance)

- Status is always « Brouillon à valider ». Approving an idea is NOT approving the final text.
- **Never publish, schedule, or share** a post without an explicit instruction that names this exact content and its destination. Before publishing, have the final text re-read and confirmed.
- Never invent facts, figures, client results, testimonials, or Celdel AI expertise that was not supplied.
- When a draft relies on an external source, keep the link and attribute the facts; do not copy long passages.
- Language: French, natural and credible. No generic ad tone, no artificial hooks, no jargon, no excessive emojis/hashtags.
- Deliverable shape per post: the post text, a hook variant, a visual suggestion, and the sources / facts to verify — the last three kept OUTSIDE the post text.

## Workflow

1. **Identify** the objective, audience, point of view, and desired call to action. Missing but non-blocking → state a short assumption; if it would change the message, ask.
2. **Get the source material.** Two entry points:
   - User-supplied notes / links / idea (in chat).
   - The weekly email source: mails sent by `<adresse-de-l-expediteur@exemple.com>` to `<boite-de-reception@exemple.com>`. Read them via the Composio CLI — commands and the email structure are in `references/composio-gmail-linkedin.md`.
3. **Extract the post text.** In the `[Validation]` emails the publisher's text sits under a `Post :` heading; the `article` and `Sources` list are separate sections. Take the `Post :` section as the publication text.
4. **Draft** to the deliverable shape above.
5. **Visual.** Prefer a free path when no paid provider works: run `scripts/generer_visuel.py` (Pollinations, no key). The option table, the endpoint variants and the throttling behaviour are in `references/image-generation.md`. Generate via a configured provider ONLY if a real test generation succeeds — a configured provider can still be refused by the account's billing (402/429). Otherwise describe the visual precisely, or render a designed title/quote card locally with Pillow (recipe in `references/composio-gmail-linkedin.md`). Never propose Gemini for images: Hermes ships no Gemini image connector and Gemini's image API has no free tier.
6. **Save** the draft to `<HERMES_HOME>/workspace/brouillons-linkedin/AAAA-MM-JJ/` (one markdown file per post + a `_recap.md`). Update `_traites.json` with processed `messageId`s for dedupe.
7. **Stop.** Present the draft and ask for validation. Do not touch LinkedIn.

## Pitfalls

- **LinkedIn has no API draft concept.** The API only publishes; real drafts exist only in LinkedIn's web composer. "Mettre en brouillon" therefore means a local file the user copies from — never promise a saved LinkedIn draft.
- **Verify whose account is connected before any publish.** The connected LinkedIn identity may be the user's personal profile, not the Celdel company page. Resolve the author identity first and flag it.
- **Profiles are isolated.** An API key set on the default profile is NOT visible in the `linkedin` profile — set the key on the target profile explicitly.
- **Cron `deliver` falls back to `local`** when the profile has no messaging platform configured: output is saved, not pushed. Say so and offer to wire a channel; never claim a notification was sent.
- **Keyword traps:** "poste" is a false-positive magnet in French (it means a job). Prefer the structural signal (the `Post :` section / the `[Validation]` subject) over a bare keyword.
- **Large Composio outputs are offloaded:** if the CLI returns `storedInFile` / `outputFilePath`, parse THAT JSON file, not the truncated stdout.
- **Reproduce the "verify before publish" step with `--dry-run`.** To show the publish mechanics WITHOUT publishing, run the create-post tool with `--dry-run` (returns `dryRun: true`, validates the payload, posts nothing). Only a real call publishes — and it posts as WHOSEVER account is connected, so resolve the identity first.
- **Never hand-edit `config.yaml`** — use `hermes config set` (secret keys route to the profile `.env`).
- **Don't propose Gemini for image generation.** Hermes has no Gemini/Google image-gen connector and Gemini's free image tier is app-only (the current image API models are not free). For a free route use Pollinations (no key, no account) or Cloudflare Workers AI (free daily allocation) — see `references/image-generation.md`.
- **A 402 from Pollinations is throttling, not a dead service.** Anonymous use allows roughly one request every 15 s; vary the endpoint/model variant and retry after ~60 s instead of reporting image generation as unavailable.

## References

- `references/composio-gmail-linkedin.md` — Composio CLI commands for reading the source mailbox and the LinkedIn tool set, the `[Validation]` email structure, and how to enable an image provider.
- `references/image-generation.md` — which image providers Hermes can drive, the free-vs-paid option table, and the Pollinations recipe (variants, watermark, throttling, re-crop).
- `scripts/generer_visuel.py` — free keyless image generation via Pollinations, with variant fallback and re-crop to the target size.
