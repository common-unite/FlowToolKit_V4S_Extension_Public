"""Asserts the demo Experience Cloud site is actually usable after config_dev.

Steps 50-55 are all ignore_failure, which is a reasonable stance for demo
scaffolding that should not sink a dev org build. The cost is that a site can
finish those steps looking built while being unusable, and nothing says so.
Every one of these has happened:

- the site stays UnderConstruction, so guests are redirected to login
- the guest user never gets its permission sets, so the Job Finder is empty
- the captured bundle never deploys, so there are no page assignments (#29)

Rather than make each step strict and risk the flow dying on transient
ordering failures, this asserts the outcome once, at the end. Steps stay
tolerant; an unusable site becomes impossible to miss. See issue #30.
"""

from cumulusci.core.exceptions import CumulusCIException
from cumulusci.tasks.salesforce import BaseSalesforceApiTask

REQUIRED_GUEST_PERMISSION_SETS = ["Form_Flow_User", "Form_Flow_V4S_User"]


class AssertSiteUsable(BaseSalesforceApiTask):
    """Fail the flow when the demo site exists but would not work for a guest."""

    task_options = {
        "network_name": {
            "description": "Name of the Network to check, e.g. Volunteer Portal",
            "required": True,
        },
        "guest_permission_sets": {
            "description": (
                "Comma-separated permission set API names the site's guest user "
                f"must hold. Defaults to {', '.join(REQUIRED_GUEST_PERMISSION_SETS)}."
            ),
            "required": False,
        },
        "guest_shared_records": {
            "description": (
                "Semicolon-separated Object:WHERE pairs, e.g. "
                "FlowToolKit__Form_Template__c:FlowToolKit__IsActive__c = true. Every "
                "matching record must carry a GuestRule share to the site's guest user."
            ),
            "required": False,
        },
        "active_flows": {
            "description": "Comma-separated flow API names that must have an active version.",
            "required": False,
        },
        "guest_api": {
            "description": "True when the Network must allow guest API access (LWR guests get 401 without it).",
            "required": False,
        },
    }

    def _init_options(self, kwargs):
        super()._init_options(kwargs)
        raw = self.options.get("guest_permission_sets") or ""
        self.required_permission_sets = [
            name.strip() for name in raw.split(",") if name.strip()
        ] or list(REQUIRED_GUEST_PERMISSION_SETS)
        self.guest_shared_records = [
            pair.strip().split(":", 1)
            for pair in (self.options.get("guest_shared_records") or "").split(";")
            if ":" in pair
        ]
        self.active_flows = [
            name.strip() for name in (self.options.get("active_flows") or "").split(",") if name.strip()
        ]
        self.guest_api = str(self.options.get("guest_api") or "").lower() == "true"

    def _run_task(self):
        network_name = self.options["network_name"]
        problems = []

        network = self._query_one(
            "SELECT Id, Name, Status, OptionsGuestChatterEnabled FROM Network WHERE Name = "
            f"'{self._escape(network_name)}'"
        )
        if not network:
            raise CumulusCIException(
                f"No Network named '{network_name}'. The site was never created, "
                "so every later step was a no-op."
            )

        if network["Status"] != "Live":
            problems.append(
                f"Network.Status is '{network['Status']}', not 'Live'. Guests are "
                "redirected to the login page. Check activate_volunteer_portal."
            )

        if self.guest_api and not network.get("OptionsGuestChatterEnabled"):
            problems.append(
                "Guest API access is off on the Network, so every ui-api call a "
                "guest makes returns 401. Check activate-volunteer-portal.sh guest-api."
            )

        problems.extend(self._guest_permission_problems(network_name))
        problems.extend(self._guest_share_problems(network_name))
        problems.extend(self._inactive_flow_problems())

        if problems:
            raise CumulusCIException(
                f"The '{network_name}' site finished config_dev but is not usable:\n"
                + "\n".join(f"  - {problem}" for problem in problems)
                + "\nThose steps carry ignore_failure, so they will not have "
                "reported anything. See issue #30."
            )

        self.logger.info(
            f"'{network_name}' is Live and its guest user holds "
            f"{', '.join(self.required_permission_sets)}."
        )

    def _guest_permission_problems(self, network_name):
        guest_user_id = self._resolve_guest_user_id(network_name)
        if not guest_user_id:
            return [
                f"No active Site matching '{network_name}' has a guest user, so "
                "guest access cannot work at all. Check create_community and "
                "scripts/setup-volunteer-portal-site.apex."
            ]

        assigned = {
            row["PermissionSet"]["Name"]
            for row in self._query_all(
                "SELECT PermissionSet.Name FROM PermissionSetAssignment "
                f"WHERE AssigneeId = '{guest_user_id}'"
            )
            if row.get("PermissionSet")
        }
        missing = [
            name for name in self.required_permission_sets if name not in assigned
        ]
        if not missing:
            return []
        return [
            f"The site's guest user is missing permission set(s): "
            f"{', '.join(missing)}. The Job Finder will show guests nothing. "
            "Check scripts/setup-volunteer-portal-site.apex."
        ]

    def _guest_share_problems(self, network_name):
        if not self.guest_shared_records:
            return []
        guest_user_id = self._resolve_guest_user_id(network_name)
        if not guest_user_id:
            return []
        # A guest sharing rule shares to the guest's GuestUserGroup, not to the user itself
        recipients = [guest_user_id] + [
            row["Id"]
            for row in self._query_all(
                f"SELECT Id FROM Group WHERE Type = 'GuestUserGroup' AND RelatedId = '{guest_user_id}'"
            )
        ]
        recipient_list = ", ".join(f"'{recipient}'" for recipient in recipients)
        problems = []
        for object_name, where in self.guest_shared_records:
            record_ids = {row["Id"] for row in self._query_all(f"SELECT Id FROM {object_name} WHERE {where}")}
            if not record_ids:
                continue
            share_object = (object_name[:-3] + "__Share") if object_name.endswith("__c") else object_name + "Share"
            parent_field = "ParentId" if object_name.endswith("__c") else object_name + "Id"
            shared = {
                row[parent_field]
                for row in self._query_all(
                    f"SELECT {parent_field} FROM {share_object} "
                    f"WHERE RowCause = 'GuestRule' AND UserOrGroupId IN ({recipient_list})"
                )
            }
            missing = record_ids - shared
            if missing:
                problems.append(
                    f"{len(missing)} of {len(record_ids)} {object_name} records ({where}) "
                    "are not shared to the guest user, so a guest cannot open them. "
                    "Check the guest sharing rules in scratch-org/site/sharingRules."
                )
        return problems

    def _inactive_flow_problems(self):
        if not self.active_flows:
            return []
        names = ", ".join(f"'{name}'" for name in self.active_flows)
        active = {
            row["ApiName"]
            for row in self._query_all(
                f"SELECT ApiName FROM FlowDefinitionView WHERE ApiName IN ({names}) AND IsActive = true"
            )
        }
        return [
            f"Flow {name} is not active, so a guest save that needs it fails. "
            "Check scripts/activate-guest-save-override.sh."
            for name in self.active_flows
            if name not in active
        ]

    def _resolve_guest_user_id(self, network_name):
        """Match a Site to the Network by name, as setup-volunteer-portal-site.apex does.

        create_community appends a numeric suffix to the site developer name, so
        Volunteer Portal becomes Volunteer_Portal1. Match on prefix rather than
        equality, and normalise spaces the same way that script does.
        """
        wanted = network_name.replace(" ", "_").lower()
        for site in self._query_all(
            "SELECT Id, Name, GuestUserId FROM Site "
            "WHERE Status = 'Active' AND GuestUserId != null"
        ):
            if site["Name"].replace(" ", "_").lower().startswith(wanted):
                return site["GuestUserId"]
        return None

    def _query_all(self, soql):
        return self.sf.query_all(soql)["records"]

    def _query_one(self, soql):
        records = self._query_all(soql)
        return records[0] if records else None

    @staticmethod
    def _escape(value):
        return value.replace("\\", "\\\\").replace("'", "\\'")
