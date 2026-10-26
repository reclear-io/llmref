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


if __name__=="__main__":
    unittest.main()
