# Generating the post visual (Celdel AI `linkedin` profile)

Goal: attach a visual to each drafted post. Never promise an image before a real test
generation returned a file, "toolset enabled" and "provider configured" are both
weaker signals than one successful run.

## What Hermes can actually drive

Hermes ships image-gen providers for: `fal`, `openai`, `openai-codex`, `openrouter`,
`xai`, `deepinfra`, `krea`, `meta-ai`. **There is no Gemini/Google image-gen connector**, 
a Gemini/`GOOGLE_API_KEY` cannot be plugged into the image tool. Gemini's free image
generation is *app-only* (gemini.google.com) and the current Gemini image **API** models
are not on a free tier, so Gemini is never the free route here. Check the installed
provider dirs (`plugins/image_gen/`) rather than assuming a provider exists.

## Free / low-cost options

| Option | Cost | Access | Caveats |
|---|---|---|---|
| Pollinations.ai | free, **no key, no account** | plain HTTP GET | watermark in anonymous mode; ~1 request / 15 s |
| Pollinations + free key | free (signup, no card) | same URL + `Authorization: Bearer <key>` | removes the watermark |
| Cloudflare Workers AI | free daily allocation (10 000 neurons/day) | `@cf/black-forest-labs/flux-1-schnell`, needs a free account id + API token | no card required |
| openai / openrouter / fal | paid | already-wired providers | blocked until the account is funded (402/429) |

When a paid provider is configured but the account has no credit, offer the free paths
instead of reporting image generation as impossible.

## Pollinations recipe

The endpoint shape decides whether the request passes free or returns **402 Payment
Required**. Try these variants in order and stop at the first that returns image bytes:

```
https://image.pollinations.ai/prompt/{urlencoded-prompt}?width=1200&height=627&model=flux&nologo=true
https://image.pollinations.ai/prompt/{p}?width=1200&height=627&model=turbo&nologo=true
https://image.pollinations.ai/prompt/{p}?width=1200&height=627&model=turbo
https://image.pollinations.ai/prompt/{p}?width=1200&height=627
```

- A 402 here is **throttling, not a dead service** (anonymous tier ≈ 1 request/15 s).
  Vary the variant and retry after ~60 s before concluding anything.
- `nologo=true` only actually drops the watermark when an API key is sent; anonymous
  requests keep it. Say so, and offer the free signup that removes it.
- The response is **JPEG** (even when written to a `.png` name). Re-encode with Pillow:
  resize-cover then centre-crop to the exact target size so the file matches the
  LinkedIn format (1200×627 landscape, 1080×1350 portrait).
- Use the `image.pollinations.ai/prompt/` host for keyless use. The `gen.pollinations.ai`
  host answers **401** without a key.
- `scripts/generer_visuel.py` implements the variant fallback, the Pillow re-crop, and
  reads `POLLINATIONS_API_KEY` from the environment when present, run it instead of
  hand-writing curl calls.

## No-network / no-provider fallback

Render a designed title-or-quote card directly with Pillow (recipe in
`references/composio-gmail-linkedin.md`). Always ask for the brand colours before calling
any visual on-brand, and if the source email already carries a photo attachment, flag it
rather than silently replacing it.
