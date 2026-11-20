"""Tests for tasks/namespace_guard.py. Run from the repo root with the CumulusCI interpreter:
    "<cci venv>/bin/python" -m unittest tasks.tests.test_namespace_guard
"""

import tempfile
import unittest
from pathlib import Path

from tasks.namespace_guard import field_names, find_violations

REPO = Path(__file__).resolve().parents[2]


def write_field(root, obj, api_name):
    path = Path(root) / "main/default/objects" / obj / "fields" / f"{api_name}.field-meta.xml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("<CustomField/>")


class CapturedSiteTest(unittest.TestCase):
    def test_captured_site_spells_every_unpackaged_field_with_the_token(self):
        # Fails if volunteerJobDetail.json goes back to FlowToolKit__ on unpackaged fields (issue 39)
        unpackaged = field_names(REPO / "force-app-unpackaged-objects")
        packaged = field_names(REPO / "force-app")
        self.assertIn("cUnite_Volunteer_Role__r", unpackaged)
        self.assertEqual(find_violations(REPO / "scratch-org/site", unpackaged, packaged), [])


class FindViolationsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        write_field(root / "unpackaged", "Volunteer_Role__c", "Minimum_Age__c")
        write_field(root / "unpackaged", "GW_Volunteers__Volunteer_Job__c", "cUnite_Volunteer_Role__c")
        write_field(root / "packaged", "GW_Volunteers__Volunteer_Job__c", "cUnite_Subtitle__c")
        self.unpackaged = field_names(root / "unpackaged")
        self.packaged = field_names(root / "packaged")
        self.site = root / "site"
        self.site.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, token):
        (self.site / "view.json").write_text('{"heading": "{{' + token + '}}"}')
        return [ref for _, ref, _ in find_violations(self.site, self.unpackaged, self.packaged)]

    def test_token_on_both_hops_passes(self):
        self.assertEqual(self.check("%%%NAMESPACED_ORG%%%cUnite_Volunteer_Role__r.%%%NAMESPACED_ORG%%%Minimum_Age__c"), [])

    def test_literal_prefix_on_unpackaged_field_fails(self):
        self.assertEqual(
            self.check("%%%NAMESPACED_ORG%%%cUnite_Volunteer_Role__r.FlowToolKit__Minimum_Age__c"),
            ["FlowToolKit__Minimum_Age__c"],
        )

    def test_bare_unpackaged_field_fails(self):
        self.assertEqual(self.check("cUnite_Volunteer_Role__r.Name"), ["cUnite_Volunteer_Role__r"])

    def test_packaged_field_with_literal_prefix_passes(self):
        self.assertEqual(self.check("FlowToolKit__cUnite_Subtitle__c"), [])

    def test_other_namespaces_are_ignored(self):
        self.assertEqual(self.check("GW_Volunteers__Campaign__r.Name"), [])


if __name__ == "__main__":
    unittest.main()
