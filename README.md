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

## Contributing

- [CONTRIBUTING.md](./CONTRIBUTING.md) — PR title format, registry layout, submission guidelines
- [Request docs](.github/ISSUE_TEMPLATE/request-docs.yml) — ask maintainers to add or refresh a snapshot
- [Report registry issue](.github/ISSUE_TEMPLATE/report-registry-issue.yml) — flag incorrect or stale content

## Community

- [Code of Conduct](./CODE_OF_CONDUCT.md)
- [Security policy](./SECURITY.md)

## License

[MIT](./LICENSE)
