"""The worker downloads and imports only verify_registry.py at its pinned ref."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class SnapshotValidatorContractTests(unittest.TestCase):
    def test_single_file_import_keeps_snapshot_validation_and_immutable_publications(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / "registry-validator.py"
            shutil.copyfile(Path(__file__).with_name("verify_registry.py"), script)
            folder = root / "artifacts/registry/example/1.0.0"
            folder.mkdir(parents=True)
            full = b"Full docs\n"
            meta = {
                "project": "example",
                "project_version": "1.0.0",
                "snapshot_id": "9fd6f0a1-f59c-459b-860a-5e9ce6389fad",
                "snapshot_at": "2026-10-22T00:00:00Z",
                "source_last_seen_at": "2026-10-22T00:00:00Z",
                "content_fingerprint": hashlib.sha256(full).hexdigest(),
                "page_count": 1,
                "source_root": "https://docs.example.org",
                "embedding_model": "local",
                "chunking_profile": "docs-v2",
                "generator_version": "test",
                "license": {"spdx": "MIT", "redistribution_allowed": True, "share_alike": False, "source": "declared"},
            }
            (folder / "meta.json").write_text(json.dumps(meta))
            (folder / "llms.txt").write_text("# Docs\n\n- [Guide](https://docs.example.org/guide)\n")
            (folder / "llms-full.txt").write_bytes(full)
            child = '''import importlib.util,json,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location("llmref_scoped_validator",sys.argv[1])
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
folder=Path(sys.argv[2])
assert module.validate_snapshot("example","1.0.0",folder)[0]
meta=json.loads((folder/"meta.json").read_text())
original=meta["content_fingerprint"]
meta["content_fingerprint"]="b"*64
(folder/"meta.json").write_text(json.dumps(meta))
assert not module.validate_snapshot("example","1.0.0",folder)[0]
meta.update(content_fingerprint=original,revision_id="a"*64,artifact_storage="llmref-snapshot-v1")
(folder/"meta.json").write_text(json.dumps(meta))
(folder/"llms-full.txt").unlink()
assert module.validate_snapshot("example","1.0.0",folder)[0]
'''
            result = subprocess.run(
                [sys.executable, "-I", "-c", child, str(script), str(folder)],
                cwd=root, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
