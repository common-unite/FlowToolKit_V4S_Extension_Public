"""Guards against metadata deploys that report success while shipping nothing.

A metadata-format deploy cannot fail for components the manifest never asked
for: anything missing from package.xml is not an error, it simply was not
requested. So a stale manifest degrades every org built from the flow, silently
and indefinitely, while the deploy reports Succeeded.

That is what happened to scratch-org/site (see issue #29): the captured
ExperienceBundle was committed but never added to package.xml, so for months
every dev org deployed one sharing rule and none of the 43 site files. The
related failure is an empty payload, where dx_convert_from produces a package.xml
and nothing else, recognisable by a 316 byte deploy.

Neither case raises anything on its own. This task is the assertion that turns
both into a loud failure. See issue #30.
"""

from pathlib import Path
from xml.etree import ElementTree

from cumulusci.core.exceptions import CumulusCIException, TaskOptionsError
from cumulusci.core.tasks import BaseTask

METADATA_NAMESPACE = "{http://soap.sforce.com/2006/04/metadata}"

# Metadata-format directory name -> the type name package.xml must declare for
# it. An unrecognised directory is a hard error rather than a silent pass: a new
# metadata type has to be added here deliberately, which is the entire point.
DIRECTORY_TYPE_MAP = {
    "applications": "CustomApplication",
    "brandingSets": "BrandingSet",
    "classes": "ApexClass",
    "communityThemeDefinitions": "CommunityThemeDefinition",
    "contentassets": "ContentAsset",
    "customMetadata": "CustomMetadata",
    "experiences": "ExperienceBundle",
    "flexipages": "FlexiPage",
    "flows": "Flow",
    "labels": "CustomLabels",
    "layouts": "Layout",
    "lwc": "LightningComponentBundle",
    "networks": "Network",
    "objects": "CustomObject",
    "pages": "ApexPage",
    "permissionsets": "PermissionSet",
    "profiles": "Profile",
    "sharingRules": "SharingRules",
    "sites": "CustomSite",
    "staticresources": "StaticResource",
    "tabs": "CustomTab",
    "triggers": "ApexTrigger",
}


class AssertMetadataPayload(BaseTask):
    """Fail loudly when a metadata directory would deploy less than it should."""

    task_options = {
        "path": {
            "description": "Path to the metadata-format directory to check",
            "required": True,
        },
        "require_types": {
            "description": (
                "Comma-separated metadata type names this deploy must ship, "
                "e.g. ExperienceBundle,SharingRules. Each must be declared in "
                "package.xml with at least one member."
            ),
            "required": False,
        },
    }

    def _init_options(self, kwargs):
        super()._init_options(kwargs)
        raw = self.options.get("require_types") or ""
        self.required_types = [name.strip() for name in raw.split(",") if name.strip()]

    def _run_task(self):
        path = Path(self.options["path"])
        if not path.is_dir():
            raise TaskOptionsError(f"Not a directory: {path}")

        manifest = path / "package.xml"
        if not manifest.exists():
            raise CumulusCIException(f"No package.xml in {path}, nothing would deploy.")

        declared = self._declared_types(manifest)
        self._assert_required(path, declared)
        self._assert_no_orphans(path, declared)

        self.logger.info(
            f"{path} declares {len(declared)} metadata type(s): "
            f"{', '.join(sorted(declared)) or 'none'}"
        )

    def _declared_types(self, manifest):
        """Map declared type name -> member list, from package.xml."""
        root = ElementTree.parse(manifest).getroot()
        declared = {}
        for types_element in root.findall(f"{METADATA_NAMESPACE}types"):
            name = types_element.findtext(f"{METADATA_NAMESPACE}name")
            if not name:
                continue
            declared[name] = [
                member.text
                for member in types_element.findall(f"{METADATA_NAMESPACE}members")
                if member.text
            ]
        return declared

    def _assert_required(self, path, declared):
        """Every required type must be declared AND carry at least one member."""
        missing = [name for name in self.required_types if not declared.get(name)]
        if not missing:
            return
        raise CumulusCIException(
            f"{path}/package.xml does not deploy {', '.join(missing)}. "
            f"It declares: {', '.join(sorted(declared)) or 'nothing'}. "
            "The deploy would report success while shipping less than intended. "
            "Add the missing <types> entry to package.xml."
        )

    def _assert_no_orphans(self, path, declared):
        """Every metadata directory on disk must be declared in the manifest."""
        orphans = []
        unknown = []
        for child in sorted(path.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            if not any(child.rglob("*")):
                continue
            metadata_type = DIRECTORY_TYPE_MAP.get(child.name)
            if metadata_type is None:
                unknown.append(child.name)
            elif metadata_type not in declared:
                orphans.append(f"{child.name}/ ({metadata_type})")

        if unknown:
            raise CumulusCIException(
                f"{path} contains directories this guard does not recognise: "
                f"{', '.join(unknown)}. Add them to DIRECTORY_TYPE_MAP in "
                "tasks/metadata_guard.py so their manifest coverage is checked."
            )
        if orphans:
            raise CumulusCIException(
                f"{path} holds files that no <types> entry in package.xml claims: "
                f"{', '.join(orphans)}. They would be silently excluded from the "
                "deploy, which still reports success. This is issue #29 all over "
                "again. Add the missing <types> entries."
            )
