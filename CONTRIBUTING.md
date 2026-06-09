# Contributing

Thank you for helping grow the registry. This repository holds versioned documentation snapshots — `llms.txt`, `llms-full.txt`, and `meta.json` — for open technologies.

## Ways to contribute

**Request** — Ask maintainers to add or refresh a snapshot. Open an issue or PR with the official docs root, technology ID, and version. You do not need to prepare artifacts yourself.

**Contribution** — Submit a PR with the artifacts already prepared under `registry/<technology-id>/<version>/`.

## Pull request title format

Use this pattern for every PR:

```
Add|Update [technology name] [version name] - [reason phrase]
```

- **Add** — new technology or new version in the registry
- **Update** — refresh of an existing snapshot
- **Reason phrase** — short explanation: initial snapshot, upstream docs refresh, corrected docs root, community request, etc.

Examples:

```
Add Svelte 5.0.0 - initial snapshot
Update Svelte 5.0.0 - upstream docs refresh
Add Vite 6.0.0 - community request
Update React 19.0.0 - corrected docs root
```

## Pull request body

Use the [pull request template](.github/pull_request_template.md). Fill in every field in the registry table:

| Field | Description |
|---|---|
| **Technology ID** | Registry slug, e.g. `svelte` |
| **Version** | Project version, e.g. `5.0.0` |
| **Docs root** | Official documentation URL, e.g. `https://svelte.dev` |
| **Snapshot timestamp** | ISO 8601 value from `meta.json` |
| **Change type** | Addition or Update |
| **Submission type** | Request or Contribution |

Complete all checklists before requesting review.

Prefer opening a [request docs issue](.github/ISSUE_TEMPLATE/request-docs.yml) if you are not submitting artifacts yourself. Use [report registry issue](.github/ISSUE_TEMPLATE/report-registry-issue.yml) for incorrect or stale content.

See [SCHEMA.md](./SCHEMA.md) for the full `meta.json` specification.

## Registry layout

Each snapshot lives at:

```
registry/
  <technology-id>/
    <version>/
      llms.txt
      llms-full.txt
      meta.json
```

### `meta.json` requirements

- `project` must match **Technology ID**
- `project_version` must match **Version**
- `source_root` must match **Docs root**
- `snapshot_at` must match **Snapshot timestamp**
- `content_fingerprint` must reflect the published artifact content

## Guidelines

- Use the official public documentation source only.
- Do not include proprietary or non-public documentation.
- Upstream license/terms must not restrict redistribution of docs content.
- For updates, ensure `content_fingerprint` has changed from the prior snapshot.
- Do not overwrite an existing version unless the PR is an intentional refresh.

## Catalog index

When adding or updating a snapshot, update `registry/index.json` to reflect the current project and version list.

## Review

Maintainers verify metadata consistency, artifact completeness, and checklist items before merge.
