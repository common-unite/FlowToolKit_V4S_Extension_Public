from cumulusci.tasks.util import FindReplace as FindReplace


class FindReplaceUsername(FindReplace):
    salesforce_task = True # Require a target org

    def _init_options(self, kwargs):
        # Run the _init_options logic from FindReplace
        super()._init_options(kwargs)
        # Set the replace option to the org's username
        self.options["replace"] = self.org_config.username