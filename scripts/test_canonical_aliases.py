import copy
import unittest
from verify_project_identity import alias_catalog_errors, alias_transition_errors, check_project


def entry(source, version="1"):
    return {"version":version,"source_root":source,"snapshot_at":"2026-07-02T00:00:00Z","content_fingerprint":"a"*64}


def catalog():
    leaf=entry("https://adk.hexdocs.pm")
    alias={**leaf,"canonical_target":{"project":"adk-elixir","version":"1"},"legacy_default":True}
    return {"projects":[{"id":"adk","versions":[alias]},{"id":"adk-elixir","versions":[leaf]}]}


class CanonicalAliasTests(unittest.TestCase):
    def test_valid_alias_preserves_source_and_original(self):
        self.assertEqual(alias_catalog_errors(catalog()),[])

    def test_missing_or_changed_target_is_rejected(self):
        for field,value in [("source_root","https://other.example.org"),("content_fingerprint","b"*64)]:
            data=catalog();data["projects"][1]["versions"][0][field]=value
            self.assertTrue(alias_catalog_errors(data))
        data=catalog();data["projects"].pop()
        self.assertTrue(alias_catalog_errors(data))

    def test_chains_and_cycles_are_rejected(self):
        data=catalog()
        data["projects"][1]["versions"][0].update(canonical_target={"project":"adk","version":"1"},legacy_default=True)
        self.assertTrue(alias_catalog_errors(data))

    def test_missing_or_multiple_frozen_defaults_are_rejected(self):
        data=catalog();data["projects"][0]["versions"][0].pop("legacy_default")
        self.assertTrue(alias_catalog_errors(data))
        data=catalog();second=copy.deepcopy(data["projects"][0]["versions"][0]);second["version"]="2"
        data["projects"][0]["versions"].append(second)
        self.assertTrue(alias_catalog_errors(data))

    def test_target_changes_need_review_even_when_original_fields_are_unchanged(self):
        old=catalog();new=copy.deepcopy(old)
        new["projects"].append({"id":"adk-other","versions":[entry("https://adk.hexdocs.pm")]})
        new["projects"][0]["versions"][0]["canonical_target"]["project"]="adk-other"
        self.assertEqual(alias_catalog_errors(new),[])
        self.assertTrue(alias_transition_errors(old,new))
        self.assertEqual(alias_transition_errors(old,new,approved=True),[])

    def test_initial_migration_requires_review_but_unchanged_alias_maintenance_does_not(self):
        new=catalog();old=copy.deepcopy(new)
        old["projects"][0]["versions"][0].pop("canonical_target")
        old["projects"][0]["versions"][0].pop("legacy_default")
        self.assertTrue(alias_transition_errors(old,new))
        self.assertEqual(alias_transition_errors(new,new),[])

    def test_compatibility_names_cannot_acquire_new_captures(self):
        old=catalog()["projects"][0]["versions"]
        self.assertTrue(check_project("adk",old,[entry("https://adk.hexdocs.pm","2")]))
        self.assertFalse(check_project("adk",old,[{**old[0],"archive_status":"unavailable","archive_reason":"Exact original unavailable"}]))

    def test_mixed_namespaces_missing_fingerprints_and_unsafe_targets_are_rejected(self):
        data=catalog();data["projects"][0]["versions"].append(entry("https://adk.dev","2"))
        self.assertTrue(alias_catalog_errors(data))
        data=catalog()
        for project in data["projects"]:project["versions"][0].pop("content_fingerprint")
        self.assertTrue(alias_catalog_errors(data))
        data=catalog();data["projects"][0]["versions"][0]["canonical_target"]["version"]="../escape"
        self.assertTrue(alias_catalog_errors(data))

    def test_docs_rs_crate_identity_is_stable_and_tenant_scoped(self):
        from verify_project_identity import source_scope
        self.assertEqual(source_scope("https://docs.rs/crate/permutation/0.4.1/source","0.4.1"),source_scope("https://docs.rs/permutation","2026.10.26"))
        self.assertNotEqual(source_scope("https://docs.rs/other","1"),source_scope("https://docs.rs/permutation","1"))
        with self.assertRaises(ValueError):source_scope("https://docs.rs","1")

    def test_retired_capture_cannot_authorize_new_capture(self):
        old={**entry("https://blog.example.org"),"capture_status":"misqualified","capture_reason":"Wrong corpus"}
        self.assertFalse(check_project("demo",[old],[{**old,"capture_reason":"Clarified reason"}]))
        self.assertTrue(check_project("demo",[old],[entry("https://blog.example.org","2")]))

    def test_capture_annotation_validation_and_index_parity(self):
        import contextlib,io,tempfile
        from pathlib import Path
        import verify_registry as verifier
        baseline={"project":"demo","project_version":"1","snapshot_id":"00000000-0000-4000-8000-000000000000","snapshot_at":"2026-07-02T00:00:00Z","source_last_seen_at":"2026-07-02T00:00:00Z","content_fingerprint":"a"*64,"page_count":1,"source_root":"https://docs.example.org","embedding_model":"local","chunking_profile":"docs-v2","generator_version":"test"}
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertFalse(verifier.validate_meta({**baseline,"capture_status":"misqualified"},"demo","1",Path("demo/1"),"",False,"# Docs\\n- [Intro](https://docs.example.org/intro)"))
            self.assertTrue(verifier.validate_meta({**baseline,"capture_status":"misqualified","capture_reason":"Wrong scope","replacement_project":"official-demo"},"demo","1",Path("demo/1"),"",False,"# Docs\\n- [Intro](https://docs.example.org/intro)"))

if __name__=="__main__":
    unittest.main()
