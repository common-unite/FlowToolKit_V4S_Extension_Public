from cumulusci.tasks.salesforce import BaseSalesforceApiTask


class CheckSObjectsAvailable(BaseSalesforceApiTask):
    """Preflight check: the set of sobject API names available in the org.

    The NPC plan uses this to confirm Nonprofit Cloud objects
    (PartyRelationshipGroup, ContactContactRelation) exist before allowing the
    install, so a non-Nonprofit-Cloud org is sent to the standard plan instead.

    A global describe lists both objects on a real NPC org, so membership in the
    returned list is a reliable gate. Sets return_values["sobjects"] to a sorted
    list of API names.
    """

    task_docs = "List the sobject API names available in the target org."

    def _run_task(self):
        names = sorted(entry["name"] for entry in self.sf.describe()["sobjects"])
        self.return_values["sobjects"] = names
        self.logger.info(f"{len(names)} sobjects available in the org.")
        return self.return_values
