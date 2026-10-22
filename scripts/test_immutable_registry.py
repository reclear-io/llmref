"""Metadata-only snapshots retain the existing schema and licensing gates."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from verify_registry import validate_snapshot


class ImmutableRegistryTests(unittest.TestCase):
    def test_shared_storage_requires_a_complete_reference_without_a_corpus_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            meta = {"project":"example","project_version":"1.0.0","snapshot_id":"9fd6f0a1-f59c-459b-860a-5e9ce6389fad","snapshot_at":"2026-10-22T00:00:00Z","source_last_seen_at":"2026-10-22T00:00:00Z","content_fingerprint":hashlib.sha256(b"Full docs").hexdigest(),"page_count":1,"source_root":"https://docs.example.org","embedding_model":"local","chunking_profile":"docs-v2","generator_version":"test","license":{"spdx":"MIT","redistribution_allowed":True,"share_alike":False,"source":"declared"},"revision_id":"a"*64,"artifact_storage":"llmref-snapshot-v1"}
            (folder/"llms.txt").write_text("# Example\n\n- [Docs](https://docs.example.org/reference)\n")
            def valid():
                (folder/"meta.json").write_text(json.dumps(meta))
                return validate_snapshot("example","1.0.0",folder)[0]
            self.assertTrue(valid())
            (folder/"llms-full.txt").write_text("Full docs")
            self.assertFalse(valid())
            (folder/"llms-full.txt").unlink()
            meta["revision_id"] = "../outside"
            self.assertFalse(valid())
            meta["revision_id"] = "a"*64
            meta.pop("artifact_storage")
            self.assertFalse(valid())
            meta.pop("revision_id")
            self.assertFalse(valid())  # Legacy licensed publication still needs its text.


if __name__ == "__main__":
    unittest.main()
