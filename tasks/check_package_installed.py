"""Preflight check: is a specific managed package already installed?

The usual idiom, ``'<namespace>' in tasks.get_installed_packages()``, cannot be
used for a same-namespace extension. The NPC conversion extension is namespaced
``FlowToolKit``, exactly like the base package, and ``GetInstalledPackages``
returns a dict keyed by namespace, so that check is already true the moment the
base is installed and a genuine first install would be skipped.

Querying ``InstalledSubscriberPackage`` by package NAME distinguishes the two.

Gates the one-time post-install content on the NPC plan, and is written with a
``package_name`` option so the NPSP conversion engine can reuse it.

Sets ``return_values["is_installed"]`` to True/False.

Register in ``cumulusci.yml``::

    tasks:
        check_npc_conversion_installed:
            class_path: tasks.check_package_installed.CheckPackageInstalled
            options:
                package_name: "Flow Tool Kit: AFNP | NPC Extension"
"""

from cumulusci.tasks.salesforce import BaseSalesforceApiTask


class CheckPackageInstalled(BaseSalesforceApiTask):
    task_docs = "Check whether a managed package is installed, by package name."

    task_options = {
        "package_name": {
            "description": "Name of the subscriber package to look for, as it "
            "appears in Setup under Installed Packages.",
            "required": True,
        },
    }

    def _run_task(self):
        package_name = self.options["package_name"]
        result = self.tooling.query(
            "SELECT SubscriberPackage.Name FROM InstalledSubscriberPackage"
        )

        installed_names = set()
        for record in result.get("records") or []:
            package = record.get("SubscriberPackage") or {}
            if package.get("Name"): installed_names.add(package["Name"])

        is_installed = package_name in installed_names
        self.return_values["is_installed"] = is_installed

        if is_installed: self.logger.info(f"'{package_name}' is already installed.")
        else: self.logger.info(f"'{package_name}' is not installed. This is a first install.")

        return self.return_values
