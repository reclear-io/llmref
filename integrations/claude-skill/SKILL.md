---
name: llmref
description: >-
  Fetch accurate, VERSION-PINNED documentation for a library, framework, SDK,
  API, or CLI tool from the LLM Reference registry (llmref, api.llmref.org)
  instead of relying on training data. Use whenever the user asks about a
  library's API, configuration, setup, migration, version differences, or
  library-specific debugging — even well-known ones (React, Next.js, Prisma,
  Tailwind, Drizzle, Hono, Svelte, Zod, Bun, Vite). Especially use when the
  task targets a specific version, or when correctness for the exact version
  in the project matters. Triggers: "docs for X", "how do I do X in <library>",
  "X version <n>", "is this the right API for <library>@<version>", "look up
  <library> docs", "llmref".
---

# LLM Reference (llmref)

LLM Reference is a **versioned, reproducible** documentation registry. Unlike a
live "latest" doc index, every snapshot is pinned to an exact upstream version
and is byte-for-byte stable. Reach for it when the *version* matters — read the exact snapshot a project
depends on rather than an amalgam of whatever is current. Versions are semver for
package-sourced docs (e.g. `drizzle-orm@0.45.2`) and crawl dates for site-crawled
projects (e.g. Next.js at `2026.07.02`).

Base URL: `https://api.llmref.org/v1` — **no account or API key required.**

## When to use

- The user asks how to do something in a specific library/framework/SDK/CLI.
- The task pins a version (from `package.json`, a lockfile, or the user saying so).
- You're unsure your training data reflects the version in use.
- The user wants to search a library's docs semantically for a passage.

**Don't** use it for general programming concepts, refactoring, or business-logic
debugging — only for library-specific facts.

## Which surface to use (in priority order)

1. **MCP tools** — if this session has the `llmref` MCP server connected, its
   tools (`list_projects`, `list_versions`, `resolve_docs`, `search_docs`) are
   the cleanest path. Check your available tools first.
2. **`curl` against the public API** — the zero-setup default. Works anywhere
   with network access, no install. Use this when no MCP is connected.
3. **SDK / CLI** — when you're writing code that will call llmref at runtime,
   reach for `@llmref/sdk` (TypeScript) or `@llmref/cli` (shell). See
   `references/api-reference.md`.

## Core workflow

Always: **discover → resolve → read (or search)**. Never guess a slug or version.

1. **Discover** the project slug and its available versions.
2. **Resolve** the version you want (`latest`, or a concrete one) to a real
   snapshot. This confirms the version exists and gives you artifact URLs.
3. **Read** the compact `llms.txt` (routing/summary, drop straight into context)
   or `llms-full.txt` (complete merged docs), **or Search** semantically for
   just the relevant passages.

### With `curl` (default, zero-setup)

```sh
# 1. Discover — is the library indexed, and at what versions?
curl -s "https://api.llmref.org/v1/projects?query=next"

# 2. Resolve — turn "latest" (or a version query) into a concrete snapshot
curl -s "https://api.llmref.org/v1/resolve?project=nextjs&version=latest"

# 3a. Read the compact, model-ready docs. `latest` resolves server-side; pin the
#     resolved_version from step 2 when you need reproducibility.
curl -s "https://api.llmref.org/v1/projects/nextjs/latest/llms.txt"

# 3b. Or the full merged docs (large; license-gated — see gotchas)
curl -s "https://api.llmref.org/v1/projects/nextjs/latest/llms-full.txt"

# 3c. Or search semantically for just the relevant passages
curl -s -X POST "https://api.llmref.org/v1/search/semantic" \
  -H "Content-Type: application/json" \
  -d '{"project":"nextjs","version":"latest","query":"configure caching","top_k":5,"token_budget":2000}'
```

### With the MCP tools (if connected)

Call `list_projects` → `list_versions` → then `resolve_docs` or `search_docs`.
The server's own instructions enforce that ordering, so just start with
`list_projects`. Note the MCP `resolve_docs` result uses underscore keys
(`llms_txt`, `llms_full_txt`) where the HTTP `/resolve` uses filenames
(`llms.txt`) — the URLs are identical.

## Version pinning (the whole point)

Pin to a concrete version so results stay reproducible — but how you get that
version depends on the project:

- **Package-sourced docs** (npm/PyPI/crates) are versioned by **semver**. If the
  project is in the user's lockfile or `package.json`, request that release.
- **Site-crawled docs** (pulled from a project's website, like Next.js) are
  versioned by **crawl date** (e.g. `2026.07.02`), not semver — a lockfile semver
  won't match. For these, resolve `latest`, record the `resolved_version`, and
  reuse that concrete value.

Either way, never hardcode a version you didn't get from `list_versions` or
`/resolve` — guessing one 404s. To notice a snapshot changed underneath you,
compare the `content_fingerprint` in `meta.json`. (Semver-*range* resolution —
asking for `15.1` and getting the matching snapshot — is planned, not yet live.)

## Gotchas

- **License gate (`451`)**: `llms-full.txt` and dumps are served only when the
  upstream license permits redistribution. A `451` is expected, not an error —
  fall back to `llms.txt` (always available) or the source URL in the response.
  The compact `llms.txt` and search are never fully gated.
- **Empty search (`{"chunks": []}`)**: the endpoint you hit has semantic search
  disabled — this is not an error. Fall back to reading `llms.txt`. The
  deterministic list/resolve/read paths always work.
- **Not indexed?** If `/projects` doesn't list the library, it isn't in the
  registry yet. Say so and fall back to your normal doc sources — don't invent a
  slug or version. (Users can request it via the registry's issue template.)
- **Rate limits**: anonymous is 60 req/min per IP. Batch your calls; prefer one
  `search` or one `llms.txt` read over many small requests. A `429` means slow
  down. An API key raises the limit to 600/min but is never required for data.
- **`token_budget`** is available on the HTTP API and MCP `search_docs`, but not
  the CLI's `search`. Use curl/SDK/MCP when you need to cap context size.

Full route/parameter/type reference: **`references/api-reference.md`**.
