from cumulusci.tasks.salesforce import BaseSalesforceApiTask


class CheckLWSEnabled(BaseSalesforceApiTask):
    """Preflight check: verifies Lightning Web Security is enabled.

    Queries SessionSettings.LockerServiceNext via the Tooling API.
    Without LWS, Lightning Locker's heavyweight SecureObject proxies
    cause severe performance degradation on components with large datasets.

    Sets return_values["is_enabled"] to True/False.
    """

    task_docs = "Check if Lightning Web Security (LWS) is enabled in the target org."

    def _run_task(self):
        result = self.tooling.query(
            "SELECT LockerServiceNext FROM SessionSettings"
        )
        if not result["records"]:
            self.return_values["is_enabled"] = False
            self.logger.warning("Could not read SessionSettings — assuming LWS is disabled.")
            return

        enabled = result["records"][0].get("LockerServiceNext", False)
        self.return_values["is_enabled"] = enabled

        if enabled:
            self.logger.info("Lightning Web Security is ENABLED.")
        else:
            self.logger.warning("Lightning Web Security is DISABLED.")
