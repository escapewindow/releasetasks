import unittest

from releasetasks.test.firefox import make_task_graph, do_common_assertions, \
    get_task_by_name
from releasetasks.test import PVT_KEY_FILE


class TestBouncerAliases(unittest.TestCase):
    maxDiff = 30000
    graph = None
    task = None
    human_task = None
    payload = None

    def setUp(self):
        self.graph = make_task_graph(
            version="42.0b2",
            next_version="42.0b3",
            appVersion="42.0",
            buildNumber=3,
            source_enabled=False,
            checksums_enabled=False,
            en_US_config={
                "platforms": {
                    "macosx64": {},
                    "win32": {},
                    "win64": {},
                    "linux": {},
                    "linux64": {},
                }
            },
            l10n_config={},
            repo_path="releases/foo",
            product="firefox",
            revision="fedcba654321",
            mozharness_changeset="abcd",
            partial_updates={
                "38.0": {
                    "buildNumber": 1,
                    "locales": ["de", "en-GB", "zh-TW"],
                },
                "37.0": {
                    "buildNumber": 2,
                    "locales": ["de", "en-GB", "zh-TW"],
                },
            },
            branch="foo",
            updates_enabled=False,
            bouncer_enabled=False,
            push_to_candidates_enabled=False,
            push_to_releases_enabled=False,
            uptake_monitoring_enabled=False,
            postrelease_version_bump_enabled=False,
            postrelease_mark_as_shipped_enabled=False,
            postrelease_bouncer_aliases_enabled=True,
            tuxedo_server_url="https://bouncer.real.allizom.org/api",
            signing_class="release-signing",
            release_channels=["foo"],
            balrog_api_root="https://balrog.real/api",
            funsize_balrog_api_root="http://balrog/api",
            signing_pvt_key=PVT_KEY_FILE,
            build_tools_repo_path='build/tools',
            publish_to_balrog_channels=None,
        )
        self.task = get_task_by_name(
            self.graph, "release-foo-firefox_bouncer_aliases")
        self.human_task = get_task_by_name(
            self.graph, "publish_release_human_decision")
        self.payload = self.task["task"]["payload"]

    def test_common_assertions(self):
        do_common_assertions(self.graph)

    def test_provisioner(self):
        self.assertEqual(self.task["task"]["provisionerId"],
                         "buildbot-bridge")

    def test_human_provisioner(self):
        self.assertEqual(self.human_task["task"]["provisionerId"],
                         "null-provisioner")

    def test_human_worker_type(self):
        self.assertEqual(self.human_task["task"]["workerType"],
                         "human-decision")

    def test_worker_type(self):
        self.assertEqual(self.task["task"]["workerType"], "buildbot-bridge")

    def test_graph_scopes(self):
        expected_graph_scopes = set([
            "queue:task-priority:high",
        ])
        self.assertTrue(expected_graph_scopes.issubset(self.graph["scopes"]))

    def test_requires(self):
        self.assertIn(self.human_task["taskId"], self.task["requires"])

    def test_product(self):
        self.assertEqual(self.payload["properties"]["product"],
                         "firefox")

    def test_version(self):
        self.assertEqual(self.payload["properties"]["version"],
                         "42.0b2")

    def test_build_number(self):
        self.assertEqual(self.payload["properties"]["build_number"], 3)

    def test_repo_path(self):
        self.assertEqual(self.payload["properties"]["repo_path"],
                         "releases/foo")

    def test_script_repo_revision(self):
        self.assertEqual(self.payload["properties"]["script_repo_revision"],
                         "abcd")

    def test_revision(self):
        self.assertEqual(self.payload["properties"]["revision"],
                         "fedcba654321")

    def test_tuxedo_server_url(self):
        self.assertEqual(self.payload["properties"]["tuxedo_server_url"],
                         "https://bouncer.real.allizom.org/api")
