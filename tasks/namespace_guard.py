"""Guards the demo site against field names that resolve in only one kind of org.

The demo site's Site Design Blocks read their {{Field__c}} tokens through the UI
API (getRecord optionalFields). The UI API does not fill in an org's own
namespace, so a token has to spell the field exactly as that org names it:

- Packaged fields (force-app) are FlowToolKit__ prefixed in every org, so a
  literal FlowToolKit__ prefix is right everywhere.
- Unpackaged fields (force-app-unpackaged-objects) are FlowToolKit__ prefixed in
  a namespaced dev org, where everything deployed takes the namespace, but bare
  in an org with the package installed. Neither spelling works in both, so they
  carry the CumulusCI token %%%NAMESPACED_ORG%%%, which the deploy task turns
  into FlowToolKit__ in a namespaced org and into nothing everywhere else.

A captured site retrieved from a dev org comes back with the literal prefix on
every field, so a re-capture silently breaks the page in subscriber orgs while
looking perfect in dev. A bare unpackaged name does the reverse. This task fails
on either, before the site deploys.
"""

import re
from pathlib import Path

from cumulusci.core.exceptions import CumulusCIException, TaskOptionsError
from cumulusci.core.tasks import BaseTask

TOKEN = "%%%NAMESPACED_ORG%%%"
PREFIX = "FlowToolKit__"
# A field or relationship name as it appears inside a {{token}}, with what precedes it
FIELD_REFERENCE = re.compile(r"(?<![A-Za-z0-9_%])(%%%NAMESPACED_ORG%%%|FlowToolKit__)?([A-Za-z][A-Za-z0-9_]*__[cr])\b")


def field_names(source_dir):
    """Every custom field API name under an sfdx source dir, as Name__c and Name__r."""
    names = set()
    for meta in Path(source_dir).glob("main/default/objects/*/fields/*.field-meta.xml"):
        api_name = meta.name[: -len(".field-meta.xml")]
        names.add(api_name)
        names.add(api_name[:-3] + "__r")
    return names


def find_violations(site_dir, unpackaged, packaged):
    """List (file, reference, reason) for every token spelled wrong for its field."""
    violations = []
    for path in sorted(Path(site_dir).rglob("*.json")):
        text = path.read_text(encoding="utf-8")
        for match in FIELD_REFERENCE.finditer(text):
            qualifier, name = match.group(1) or "", match.group(2)
            if name in packaged:
                continue
            if name not in unpackaged:
                continue
            if qualifier == PREFIX:
                violations.append((path, match.group(0), "literal FlowToolKit__ renders empty in subscriber orgs"))
            elif qualifier == "":
                violations.append((path, match.group(0), "bare name renders empty in namespaced dev orgs"))
    return violations


class AssertUnpackagedFieldsTokenized(BaseTask):
    """Fail when the demo site names an unpackaged field any way but %%%NAMESPACED_ORG%%%Name."""

    task_options = {
        "path": {"description": "Metadata-format site directory to check, e.g. scratch-org/site", "required": True},
        "unpackaged_dirs": {
            "description": "Comma-separated sfdx source dirs whose fields are unpackaged. Defaults to force-app-unpackaged-objects.",
            "required": False,
        },
        "packaged_dirs": {
            "description": "Comma-separated sfdx source dirs whose fields are packaged. Defaults to force-app.",
            "required": False,
        },
    }

    def _init_options(self, kwargs):
        super()._init_options(kwargs)
        self.unpackaged_dirs = self._split("unpackaged_dirs", "force-app-unpackaged-objects")
        self.packaged_dirs = self._split("packaged_dirs", "force-app")

    def _split(self, option, default):
        raw = self.options.get(option) or default
        return [part.strip() for part in raw.split(",") if part.strip()]

    def _run_task(self):
        site = Path(self.options["path"])
        if not site.is_dir():
            raise TaskOptionsError(f"Not a directory: {site}")

        unpackaged = set().union(*(field_names(d) for d in self.unpackaged_dirs))
        packaged = set().union(*(field_names(d) for d in self.packaged_dirs))
        if not unpackaged:
            raise TaskOptionsError(f"No fields found under {', '.join(self.unpackaged_dirs)}; nothing to check against.")

        violations = find_violations(site, unpackaged, packaged)
        if violations:
            lines = "\n".join(f"  {path}: {ref} ({reason})" for path, ref, reason in violations)
            raise CumulusCIException(
                f"{len(violations)} unpackaged field reference(s) in {site} will render empty in one kind of org. "
                f"Write each as {TOKEN}<Field>, see tasks/namespace_guard.py:\n{lines}"
            )
        self.logger.info(f"{site}: every unpackaged field reference carries {TOKEN}.")
