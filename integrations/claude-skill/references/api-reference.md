# llmref API reference

Complete surface for the LLM Reference registry. Base URL: `https://api.llmref.org/v1`.
Auth is optional (an `Authorization: Bearer <key>` header only raises rate limits).

## HTTP API

### Deterministic routes (immutable per snapshot, cacheable)

| Method & path | Purpose | Key params |
|---|---|---|
| `GET /projects` | List indexed projects + versions | `query` (fuzzy slug filter), `limit` (≤200, default 50), `skip` |
| `GET /projects/:slug` | One project's versions | — (`404` if unknown) |
| `GET /resolve` | Resolve a version query → concrete version + artifact URLs | `project` (req), `version` (default `latest`) |
| `GET /projects/:slug/:version/llms.txt` | Compact routing/summary file (`text/plain`) | — always available |
| `GET /projects/:slug/:version/llms-full.txt` | Full merged docs (`text/plain`) | **license-gated → `451`** |
| `GET /projects/:slug/:version/meta.json` | Snapshot metadata (`SnapshotMeta`) | — |
| `GET /projects/:slug/:version/dumps` | Object-storage URLs for raw dumps | **license-gated → `451`** |

`/resolve` response:

```json
{
  "project": "nextjs",
  "requested_version": "latest",
  "resolved_version": "15.1.0",
  "artifacts": {
    "llms.txt": "/v1/projects/nextjs/15.1.0/llms.txt",
    "llms-full.txt": "/v1/projects/nextjs/15.1.0/llms-full.txt",
    "meta.json": "/v1/projects/nextjs/15.1.0/meta.json",
    "dumps": "/v1/projects/nextjs/15.1.0/dumps"
  }
}
```

### Search routes

`POST /search` and `POST /search/semantic` — currently identical (both semantic;
the split reserves `/search` for a future keyword mode). Same body and response.

Body:

| Field | Type | Req | Default | Notes |
|---|---|---|---|---|
| `project` | string | yes | — | slug |
| `version` | string | yes | — | concrete version or `latest` |
| `query` | string | yes | — | natural-language query |
| `top_k` | int | no | 10 | 1–50 |
| `token_budget` | int | no | 4096 | caps combined tokens across returned chunks |

Response: `{ "chunks": [ { id, project, version, page_url, heading, content, token_count } ] }`.
Search disabled on the server → `{ "chunks": [] }` (not an error).

### Status codes

`200` ok · `401` invalid key · `404` unknown project/version/artifact ·
`429` rate limit · `451` full text withheld (license or takedown) ·
`500` registry read error · `503` auth requested but not configured.

### Caching & attribution headers

Snapshot responses carry `Cache-Control: public, max-age=31536000, immutable`,
`ETag` = the snapshot `content_fingerprint`, `X-Source-URL` (canonical root),
`X-License` (SPDX id), and `Link: <source_root>; rel="canonical"`.

### Rate limits

Per caller, per minute: anonymous **60** (per IP), valid API key **600** (per
key). Key goes in `Authorization: Bearer <key>` (or `x-api-key` alias).

## MCP server

Endpoint: `GET|POST https://api.llmref.org/v1/mcp` (streamable HTTP, protocol
`2024-11-05`, advertises as `llmref`). Four read-only tools; each returns
pretty-printed JSON as a text block.

| Tool | Params |
|---|---|
| `list_projects` | `query?`, `limit?` (≤200), `skip?` |
| `list_versions` | `project` (req) |
| `resolve_docs` | `project` (req), `version` (req; or `latest`) |
| `search_docs` | `project`, `version`, `query` (req); `top_k?`, `token_budget?` |

`resolve_docs` returns underscore artifact keys (`llms_txt`, `llms_full_txt`,
`meta_json`, `dumps`) — same URLs as the HTTP `/resolve` filenames.

### Connect it

Claude Code:

```sh
claude mcp add --transport http llmref https://api.llmref.org/v1/mcp
# with a key for higher limits:
claude mcp add --transport http llmref https://api.llmref.org/v1/mcp \
  --header "Authorization: Bearer your-key-here"
```

Claude Desktop / Cursor — add under `mcpServers`:

```json
{
  "mcpServers": {
    "llmref": { "type": "http", "url": "https://api.llmref.org/v1/mcp" }
  }
}
```

## CLI — `@llmref/cli`

```sh
bunx @llmref/cli <command>      # run without installing (or: npx @llmref/cli)
bun add -g @llmref/cli          # install the `llmref` command
```

Env: `LLMREF_BASE_URL` (default `https://api.llmref.org/v1`), `LLMREF_API_KEY`.

| Command | Purpose |
|---|---|
| `llmref list [-q <query>] [--limit <n>] [--skip <n>]` | List projects as `slug  (versions…)` |
| `llmref get <project> <version> [--full]` | Print `llms.txt` (or `llms-full.txt` with `--full`) to stdout |
| `llmref resolve <project> [version]` | Print resolved version + artifact URLs (default `latest`) |
| `llmref dumps <project> <version>` | Print dump URLs; exit 1 + message if none |
| `llmref search <project> <version> <query> [--top-k <n>]` | Print `page_url` + content per hit (default top-k 5) |

CLI `search` has no `token_budget` — use SDK/HTTP/MCP for that. Exit codes: `0`
success, `1` request failed / no dumps.

## SDK — `@llmref/sdk` (TypeScript, ESM, needs global `fetch`: Node 18+/Bun/Deno/browser)

```ts
import { LlmRefClient } from '@llmref/sdk';

const client = new LlmRefClient(); // or { baseUrl, apiKey, fetch }

// Resolve latest once, then pin to the concrete version for reproducibility
const { resolved_version } = await client.resolve('nextjs', 'latest');
const llmsTxt = await client.getLlmsTxt('nextjs', resolved_version);

const { chunks } = await client.search({
  project: 'nextjs',
  version: resolved_version,
  query: 'how do I configure caching',
  top_k: 5,
  token_budget: 2000,
});
```

Methods: `listProjects({query?,limit?,skip?})`, `getProject(slug)`,
`resolve(project, version='latest')`, `getLlmsTxt(slug, version)`,
`getLlmsFullTxt(slug, version)`, `getMeta(slug, version)`, `getDumps(slug, version)`,
`search(options)`. Non-2xx responses throw an `Error` (method, path, status, body
excerpt). Exported types: `LlmRefClientOptions`, `Project`, `SnapshotMeta`,
`DumpUrls`, `ResolveResult`, `Chunk`, `SearchResult`, `SearchOptions`.
