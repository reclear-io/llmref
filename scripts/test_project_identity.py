import unittest

from verify_project_identity import check_project


def capture(source, version="2026.07.02", date="2026-07-02T22:04:41Z", fingerprint="a" * 64):
    return dict(source_root=source, version=version, snapshot_at=date, content_fingerprint=fingerprint)


class ProjectIdentityTests(unittest.TestCase):
    def setUp(self):
        self.elixir = capture("https://adk.hexdocs.pm", "0.0.1", "2026-07-02T20:51:28Z")
        self.google = capture("https://adk.dev")
        self.mixed = [self.elixir, self.google]

    def test_legacy_collision_cannot_authorize_new_capture(self):
        update = capture("https://adk.hexdocs.pm", "2026.10.22", "2026-10-22T00:00:00Z")
        self.assertTrue(check_project("adk", self.mixed, [update]))
        self.assertFalse(check_project("adk-elixir", [], [update]))

    def test_existing_wrong_version_cannot_be_refreshed(self):
        self.assertTrue(check_project("adk", self.mixed, [{**self.elixir, "content_fingerprint": "b" * 64}]))

    def test_unchanged_historical_route_can_receive_metadata_repairs(self):
        self.assertFalse(check_project("adk", self.mixed, [{**self.elixir, "license": {}}]))

    def test_google_refresh_remains_allowed(self):
        self.assertFalse(check_project("adk", self.mixed, [capture("https://adk.dev/agents", "2026.10.22")]))

    def test_shared_host_is_not_project_identity(self):
        for old, new in [("https://github.com/google/adk-java", "https://github.com/other/adk"), ("https://rubydoc.info/gems/paperclip", "https://rubydoc.info/gems/other")]:
            self.assertTrue(check_project("adk", [capture(old)], [capture(new, "2.0")]))

    def test_new_project_cannot_combine_unrelated_sources(self):
        self.assertTrue(check_project("adk", [], self.mixed, approved_move=True))

    def test_broader_scope_is_not_implicitly_approved(self):
        self.assertTrue(check_project("tutorial", [capture("https://example.org/tutorial")], [capture("https://example.org", "2.0")]))

    def test_reviewed_source_move(self):
        update = capture("https://new.example.org", "2.0")
        self.assertTrue(check_project("adk", [self.google], [update]))
        self.assertFalse(check_project("adk", [self.google], [update], approved_move=True))

    def test_ambiguous_dates_fail_closed(self):
        self.assertTrue(check_project("adk", [self.google, {**self.elixir, "snapshot_at": self.google["snapshot_at"]}], [capture("https://adk.dev", "2.0")]))

    def test_version_paths_are_normalized_below_project(self):
        self.assertFalse(check_project("sdk", [capture("https://docs.example.org/sdk/v1.0/api", "1.0")], [capture("https://docs.example.org/sdk/v2.0/api", "2.0")]))


if __name__ == "__main__":
    unittest.main()
