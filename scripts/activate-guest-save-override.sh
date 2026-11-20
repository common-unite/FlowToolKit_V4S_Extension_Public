#!/bin/bash
# DEV ORGS ONLY (#50): the base installer leaves its Guest Save Override flow inactive for the admin to review; a dev org's guest sites need it active.
set -euo pipefail

FLOW_NAME="${1:-Form_Submission_Upsert_Guest}"
API_VERSION="${API_VERSION:-65.0}"

if [ -z "${SF_ACCESS_TOKEN:-}" ] || [ -z "${SF_ORG_INSTANCE_URL:-}" ]; then
    echo "SF_ACCESS_TOKEN and SF_ORG_INSTANCE_URL are required (CumulusCI SalesforceCommand supplies both)." >&2
    exit 1
fi

tooling="${SF_ORG_INSTANCE_URL}/services/data/v${API_VERSION}/tooling"
query=$(printf "SELECT Id, ActiveVersionId, LatestVersion.VersionNumber FROM FlowDefinition WHERE DeveloperName = '%s'" "$FLOW_NAME" | python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read().strip()))")
read -r definition_id active latest < <(curl -sS -H "Authorization: Bearer ${SF_ACCESS_TOKEN}" "${tooling}/query?q=${query}" | python3 -c "
import json, sys
records = json.load(sys.stdin).get('records', [])
row = records[0] if records else {}
print(row.get('Id') or '-', row.get('ActiveVersionId') or '-', (row.get('LatestVersion') or {}).get('VersionNumber') or '-')
")

if [ "$definition_id" = "-" ]; then
    echo "Flow ${FLOW_NAME} not found. The base installer's guest save override was not deployed." >&2
    exit 1
fi
if [ "$active" != "-" ]; then
    echo "Flow ${FLOW_NAME} is already active."
    exit 0
fi

status=$(curl -sS -o /dev/null -w '%{http_code}' -X PATCH \
    -H "Authorization: Bearer ${SF_ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"Metadata\":{\"activeVersionNumber\":${latest}}}" \
    "${tooling}/sobjects/FlowDefinition/${definition_id}")

if [ "$status" = "204" ]; then
    echo "Flow ${FLOW_NAME} version ${latest} is active."
else
    echo "Activating ${FLOW_NAME} returned HTTP ${status}." >&2
    exit 1
fi
