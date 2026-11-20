"""Tests for the dev org guest sites (issue 50). Run from the repo root with the CumulusCI interpreter:
    "<cci venv>/bin/python" -m unittest tasks.tests.test_dev_guest_sites
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from cumulusci.core.exceptions import CumulusCIException

REPO = Path(__file__).resolve().parents[2]


def load_task_module(name):
    # Importing cumulusci.core.tasks empties the repo's tasks namespace path, so a second "from tasks.x import" fails; load by file instead
    spec = importlib.util.spec_from_file_location(f"tasks_{name}", REPO / "tasks" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AssertMetadataPayload = load_task_module("metadata_guard").AssertMetadataPayload
AssertSiteUsable = load_task_module("site_guard").AssertSiteUsable
AURA = REPO / "scratch-org/site/experiences/Volunteer_Portal1"
LWR = REPO / "scratch-org/site-lwr/digitalExperiences/site/LWR_Volunteer_Portal1"


def components(path):
    found = []

    def walk(node):
        if isinstance(node, dict):
            name = node.get("componentName") or node.get("definition")
            if name:
                found.append((name, node.get("componentAttributes") or node.get("attributes") or {}))
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(json.loads(path.read_text()))
    return found


def names(path):
    return [name for name, _ in components(path)]


class CapturedSitesTest(unittest.TestCase):
    def test_aura_home_places_the_job_finder(self):
        self.assertIn("FlowToolKit:volunteerJobsFinderPage", names(AURA / "views/home.json"))

    def test_aura_form_template_page_opens_the_template(self):
        route = json.loads((AURA / "routes/formTemplateDetail.json").read_text())
        self.assertEqual((route["objectApiName"], route["urlPrefix"]), ("FlowToolKit__Form_Template__c", "form-template"))
        attributes = dict(components(AURA / "views/formTemplateDetail.json"))["FlowToolKit:formTemplate"]
        self.assertEqual(attributes["recordId"], "{!recordId}")
        self.assertNotIn("forceCommunity:recordHeadline", names(AURA / "views/formTemplateDetail.json"), "the headline shows guests the owner's username")

    def test_lwr_site_is_public(self):
        site = json.loads((LWR / "sfdc_cms__site/LWR_Volunteer_Portal1/content.json").read_text())
        self.assertEqual(site["contentBody"]["authenticationType"], "AUTHENTICATED_WITH_PUBLIC_ACCESS_ENABLED")
        self.assertNotIn("geoBotsAllowed", site["contentBody"])

    def test_lwr_support_sits_in_the_theme_footer(self):
        layout = json.loads((LWR / "sfdc_cms__themeLayout/scopedHeaderAndFooter/content.json").read_text())
        footer = next(region for region in layout["contentBody"]["component"]["children"] if region["name"] == "footer")
        self.assertIn("FlowToolKit:flowToolKitLwrSupport", names_of(footer))

    def test_lwr_home_places_the_job_finder(self):
        self.assertIn("FlowToolKit:volunteerJobsFinderPage", names(LWR / "sfdc_cms__view/home/content.json"))

    def test_lwr_job_page_opens_the_jobs_form(self):
        attributes = dict(components(LWR / "sfdc_cms__view/volunteerJobDetail/content.json"))["FlowToolKit:formTemplate"]
        self.assertEqual(attributes, {"recordId": "{!Route.recordId}", "relatedFieldName": "FlowToolKit__Form_Template__c"})
        for route in ("Volunteer_Job_Detail__c", "Volunteer_Job_List__c", "Volunteer_Job_Related_List__c"):
            self.assertTrue((LWR / "sfdc_cms__route" / route / "content.json").exists(), route)

    def test_every_guest_sharing_rule_covers_both_sites(self):
        for name in ("Campaign", "FlowToolKit__Form_Template__c", "FlowToolKit__Form_Submission__c"):
            text = (REPO / "scratch-org/site/sharingRules" / f"{name}.sharingRules").read_text()
            for guest in ("<guestUser>Volunteer_Portal</guestUser>", "<guestUser>LWR_Volunteer_Portal</guestUser>"):
                self.assertIn(guest, text, f"{name} misses {guest}")

    def test_captured_folders_pass_the_payload_guard(self):
        for path, types in (("scratch-org/site", "ExperienceBundle,SharingRules"), ("scratch-org/site-lwr", "DigitalExperienceBundle")):
            guard(path, types)._run_task()


def names_of(node):
    found = []
    if isinstance(node, dict):
        if node.get("definition"):
            found.append(node["definition"])
        for value in node.values():
            found.extend(names_of(value))
    elif isinstance(node, list):
        for value in node:
            found.extend(names_of(value))
    return found


def guard(path, types):
    task = AssertMetadataPayload.__new__(AssertMetadataPayload)
    task.options = {"path": str(REPO / path)}
    task.required_types = types.split(",")
    task.logger = mock.Mock()
    return task


class MemberCheckTest(unittest.TestCase):
    def test_undeclared_sharing_rules_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sharingRules").mkdir()
            (root / "sharingRules/Campaign.sharingRules").write_text("<SharingRules/>")
            (root / "sharingRules/FlowToolKit__Form_Template__c.sharingRules").write_text("<SharingRules/>")
            (root / "package.xml").write_text(
                '<Package xmlns="http://soap.sforce.com/2006/04/metadata"><types><members>Campaign</members>'
                "<name>SharingRules</name></types></Package>"
            )
            with self.assertRaisesRegex(CumulusCIException, "FlowToolKit__Form_Template__c"):
                guard(tmp, "SharingRules")._run_task()


class SiteGuardTest(unittest.TestCase):
    def task(self, rows, **options):
        task = AssertSiteUsable.__new__(AssertSiteUsable)
        task.options = {"network_name": "LWR Volunteer Portal", **options}
        task.logger = mock.Mock()
        task.required_permission_sets = ["Form_Flow_User"]
        task.guest_shared_records = [pair.split(":", 1) for pair in options.get("guest_shared_records", "").split(";") if ":" in pair]
        task.active_flows = [name for name in options.get("active_flows", "").split(",") if name]
        task.guest_api = options.get("guest_api") == "True"

        def query_all(soql):
            for prefix, result in rows.items():
                if soql.startswith(prefix):
                    return result
            return []

        task._query_all = query_all
        return task

    def base_rows(self, **overrides):
        rows = {
            "SELECT Id, Name, Status, OptionsGuestChatterEnabled FROM Network": [{"Id": "0DB", "Name": "LWR Volunteer Portal", "Status": "Live", "OptionsGuestChatterEnabled": True}],
            "SELECT Id, Name, GuestUserId FROM Site": [{"Id": "0DM", "Name": "LWR_Volunteer_Portal1", "GuestUserId": "005G"}],
            "SELECT PermissionSet.Name": [{"PermissionSet": {"Name": "Form_Flow_User"}}],
            "SELECT Id FROM FlowToolKit__Form_Template__c": [{"Id": "a0M1"}, {"Id": "a0M2"}],
            "SELECT Id FROM Group": [{"Id": "00GG"}],
            "SELECT ParentId FROM FlowToolKit__Form_Template__Share": [{"ParentId": "a0M1"}, {"ParentId": "a0M2"}],
            "SELECT ApiName FROM FlowDefinitionView": [{"ApiName": "Form_Submission_Upsert_Guest"}],
        }
        rows.update(overrides)
        return rows

    OPTIONS = {"guest_shared_records": "FlowToolKit__Form_Template__c:FlowToolKit__IsActive__c = true", "active_flows": "Form_Submission_Upsert_Guest", "guest_api": "True"}

    def test_usable_site_passes(self):
        self.task(self.base_rows(), **self.OPTIONS)._run_task()

    def test_unshared_template_fails(self):
        rows = self.base_rows(**{"SELECT ParentId FROM FlowToolKit__Form_Template__Share": [{"ParentId": "a0M1"}]})
        with self.assertRaisesRegex(CumulusCIException, "1 of 2 FlowToolKit__Form_Template__c"):
            self.task(rows, **self.OPTIONS)._run_task()

    def test_inactive_override_fails(self):
        rows = self.base_rows(**{"SELECT ApiName FROM FlowDefinitionView": []})
        with self.assertRaisesRegex(CumulusCIException, "Form_Submission_Upsert_Guest is not active"):
            self.task(rows, **self.OPTIONS)._run_task()

    def test_guest_api_off_fails(self):
        network = [{"Id": "0DB", "Name": "LWR Volunteer Portal", "Status": "Live", "OptionsGuestChatterEnabled": False}]
        rows = self.base_rows(**{"SELECT Id, Name, Status, OptionsGuestChatterEnabled FROM Network": network})
        with self.assertRaisesRegex(CumulusCIException, "Guest API access is off"):
            self.task(rows, **self.OPTIONS)._run_task()


if __name__ == "__main__":
    unittest.main()
