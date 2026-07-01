# llm-txts

A free, public, **versioned** documentation registry and retrieval API for AI tools, coding assistants, and retrieval systems. Built on the [`llms.txt`](https://llmstxt.org) convention.

There are two ways to consume it:

1. **Hosted API** — deterministic artifacts, semantic search, and an MCP endpoint at `https://llm-txts.reclear.io`.
2. **Raw registry files** — read the artifacts straight from this repo (small, diffable, auditable).

Each indexed project version produces three artifacts:

| File | Description |
|---|---|
| `llms.txt` | Compact routing and summary file for models |
| `llms-full.txt` | Full merged documentation artifact |
| `meta.json` | Snapshot metadata, timestamps, and content fingerprints |

Large dump artifacts (chunks, embeddings) are stored separately — see a snapshot's `dumps` endpoint or `meta.json` for their URLs.

---

## Hosted API

Base URL: **`https://llm-txts.reclear.io`**

Free by default. Anonymous access has conservative rate limits; API keys (sent as `Authorization: Bearer <key>`) raise them. The underlying data stays free.

### Deterministic routes

```
GET /v1/projects
GET /v1/projects/:slug
GET /v1/projects/:slug/:version/llms.txt
GET /v1/projects/:slug/:version/llms-full.txt
GET /v1/projects/:slug/:version/meta.json
GET /v1/projects/:slug/:version/dumps
GET /v1/resolve?project=<slug>&version=<version|latest>
```

**List projects**

```bash
curl https://llm-txts.reclear.io/v1/projects
```
```json
{
  "projects": [
    { "slug": "svelte", "versions": ["5.0.0"] },
    { "slug": "vite", "versions": ["8.0.16"] }
  ]
}
```

**Resolve a version** (accepts `latest`) and get artifact URLs:

```bash
curl "https://llm-txts.reclear.io/v1/resolve?project=svelte&version=latest"
```
```json
{
  "project": "svelte",
  "requested_version": "latest",
  "resolved_version": "5.0.0",
  "artifacts": {
    "llms.txt": "/v1/projects/svelte/5.0.0/llms.txt",
    "llms-full.txt": "/v1/projects/svelte/5.0.0/llms-full.txt",
    "meta.json": "/v1/projects/svelte/5.0.0/meta.json",
    "dumps": "/v1/projects/svelte/5.0.0/dumps"
  }
}
```

**Fetch an artifact** (`llms.txt` / `llms-full.txt` are `text/plain`):

```bash
curl https://llm-txts.reclear.io/v1/projects/svelte/5.0.0/llms.txt
```

**Snapshot metadata** (`meta.json`):

```json
{
  "project": "svelte",
  "project_version": "5.0.0",
  "snapshot_id": "7ddd5989-1888-4fcc-8908-e3bb8877eda7",
  "snapshot_at": "2026-06-12T07:52:39.572274+00:00",
  "source_last_seen_at": "2026-06-30T21:17:09.400213+00:00",
  "content_fingerprint": "7a2de2e589bd2c9b9b7008677d3d9d2be4f9cf9e18718e65c0cf56eea4c7140b",
  "page_count": 7,
  "source_root": "https://svelte.dev",
  "embedding_model": "voyage-3-lite",
  "chunking_profile": "docs-v1",
  "generator_version": "0.1.0"
}
```

**Dump URLs** (chunks / embeddings / manifest; `{}` when a snapshot has no published dumps):

```bash
curl https://llm-txts.reclear.io/v1/projects/svelte/5.0.0/dumps
```
```json
{ "dump_urls": { "chunks": "...", "embeddings": "...", "manifest": "..." } }
```

### Semantic search

```
POST /v1/search
POST /v1/search/semantic
```

Request body:

| Field | Type | Required | Description |
|---|---|---|---|
| `project` | string | yes | Project slug |
| `version` | string | yes | Concrete version (resolve `latest` first) |
| `query` | string | yes | Natural-language query |
| `top_k` | number | no | Max chunks to return |
| `token_budget` | number | no | Cap total returned tokens instead of count |

```bash
curl -X POST https://llm-txts.reclear.io/v1/search/semantic \
  -H 'Content-Type: application/json' \
  -d '{"project":"svelte","version":"5.0.0","query":"how do runes work","top_k":1}'
```
```json
{
  "chunks": [
    {
      "id": "00cdafc7cca227e4b1e4b05c92cee7a8",
      "project": "svelte",
      "version": "5.0.0",
      "page_url": "https://svelte.dev/docs/svelte/llms.txt",
      "heading": "What are runes?",
      "content": "# What are runes?\n\nRunes are symbols that you use in `.svelte` ...",
      "token_count": 215,
      "score": 0.5887165
    }
  ]
}
```

### MCP

A [Model Context Protocol](https://modelcontextprotocol.io) endpoint is exposed over **Streamable HTTP**:

```
https://llm-txts.reclear.io/v1/mcp
```

Add it to an MCP-capable client (Claude, Cursor, etc.):

```json
{
  "mcpServers": {
    "llm-txts": {
      "type": "http",
      "url": "https://llm-txts.reclear.io/v1/mcp"
    }
  }
}
```

Tools:

| Tool | Purpose |
|---|---|
| `list_projects` | List indexed projects and versions |
| `list_versions` | List versions for a project |
| `resolve_docs` | Resolve a version and return artifact URLs |
| `search_docs` | Semantic search over a project version |

---

## Raw registry access (no API)

Every artifact is also a plain file in this repo, fetchable over raw GitHub:

```
https://raw.githubusercontent.com/reclear-io/llm-txts/main/registry/<technology-id>/<version>/llms.txt
https://raw.githubusercontent.com/reclear-io/llm-txts/main/registry/<technology-id>/<version>/llms-full.txt
https://raw.githubusercontent.com/reclear-io/llm-txts/main/registry/<technology-id>/<version>/meta.json
```

List everything indexed:

```
https://raw.githubusercontent.com/reclear-io/llm-txts/main/registry/index.json
```

Example — Svelte 5.0.0:

```
https://raw.githubusercontent.com/reclear-io/llm-txts/main/registry/svelte/5.0.0/llms.txt
```

## Registry structure

```
registry/
  <technology-id>/
    <version>/
      llms.txt
      llms-full.txt
      meta.json
  index.json
```

See [SCHEMA.md](./SCHEMA.md) for naming rules, `meta.json` fields, and change detection.

## Contributing

- [CONTRIBUTING.md](./CONTRIBUTING.md) — PR title format, registry layout, submission guidelines
- [Request docs](https://github.com/reclear-io/llm-txts/issues/new?template=request-docs.yml) — ask maintainers to add or refresh a snapshot
- [Report registry issue](https://github.com/reclear-io/llm-txts/issues/new?template=report-registry-issue.yml) — flag incorrect or stale content

## Community

- [Code of Conduct](./CODE_OF_CONDUCT.md)
- [Security policy](./SECURITY.md)

## License

[MIT](./LICENSE)
