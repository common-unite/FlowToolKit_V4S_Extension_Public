# LWR Volunteer Portal (dev org LWR guest site)

Every dev org gets an LWR host for the Volunteer Job Finder, so LWR guest checks and the six-host rendering check (flowtoolkit rule 33) need no hand setup. Issue #50. Scratch-org scaffolding only: never packaged, never in the `demo_portal` plan or a client path.

| config_dev step | What it does |
| --- | --- |
| 53.2 `create_community` | Creates **LWR Volunteer Portal** at `/volunteerslwr` from Build Your Own (LWR). Skipped when it exists. |
| 53.3 `activate_lwr_volunteer_portal` | Sets the site Live and turns on guest API access (`OptionsGuestChatterEnabled`, `OptionsGuestFileAccessEnabled`). Without guest API access every guest `ui-api` call returns 401. |
| 53.4 `assert_site_lwr_payload` | Fails the flow when `package.xml` would deploy less than this folder holds. |
| 53.5 `deploy` | Deploys this folder (below). |
| 54 `deploy` of `scratch-org/site` | Guest sharing rules for both sites, including this site's guest (`LWR_Volunteer_Portal`). |
| 54.1 `setup-dev-guest-sites.apex` | Gives both guests Form_Flow_User, Form_Flow_V4S_User and Form_Flow_Guest_User. |
| 54.2 `activate_guest_save_override` | Activates the base installer's Guest Save Override flow. |
| 54.3 `publish_community` | Publishes. An LWR site serves only what its last publish bundled. |
| 55.2 `assert_site_usable` | Fails the flow unless the site is Live with guest API access, its guest holds the three permission sets, every active Form Template, prefill template and volunteer Campaign is shared to it, and the override flow is active. |

## What this folder holds

The full `DigitalExperienceBundle` of a freshly created site, retrieved and then changed in four places:

- `sfdc_cms__site`: `authenticationType` is `AUTHENTICATED_WITH_PUBLIC_ACCESS_ENABLED`, so guests can reach it. `geoBotsAllowed` is removed: a retrieve returns it, but a deploy refuses it.
- `sfdc_cms__themeLayout/scopedHeaderAndFooter`: **FlowToolKit LWR Support** is in the Theme Footer (flowtoolkit rule 41). Without it, a published page holding a form shows no sections.
- `sfdc_cms__view/home`: the **Volunteer Job Finder**, configured as on the Aura portal's Home.
- Volunteer Job object pages (`Volunteer_Job_Detail__c` plus its list and related list routes, which an object route needs before it will deploy). The finder opens a job's record page, and that page holds **Form (Template)** with Record Id `{!Route.recordId}` and Related Field Name `FlowToolKit__Form_Template__c`, so a guest opens the job's form.

Route types use the key prefix `a03` (V4S Volunteer Job, the same in every org).

`tasks/tests/test_dev_guest_sites.py` fails if any of these four changes is reverted.

## Changing it

Edit in Experience Builder on a dev org, publish, then retrieve over this folder and put the four changes back if Builder dropped them:

```
sf project retrieve start --metadata "DigitalExperienceBundle:site/LWR_Volunteer_Portal1" \
    --target-org <alias> --target-metadata-dir <tmp> --unzip
```

Copy `digitalExperiences/` from the retrieve over this folder, drop `geoBotsAllowed` again, and run the test above.
