"""CCI task to map values of a DEPENDENT picklist to their controlling values.

``AddPicklistEntries`` can add a value to a dependent picklist, but it never
writes ``<valueSettings>``. A value with no ``valueSettings`` row is valid under
no controlling value at all: it is invisible in the UI and any DML that sets it
fails with ``INVALID_OR_NULL_FOR_RESTRICTED_PICKLIST``. This task supplies the
missing half, so the pair together makes an injected value actually usable.

This works against a field owned by an INSTALLED MANAGED PACKAGE. The field is
retrieved from the target org, the new rows are merged into the value set that
org already has, and it is deployed back. Nothing is redefined from local
source, which is what makes it safe: a static field file in the repo would
overwrite the value set with a snapshot and silently drop any value the upstream
package added after that snapshot was taken.

Vendored into this repo's ``tasks/`` package so MetaDeploy can import it. The
MetaDeploy worker container runs stock CumulusCI and has no
``cci_flowtoolkit_tasks`` installed, so a ``cci_flowtoolkit_tasks.*`` class_path
raises ImportError mid install for the subscriber. Keep this file in sync with
``cci-flowtoolkit-tasks/cci_flowtoolkit_tasks/picklist_dependency.py``.

Namespace tokens (``%%%NAMESPACE%%%``) in the three API names are injected exactly as
``add_picklist_entries`` does it, so one definition serves a subscriber org (managed,
prefixed) and a namespaced development org (``-o managed False``, bare names).

Register in ``cumulusci.yml``::

    tasks:
        inject_conversion_rule_dependency:
            class_path: tasks.picklist_dependency.AddPicklistDependencies
            options:
                object_api_name: FlowToolKit__Form_Template__c
                field_api_name: FlowToolKit__Conversion_Rules__c
                controlling_field_api_name: FlowToolKit__Conversion_Type__c
                dependencies:
                    - value: Volunteer Application
                      controlling_values:
                          - Volunteer Application

Usage::

    cci task run inject_conversion_rule_dependency --org install_test
"""

from __future__ import annotations

from cumulusci.core.exceptions import TaskOptionsError
from cumulusci.core.utils import process_list_arg
from cumulusci.tasks.metadata_etl import MetadataSingleEntityTransformTask
from cumulusci.utils.xml.metadata_tree import MetadataElement


class AddPicklistDependencies(MetadataSingleEntityTransformTask):
    entity = "CustomObject"
    task_options = {
        "object_api_name": {
            "description": "API name of the object owning the dependent picklist.",
            "required": True,
        },
        "field_api_name": {
            "description": "API name of the dependent picklist field.",
            "required": True,
        },
        "controlling_field_api_name": {
            "description": "API name of the controlling field. Used to verify the "
            "field is actually dependent, and on the controller it is expected to be.",
            "required": True,
        },
        "dependencies": {
            "description": "List of mappings. Each needs 'value', the dependent "
            "picklist value, and 'controlling_values', the list of controlling "
            "values it should be selectable under.",
            "required": True,
        },
        **MetadataSingleEntityTransformTask.task_options,
    }

    def _init_options(self, kwargs):
        self.task_config.options["api_names"] = "dummy"
        super()._init_options(kwargs)

        self.object_api_name = self._inject_namespace(self.options["object_api_name"])
        self.field_api_name = self._inject_namespace(self.options["field_api_name"])
        self.controlling_field_api_name = self._inject_namespace(self.options["controlling_field_api_name"])
        self.api_names = {self.object_api_name}

        self.dependencies = []
        for dep in process_list_arg(self.options["dependencies"]):
            if "value" not in dep:
                raise TaskOptionsError(
                    "The 'value' key is required on every dependency."
                )
            controlling = process_list_arg(dep.get("controlling_values") or [])
            if not controlling:
                raise TaskOptionsError(
                    f"Dependency '{dep['value']}' needs at least one controlling value."
                )
            self.dependencies.append((dep["value"], controlling))

    def _transform_entity(self, metadata: MetadataElement, api_name: str):
        field = metadata.find("fields", fullName=self.field_api_name)
        if not field:
            raise TaskOptionsError(
                f"The field {api_name}.{self.field_api_name} was not found."
            )

        value_set = field.find("valueSet")
        if not value_set:
            raise TaskOptionsError(
                f"{api_name}.{self.field_api_name} is not a picklist."
            )

        controlling = value_set.find("controllingField")
        if not controlling:
            raise TaskOptionsError(
                f"{api_name}.{self.field_api_name} is not a dependent picklist. "
                "Use add_picklist_entries instead."
            )
        if controlling.text != self.controlling_field_api_name:
            raise TaskOptionsError(
                f"{api_name}.{self.field_api_name} is controlled by "
                f"'{controlling.text}', not '{self.controlling_field_api_name}'."
            )

        for value, controlling_values in self.dependencies:
            self._map_value(value_set, value, controlling_values)

        return metadata

    def _map_value(
        self, value_set: MetadataElement, value: str, controlling_values: list
    ):
        """Merge one value's controlling values into its valueSettings row.

        The row is created when absent. When it already exists only missing
        controlling values are appended, so re-running is a no-op and a value
        already mapped by hand in Setup is never narrowed.
        """
        settings = None
        for candidate in value_set.findall("valueSettings"):
            name = candidate.find("valueName")
            if name is not None and name.text == value:
                settings = candidate
                break

        if settings is None:
            settings = value_set.append("valueSettings")
            for controlling_value in controlling_values:
                settings.append("controllingFieldValue", text=controlling_value)
            settings.append("valueName", text=value)
            self.logger.info(
                f"Mapping '{value}' to controlling value(s): "
                f"{', '.join(controlling_values)}"
            )
            return

        existing = {
            element.text for element in settings.findall("controllingFieldValue")
        }
        missing = [c for c in controlling_values if c not in existing]
        if not missing:
            self.logger.info(f"'{value}' is already mapped. Leaving it alone.")
            return

        for controlling_value in missing:
            settings.insert_before(
                settings.find("valueName"),
                "controllingFieldValue",
                text=controlling_value,
            )
        self.logger.info(
            f"Adding controlling value(s) to '{value}': {', '.join(missing)}"
        )
