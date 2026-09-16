# Volunteer Portal (demo Experience Cloud site)

Guest-facing rendering is a core part of this product, so every dev org gets a site to
test in. `config_dev` steps 50-54 create **Volunteer Portal** (`/volunteers`, Build Your
Own), publish it, assign the guest user's permission sets, deploy this folder, and
republish. Every step carries `ignore_failure: True`, so they no-op harmlessly on an org
where the site already exists or the bundle below has not been captured yet.

Scratch-org scaffolding only. Never packaged. It sits outside `force-app`.

## What is automated vs. captured

| Automated by `config_dev` | Manual once, then captured into this folder |
| --- | --- |
| Site creation and publish | Making pages public ("Public can access the site") |
| **Activation** (`Network.Status = Live`, step 53) | Page assignments (which packaged page serves which route) |
| Guest permission sets (`Form_Flow_User`, `Form_Flow_V4S_User`) | Theme, branding, navigation menu |
| Guest sharing rule on Campaign (`sharingRules/Campaign.sharingRules`) | |
| Campaign Member cleanup (guest PII, see `documents/security/`) | |

### Activation: use the sObject REST endpoint, nothing else works

`scripts/activate-volunteer-portal.sh` PATCHes `Network.Status` to `Live` and is wired as
the `activate_volunteer_portal` task (CumulusCI's `SalesforceCommand` supplies
`SF_ACCESS_TOKEN` and `SF_ORG_INSTANCE_URL`). Verified end to end: toggled the site back
to `UnderConstruction`, ran the task, site returned to `Live`.

Three other routes were tried against a real org and all fail, so do not re-try them:

- **Apex DML on Network** does not compile; the object is not DML-writable.
- **Network metadata deploy** (`<status>Live</status>`) rejects its own retrieved
  `unfiled$public/Community*EmailTemplate` references with "no EmailTemplate named ...
  found". Substituting a real folder path fails identically for managed-package templates.
- **Connect API**: `ConnectApi.CommunityInput` is not a valid type in this API version, and
  REST `/connect/communities/{id}` allows only GET and HEAD.

### What activation does NOT do

`Live` alone does not make pages reachable by a guest: the browser still lands on
`/s/login/?ec=302`. Per-page public access is an Experience Builder setting that lives in
the ExperienceBundle, and a site created by `create_community` has no bundle until it is
opened and saved in Builder once. That is the same Builder session as page assignment, so
both are covered by the capture below.

## One-time capture

A community created by `create_community` has no ExperienceBundle until it is opened and
saved in Experience Builder once. Until then a retrieve returns "Nothing retrieved",
which is exactly what a fresh org does.

1. `cci flow run dev_org --org dev_namespaced`, then open Experience Builder for
   **Volunteer Portal**.
2. Assign the packaged pages to their routes, set the theme, and save.
3. Capture it. This folder is **metadata format** (it has its own `package.xml`), so
   retrieve with `--target-metadata-dir`, not `--output-dir`. `create_community` adds a
   numeric suffix to the site developer name, so confirm it first:
   ```
   sf data query -q "SELECT Id, Name, UrlPathPrefix FROM Site WHERE Name LIKE 'Volunteer%'"
   sf project retrieve start --metadata "ExperienceBundle:Volunteer_Portal1" \
       --target-org <alias> --target-metadata-dir scratch-org/site --unzip
   ```
4. Add `ExperienceBundle` to `package.xml` and commit `scratch-org/site/experiences/**`.

`.forceignore` blanket-ignores `**/networks/**` and `**/sites/**`, and an ignored path is
skipped silently by every sf CLI operation, not just source tracking. The
`!scratch-org/site/**` negation at the bottom of `.forceignore` is what lets a captured
bundle deploy at all - do not remove it.

## The guest sharing rule

`sharingRules/Campaign.sharingRules` shares active Campaigns to the site's guest user.
It is load-bearing: Volunteer Job is master-detail to Campaign and Shift is master-detail
to Job, so without it the Job Finder shows a guest an empty list. Verified in
`dev_namespaced`: all 5 demo campaigns get a `GuestRule` share row.

Two details cost an hour each, so they are worth stating plainly:

- The element is **`sharingGuestRules`**, not `sharingCriteriaRules`. The API rejects
  `guestUser` inside a criteria rule.
- `<guestUser>` takes the guest user's **CommunityNickname** (`Volunteer_Portal`), not
  the site developer name (`Volunteer_Portal1`). The nickname derives from the site name,
  so this file is portable across scratch orgs even though the site name is not.

**Before widening it, read `documents/security/campaign-sharing-guest-pii-summary.md`.**
Opening Campaign to guests cascades to Campaign Member mirror PII under the default
"Controlled by Campaign" org-wide setting. The guest setup script deletes Campaign Members
on volunteer campaigns for exactly this reason.
