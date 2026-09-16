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
    }

    def _init_options(self, kwargs):
        super()._init_options(kwargs)
        raw = self.options.get("guest_permission_sets") or ""
        self.required_permission_sets = [
            name.strip() for name in raw.split(",") if name.strip()
        ] or list(REQUIRED_GUEST_PERMISSION_SETS)

    def _run_task(self):
        network_name = self.options["network_name"]
        problems = []

        network = self._query_one(
            "SELECT Id, Name, Status FROM Network WHERE Name = "
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

        problems.extend(self._guest_permission_problems(network_name))

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
