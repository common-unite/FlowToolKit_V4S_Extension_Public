#!/bin/bash
# Activates the demo site. Network.Status is not writable by Apex DML and the Connect API
# exposes no activation verb, so the sObject REST endpoint is the only scriptable route.
set -euo pipefail

SITE_NAME="${SITE_NAME:-Volunteer Portal}"
API_VERSION="${API_VERSION:-65.0}"

if [ -z "${SF_ACCESS_TOKEN:-}" ] || [ -z "${SF_ORG_INSTANCE_URL:-}" ]; then
    echo "SF_ACCESS_TOKEN and SF_ORG_INSTANCE_URL are required (CumulusCI SalesforceCommand supplies both)." >&2
    exit 1
fi

query=$(printf 'SELECT Id, Status FROM Network WHERE Name = %s LIMIT 1' "'${SITE_NAME}'" | sed 's/ /+/g')
response=$(curl -sS -H "Authorization: Bearer ${SF_ACCESS_TOKEN}" \
    "${SF_ORG_INSTANCE_URL}/services/data/v${API_VERSION}/query?q=${query}")

network_id=$(printf '%s' "$response" | python3 -c "
import json, sys
records = json.load(sys.stdin).get('records', [])
print(records[0]['Id'] if records else '')
")

if [ -z "$network_id" ]; then
    echo "Site '${SITE_NAME}' not found; nothing to activate."
    exit 0
fi

status=$(curl -sS -o /dev/null -w '%{http_code}' -X PATCH \
    -H "Authorization: Bearer ${SF_ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"Status":"Live"}' \
    "${SF_ORG_INSTANCE_URL}/services/data/v${API_VERSION}/sobjects/Network/${network_id}")

if [ "$status" = "204" ]; then
    echo "Site '${SITE_NAME}' is Live."
else
    echo "Activation returned HTTP ${status} for '${SITE_NAME}'." >&2
    exit 1
fi
