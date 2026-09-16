#!/usr/bin/env bash
# Fail loudly when a scratch org is not on the Salesforce release we build against.
#
#   scripts/assert_org_release.sh <sf alias or username> "<release label prefix>"
#   scripts/assert_org_release.sh flowtoolkit_Budget__sprint_2026-08-grantmaking "Summer '26"
#
# During a release preview window (see "Select the Salesforce Release for a Scratch Org" in the DX guide)
# unpinned scratch orgs are supposed to match the Dev Hub, but instance-pool assignment does not honor that
# reliably: same-day creations have landed on both releases. Preview instances report the next API version
# under the label "Latest Release", so a mismatch here means the org runs the upcoming release.
set -euo pipefail
ORG="${1:?sf alias or username}"
EXPECTED="${2:?expected release label prefix, for example Summer 26}"

INSTANCE=$(sf org display -o "$ORG" --json 2>/dev/null | python3 -c "import sys,json; print(json.loads(sys.stdin.read(), strict=False)['result']['instanceUrl'])")
IFS=$'\t' read -r LABEL VERSION < <(curl -sf "$INSTANCE/services/data/" | python3 -c "import sys,json; v=json.load(sys.stdin)[-1]; print(v['label'] + '\t' + v['version'])")

if [[ "$LABEL" == "$EXPECTED"* ]]; then
  echo "OK: $ORG is on $LABEL (API v$VERSION)"
  exit 0
fi
echo "MISMATCH: $ORG is on '$LABEL' (API v$VERSION), expected '$EXPECTED'. Delete it and create again; the pool picks the instance." >&2
exit 1
