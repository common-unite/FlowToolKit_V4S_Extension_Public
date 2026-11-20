#!/bin/bash
# Activates a demo site. Network.Status is not writable by Apex DML and the Connect API
# exposes no activation verb, so the sObject REST endpoint is the only scriptable route.
# Usage: activate-volunteer-portal.sh ["Site Name"] [guest-api]. guest-api also turns on guest API access (OptionsGuestChatterEnabled and
# OptionsGuestFileAccessEnabled): an LWR guest's ui-api calls return 401 without it (#50).
set -euo pipefail

SITE_NAME="${1:-${SITE_NAME:-Volunteer Portal}}"
API_VERSION="${API_VERSION:-65.0}"
GUEST_API="${GUEST_API:-false}"
[ "${2:-}" = "guest-api" ] && GUEST_API=true

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

body='{"Status":"Live"}'
if [ "$GUEST_API" = "true" ]; then
    body='{"Status":"Live","OptionsGuestChatterEnabled":true,"OptionsGuestFileAccessEnabled":true}'
fi

status=$(curl -sS -o /dev/null -w '%{http_code}' -X PATCH \
    -H "Authorization: Bearer ${SF_ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$body" \
    "${SF_ORG_INSTANCE_URL}/services/data/v${API_VERSION}/sobjects/Network/${network_id}")

if [ "$status" = "204" ]; then
    echo "Site '${SITE_NAME}' is Live$([ "$GUEST_API" = "true" ] && echo ' with guest API access')."
else
    echo "Activation returned HTTP ${status} for '${SITE_NAME}'." >&2
    exit 1
fi
