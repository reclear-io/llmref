# fullcontext

A free, public versioned documentation registry for AI tools, coding assistants, and retrieval systems.

Each indexed project version produces three artifacts:

| File | Description |
|---|---|
| `llms.txt` | Compact routing and summary file for models |
| `llms-full.txt` | Full merged documentation artifact |
| `meta.json` | Snapshot metadata, timestamps, and content fingerprints |

Large dump artifacts (chunks, embeddings) are stored separately — see `meta.json` for their URLs.

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

## Usage

Fetch artifacts via raw GitHub URLs:

```
https://raw.githubusercontent.com/reclear-io/fullcontext/main/registry/<technology-id>/<version>/llms.txt
https://raw.githubusercontent.com/reclear-io/fullcontext/main/registry/<technology-id>/<version>/llms-full.txt
https://raw.githubusercontent.com/reclear-io/fullcontext/main/registry/<technology-id>/<version>/meta.json
```

List all indexed projects and versions:

```
https://raw.githubusercontent.com/reclear-io/fullcontext/main/registry/index.json
```

Example — Svelte 5.0.0:

```
https://raw.githubusercontent.com/reclear-io/fullcontext/main/registry/svelte/5.0.0/llms.txt
```

## Backend engine

This repository is the public registry data. The engine that produces it — the
crawler, normalization, embedding, and API server — will be open-sourced at some
point. We're deliberately not rushing that: we want the internals stable first,
and we'd rather not expose a moving target to vulnerabilities while we're still
iterating in sprints. The hosted API (`api.llmref.org`) and this registry are free
and public today regardless.

## Contributing

- [CONTRIBUTING.md](./CONTRIBUTING.md) — PR title format, registry layout, submission guidelines
- [Request docs](https://github.com/reclear-io/fullcontext/issues/new?template=request-docs.yml) — ask maintainers to add or refresh a snapshot
- [Report registry issue](https://github.com/reclear-io/fullcontext/issues/new?template=report-registry-issue.yml) — flag incorrect or stale content

## Community

- [Code of Conduct](./CODE_OF_CONDUCT.md)
- [Security policy](./SECURITY.md)

## License

[MIT](./LICENSE)
