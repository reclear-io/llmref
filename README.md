# fullcontext

Public versioned documentation registry for [llm-txts](https://github.com/reclear-io/llm-txts).

Each indexed project version stores three artifacts here:

| File | Description |
|---|---|
| `llms.txt` | Compact routing and summary file for models |
| `llms-full.txt` | Full merged documentation artifact |
| `meta.json` | Snapshot metadata, timestamps, content fingerprints |

Large dump artifacts (chunks, embeddings) are stored in R2 — see `meta.json` for URLs.

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

Artifacts are served via the llm-txts API:

```
GET /v1/projects/:slug/:version/llms.txt
GET /v1/projects/:slug/:version/llms-full.txt
GET /v1/projects/:slug/:version/meta.json
```

Or fetched directly from this repo via raw GitHub URLs.

## License

MIT
