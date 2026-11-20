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

Use the [pull request template](.github/pull_request_template.md). Fill in technology ID, version, docs root, change type, and submission type. For contributions, run python3 scripts/verify_registry.py locally before requesting review — CI enforces the rest.

Prefer opening a [request docs issue](https://github.com/reclear-io/llmref/issues/new?template=request-docs.yml) if you are not submitting artifacts yourself. Use [report registry issue](https://github.com/reclear-io/llmref/issues/new?template=report-registry-issue.yml) for incorrect or stale content.

See [SCHEMA.md](./SCHEMA.md) for the full `meta.json` specification.

## Registry layout

Each snapshot lives at:

```
registry/
  <technology-id>/
    <version>/
      llms.txt        # always
      llms-full.txt   # only when the license permits redistribution
      meta.json       # always (includes a license block)
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
- Licensing is detected automatically and recorded in `meta.json` `license`. Docs
  whose license does not permit redistribution are still indexed for search, but
  ship without `llms-full.txt` (see [SCHEMA.md](./SCHEMA.md#license)).
- For updates, ensure `content_fingerprint` has changed from the prior snapshot.
- Do not overwrite an existing version unless the PR is an intentional refresh.

## Catalog index

When adding or updating a snapshot, update `registry/index.json` to reflect the current project and version list.

## Review

Maintainers verify metadata consistency, artifact completeness, and checklist items before merge.

One project ID belongs to one documentation source. A matching name or an older
misassigned version does not authorize attaching another library to that ID.
Use a distinct ID for unrelated projects (for example, `adk-elixir` and `adk`).
CI compares new captures with the source in the base catalog, while preserving
unchanged historical routes. Conflicting historical sources require explicit
maintainer review; a later capture does not establish ownership. Shared hosts such as
GitHub and RubyDoc retain their repository or package boundary.

For an intentional move to a new docs domain or a broader scope, a maintainer
must review the old and new official sources and apply `source-move-approved`.
That label is an explicit exception to the identity check, so inspect every
source change in the PR before applying it. Automation requires the
`verify-project-identity` check to pass before merging a registry update.
