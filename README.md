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
  <project>/
    <version>/
      llms.txt
      llms-full.txt
      meta.json
```

## Usage

Fetch artifacts directly via raw GitHub URLs, or through the API:

```
GET /v1/projects/:slug/:version/llms.txt
GET /v1/projects/:slug/:version/llms-full.txt
GET /v1/projects/:slug/:version/meta.json
```

## License

MIT
