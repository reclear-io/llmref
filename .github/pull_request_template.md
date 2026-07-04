## Snapshot

**Technology ID:** <!-- e.g. svelte -->
**Version:** <!-- e.g. 5.0.0 -->
**Docs root:** <!-- e.g. https://svelte.dev -->

**Change type** (tick one):
- [ ] Addition — new project or version
- [ ] Update — refresh an existing snapshot

**Submission type** (tick one):
- [ ] Request — asking maintainers to index or refresh
- [ ] Contribution — I prepared the artifacts

## Summary

<!-- What changed and why -->


## Checklist

- [ ] registry/<technology-id>/<version>/ contains llms.txt and meta.json, plus llms-full.txt **only if** `meta.json` `license.redistribution_allowed` is `true` (Contributions only)
- [ ] `meta.json` includes a `license` block (`spdx`, `redistribution_allowed`) — see [SCHEMA.md](../SCHEMA.md#license)
- [ ] registry/index.json updated (Contributions only)
- [ ] python3 scripts/verify_registry.py passes locally (Contributions only, CI will also run this)
- [ ] Official public documentation only

**If Update:** `content_fingerprint` changed and the reason is explained above.

## Notes

<!-- Optional: related issue, upstream changelog -->
