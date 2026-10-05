# Composio CLI — reading sources, discovering accounts and tools

Use the Composio CLI from the terminal. It is installed at `~/.composio/composio` in this environment and is the configured read path for Gmail here.

## Discover what is connected

`composio connections list` prints each toolkit with its `word_id` (e.g. `gmail_exemple-aaaaa`) and status. Use only accounts whose status is `ACTIVE`; ignore `FAILED` ones.

## Read Gmail

```
composio execute GMAIL_FETCH_EMAILS --account <word_id> -d '{"query":"newer_than:7d","verbose":true}'
```

- `query` accepts Gmail search syntax: `newer_than:7d`, `from:`, `subject:`, `label:`, `is:unread`, ...
- `ids_only:true` returns message ids only (fast, no bodies) — use it for an access check / counting.
- `verbose:false` drops bodies; `verbose:true` is required for body + attachments.
- Paginate with the returned `page_token` until it is empty. `resultSizeEstimate` is approximate — trust `page_token`, not counts.

## Inspect a tool's input schema

`composio execute <SLUG> --get-schema` prints the full input/output schema (e.g. `GMAIL_FETCH_EMAILS`, `LINKEDIN_CREATE_LINKED_IN_POST`). Read it before building a payload.

## Discover tools for a use case

`composio search "<use case>" --toolkits <toolkit> --limit N` returns JSON with a recommended plan, known pitfalls, and related tool slugs. Prefer the default JSON output; the `--human` rendering can come back empty.

## Gotchas

- `execute` requires `-d` even for tools that take no arguments: pass `-d '{}'`. Omitting it fails with "Invalid JSON input".
- `--account` accepts an alias, the `word_id`, or the connected-account id.
- `proxy <url> --toolkit <tk>` reaches a toolkit's raw API through the connected account when no tool wraps the endpoint.

## Access notes

- If the obvious IMAP credentials fail, check `composio connections list` for an ACTIVE Gmail connection before concluding email is unreadable — an already-configured connection is the working path.
- LinkedIn: `LINKEDIN_CREATE_LINKED_IN_POST` publishes only (no draft state). Confirm with `--get-schema` before relying on it.
