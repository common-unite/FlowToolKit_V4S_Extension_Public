from cumulusci.tasks.salesforce import BaseSalesforceApiTask


class GetRecordTypes(BaseSalesforceApiTask):
    task_options = {
        "object": {
            "description": "The name of the object to list record types for",
            "required": True,
        }
    }

    def _init_options(self, kwargs):
        super()._init_options(kwargs)
        if "object" in self.options:
            # Escape object to avoid SOQL injection
            self.options["object"] = self.options["object"].replace("'", "\\'")

    def _run_task(self):
        # Query the Tooling API and get all results
        result = self.tooling.query_all(
            f"SELECT Id, QualifiedApiName, NamespacePrefix FROM FlowToolKit__Form_Object__mdt "
            f"WHERE QualifiedApiName != 'Q'"
        )
        self.logger.info(
            f"Found {result['totalSize']} record types for {self.options['object']}"
        )

        # Create a dictionary with DeveloperName as the key


        self.logger.info(
            f"Found {result}"
        )

        # Add the record_types dictionary to the task's return_values
        self.return_values["record_types"] = record_types