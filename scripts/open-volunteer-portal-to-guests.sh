#!/bin/bash
# Flips the site's isAvailableToGuests, without which every route redirects guests to login.
# Retrieve-edit-deploy of that ONE key only: a full-bundle round trip fails on route pageAccess,
# which Salesforce refuses to add or change through the Metadata API.
set -euo pipefail

SITE_DEV_NAME="${SITE_DEV_NAME:-Volunteer_Portal1}"
SITE_NAME="${SITE_NAME:-Volunteer Portal}"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

# CumulusCI's SalesforceCommand supplies credentials but no org alias, so mint a throwaway one.
if [ -z "${TARGET_ORG:-}" ]; then
    if [ -z "${SF_ACCESS_TOKEN:-}" ] || [ -z "${SF_ORG_INSTANCE_URL:-}" ]; then
        echo "Set TARGET_ORG, or run through CumulusCI's SalesforceCommand." >&2
        exit 1
    fi
    TARGET_ORG="volunteer_portal_guest_access"
    sf org login access-token --instance-url "$SF_ORG_INSTANCE_URL" --alias "$TARGET_ORG" --no-prompt >/dev/null
fi

sf project retrieve start --metadata "ExperienceBundle:${SITE_DEV_NAME}" \
    --target-org "$TARGET_ORG" --target-metadata-dir "$WORK_DIR" --unzip >/dev/null

BUNDLE_ROOT="$WORK_DIR/unpackaged/unpackaged"
CONFIG_DIR="$BUNDLE_ROOT/experiences/${SITE_DEV_NAME}/config"

if [ ! -d "$CONFIG_DIR" ]; then
    echo "No ExperienceBundle retrieved for ${SITE_DEV_NAME}. Enable ExperienceBundle Metadata API first (orgs/dev.json)." >&2
    exit 1
fi

python3 - "$CONFIG_DIR" <<'PY'
import glob, json, os, sys
changed = False
for path in glob.glob(os.path.join(sys.argv[1], '*.json')):
    with open(path) as handle: config = json.load(handle)
    if 'isAvailableToGuests' not in config: continue
    if config['isAvailableToGuests'] is True:
        print('Already open to guests:', os.path.basename(path)); continue
    config['isAvailableToGuests'] = True
    with open(path, 'w') as handle: json.dump(config, handle, indent=2)
    changed = True
    print('Opened to guests:', os.path.basename(path))
print('CHANGED' if changed else 'NO_CHANGE')
PY

sf project deploy start --metadata-dir "$BUNDLE_ROOT" --target-org "$TARGET_ORG" --wait 15 >/dev/null
sf community publish --name "$SITE_NAME" --target-org "$TARGET_ORG" >/dev/null
echo "Volunteer Portal is open to guests."
