# Composio: source mailbox + LinkedIn (profil `linkedin`, Celdel AI)

## Reading the source mailbox

The Composio CLI is a self-contained binary — no agent loop needed:

```bash
COMPOSIO=/root/.composio/composio
$COMPOSIO connections list                         # which toolkits/accounts are ACTIVE
$COMPOSIO search "<use case>" --toolkits gmail --limit 10   # find tool slugs + a recommended plan
$COMPOSIO execute GMAIL_FETCH_EMAILS --account <gmail_account> \
  -d '{"query":"from:<sender> newer_than:8d","verbose":true}'
```

- `-d` takes JSON or a JS-style object literal; `{}` is fine for schema-only tools.
- `--get-schema` prints a tool's input schema; `--dry-run` validates before executing.
- Paginate with `page_token` until `nextPageToken` is empty.
- Watch for `storedInFile: true` + `outputFilePath`: large replies are written to a JSON file — read that file. Inside, `data.messages[0]` holds `subject` / `sender` / `messageText` / `payload`.
- The body is base64 in `payload.parts[...].body.data`; the `messageText` field is a convenient decoded shortcut.

This Composio account is the working path for the mailbox; do not depend on the profile's raw `EMAIL_*` IMAP vars.

## The `[Validation]` source email

Received at `clement@celdel.com`, sent by `clement.t.zurcher@gmail.com` — usually a forward of a message from the publisher (`celine@celdel.com`). Body structure:

```
Subject: Fwd: [Validation] <title>

Article et post linkedin en dessous et photo ci-joint : ...

article
<article text>

------------------------------
Sources
 1. <source> <url>
 ...

Post :
<the LinkedIn post text>
```

Extract the `Post :` section as the publication text; keep `Sources` for the "facts to verify" list; note any photo attachment filename (the mails often carry an image already).

## LinkedIn tool set (Composio)

- `LINKEDIN_CREATE_LINKED_IN_POST` — publishes (needs `author` URN + `commentary`, optional `images`). No draft state.
  - **Validation gate:** prove the mechanics without publishing by adding `--dry-run` (`execute LINKEDIN_CREATE_LINKED_IN_POST --dry-run -d '{...}'` → `dryRun: true`). Only a real call publishes, as whichever account is connected.
- `LINKEDIN_GET_MY_INFO` — the connected identity; resolve `urn:li:person:<id>` from it. Use it to confirm WHOSE profile will publish.
- `LINKEDIN_GET_COMPANY_INFO` — organization URNs (needs admin scope).
- `LINKEDIN_REGISTER_IMAGE_UPLOAD`, `LINKEDIN_GET_POST_CONTENT`, `LINKEDIN_DELETE_POST`, `LINKEDIN_CREATE_ARTICLE_OR_URL_SHARE`.

## Enabling an image generator for the profile

The `image_gen` toolset is enabled but the tool stays unavailable until a provider key is set on the target profile. Providers and their keys:

| provider | env var |
|---|---|
| openrouter | `OPENROUTER_API_KEY` (default model `google/gemini-3-pro-image`) |
| fal | `FAL_KEY` |
| openai / openai-codex | `OPENAI_API_KEY` |
| xai | `XAI_API_KEY` |
| deepinfra | `DEEPINFRA_API_KEY` |
| krea | `KREA_API_KEY` |

```bash
hermes -p <profile> config set image_gen.provider openrouter
hermes -p <profile> config set OPENROUTER_API_KEY <clé>   # routes to the profile .env
hermes -p <profile> config get image_gen.provider
```

Give the user these commands — never type a key on their behalf.

- **A configured provider can still be blocked by the account's billing** (HTTP 402 from OpenRouter, 429 from OpenAI "no credits remaining"). Run one real test generation before promising an image; if it fails, use the local fallback.

## Local visual fallback (no provider, no credits)

Render the title/quote card **directly with Pillow**. Do NOT route it through HTML → browser screenshot: the bundled Chromium can fail to launch (missing system libs), and there may be no system TTF fonts installed.

```python
from PIL import Image, ImageDraw, ImageFont
img = Image.new("RGB", (1200, 627), (28, 27, 25))   # 1200x627 landscape / 1080x1350 portrait
d = ImageDraw.Draw(img)
f = ImageFont.load_default(size=78)                   # Pillow >=10.1: scalable, needs NO font file
d.textlength(line, font=f)                            # measure to auto-fit the width
```

Use ImageFont.load_default(size=N) when no TTF is available; keep it to one accent colour on a dark or light ground. Ask for the brand colours before calling it on-brand.
