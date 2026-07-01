<div align="center">

# LLM Reference

**Versioned, model-ready documentation and semantic search for AI tools.**

Give your AI accurate, version-correct docs instead of stale training data.
Free, deterministic, and open - built on the [`llms.txt`](https://llmstxt.org) standard.

[**Docs**](https://llmref.org) · [**API**](https://api.llmref.org/v1/projects) · [**MCP registry**](https://registry.modelcontextprotocol.io/?q=llmref) · [**npm**](https://www.npmjs.com/package/@llmref/cli)

</div>

---

## Connect it to your AI tool

The quickest way to use LLM Reference is its **MCP server** - a remote endpoint that
gives assistants four tools: `list_projects`, `list_versions`, `resolve_docs`, and
`search_docs`.

```
https://api.llmref.org/v1/mcp
```

| Client | Setup |
| --- | --- |
| **Claude Code** | `claude mcp add --transport http llmref https://api.llmref.org/v1/mcp` |
| **Cursor** | [![Add to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](cursor://anysphere.cursor-deeplink/mcp/install?name=llmref&config=eyJ1cmwiOiJodHRwczovL2FwaS5sbG1yZWYub3JnL3YxL21jcCJ9) or add to `.cursor/mcp.json` |
| **Codex** | `~/.codex/config.toml`: `[mcp_servers.llmref]` then `url = "https://api.llmref.org/v1/mcp"` |
| **Claude Desktop / Windsurf / VS Code** | see the [MCP guide](https://llmref.org/guides/mcp/) |

For any JSON-configured client:

```json
{ "mcpServers": { "llmref": { "type": "http", "url": "https://api.llmref.org/v1/mcp" } } }
```

Full per-client setup lives at **[llmref.org/guides/mcp](https://llmref.org/guides/mcp/)**.

## Or use the API, SDK, or CLI

One free public API at `api.llmref.org` - no account required.

```sh
# List indexed projects
curl https://api.llmref.org/v1/projects

# Fetch a library's docs, version-pinned and model-ready
curl https://api.llmref.org/v1/projects/drizzle/0.45.2/llms.txt

# Semantic search
curl -X POST https://api.llmref.org/v1/search/semantic \
  -H 'content-type: application/json' \
  -d '{"project":"drizzle","version":"0.45.2","query":"define a table schema"}'
```

Typed clients:

```sh
bun add @llmref/sdk       # TypeScript SDK
bun add -g @llmref/cli    # the `llmref` command-line tool
```

Every route, method, and type is documented at **[llmref.org](https://llmref.org)**.

## What's indexed

Browse everything at [`/v1/projects`](https://api.llmref.org/v1/projects) or in
[`registry/index.json`](./registry/index.json).

**Missing a library?** [**Request it**](https://github.com/reclear-io/llmref/issues/new?template=request-docs.yml) -
you don't prepare anything; approved requests are ingested automatically into a
versioned, searchable snapshot.

## Request or fix documentation

Open an issue and the pipeline does the work - no setup on your end.

- 📥 [**Request docs**](https://github.com/reclear-io/llmref/issues/new?template=request-docs.yml) - add a new project or version.
- 🐛 [**Report a problem**](https://github.com/reclear-io/llmref/issues/new?template=report-registry-issue.yml) - flag incorrect or stale content.

Approved requests become a versioned snapshot pull request that a maintainer reviews
and merges before it goes live. Details: [Contribute guide](https://llmref.org/contribute/).

## The registry (raw files)

Every artifact is also a plain, diffable file you can read straight from GitHub - no
API required:

```
registry/<technology-id>/<version>/
  llms.txt        # compact routing/summary file for models
  llms-full.txt   # full merged documentation
  meta.json       # snapshot metadata + content fingerprint
registry/index.json
```

```
https://raw.githubusercontent.com/reclear-io/llmref/main/registry/drizzle/0.45.2/llms.txt
```

Large dump artifacts (chunks, embeddings) live off-repo; see a snapshot's `dumps`
endpoint. Format: [SCHEMA.md](./SCHEMA.md) · PR flow: [CONTRIBUTING.md](./CONTRIBUTING.md).

## Links

- **Documentation** - https://llmref.org
- **MCP registry** - [`org.llmref/llmref`](https://registry.modelcontextprotocol.io/?q=llmref)
- **npm** - [`@llmref/sdk`](https://www.npmjs.com/package/@llmref/sdk) · [`@llmref/cli`](https://www.npmjs.com/package/@llmref/cli)
- [Code of Conduct](./CODE_OF_CONDUCT.md) · [Security policy](./SECURITY.md)

## License

[MIT](./LICENSE) · Open Source by [Reclear.io](https://reclear.io)
