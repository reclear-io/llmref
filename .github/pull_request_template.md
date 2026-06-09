## Registry change

| Field | Value |
|---|---|
| **Technology ID** | `<!-- e.g. svelte -->` |
| **Version** | `<!-- e.g. 5.0.0 -->` |
| **Docs root** | `<!-- e.g. https://svelte.dev -->` |
| **Snapshot timestamp** | `<!-- ISO 8601 from meta.json, e.g. 2026-06-09T22:39:18Z -->` |
| **Change type** | <!-- check one --> [ ] Addition · [ ] Update |
| **Submission type** | <!-- check one --> [ ] Request · [ ] Contribution |

## Summary

<!-- 1–3 bullets: what changed and why -->

-

## Checklists

### Snapshot metadata

- [ ] `registry/<technology-id>/<version>/meta.json` is present
- [ ] `meta.json` `project` matches **Technology ID**
- [ ] `meta.json` `project_version` matches **Version**
- [ ] `meta.json` `source_root` matches **Docs root**
- [ ] `meta.json` `snapshot_at` matches **Snapshot timestamp**
- [ ] `content_fingerprint` is set and reflects the published artifacts

### Artifacts

- [ ] `llms.txt` is present and non-empty
- [ ] `llms-full.txt` is present and non-empty
- [ ] Artifact content matches the stated docs root (native fetch or crawl)
- [ ] `registry/index.json` updated to include this project and version

### Change type

**Addition** (new project or new version):

- [ ] Path `registry/<technology-id>/<version>/` did not exist before this PR
- [ ] No prior version is unintentionally overwritten

**Update** (refresh of an existing snapshot):

- [ ] `content_fingerprint` changed from the previous snapshot
- [ ] PR describes what changed upstream (docs refresh, corrected source, etc.)
- [ ] Update is intentional, not a duplicate of an existing snapshot

### Submission type

**Request** (asking maintainers to index or refresh):

- [ ] Requester has linked the official docs root
- [ ] Requested technology ID and version are correct
- [ ] No proprietary or non-public documentation included

**Contribution** (submitter prepared the artifacts):

- [ ] Artifacts prepared per registry guidelines
- [ ] `generator_version` recorded in `meta.json`
- [ ] Upstream license/terms do not restrict redistribution of docs content

## Test plan

- [ ] Raw GitHub URLs for `llms.txt`, `llms-full.txt`, and `meta.json` resolve after merge
- [ ] `llms.txt` links and summaries match the stated docs root
- [ ] `llms-full.txt` content is complete and readable
- [ ] `meta.json` fields are consistent with the registry table above

## Notes

<!-- Optional: upstream changelog, fingerprint diff, related issue, dump URLs -->
