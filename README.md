# Flow Tool Kit: V4S Extension

Experience Cloud and Flow components for [Volunteers for Salesforce](https://github.com/SalesforceFoundation/Volunteers-for-Salesforce)
(V4S), built on the [Flow Tool Kit](https://github.com/common-unite/Flow_Tool_Kit_Public) form
framework. Volunteers search, filter and sign up for jobs and shifts on a public site or inside a
Flow. The org gets the registration, the application and the hours back as V4S records through
conversion flows an admin can override.

## Documentation

Release notes, with install links for every version, are on the
[Releases](https://github.com/common-unite/FlowToolKit_V4S_Extension_Public/releases) page. Guides
land in `documents/` as they are written.

## What it does

- **Volunteer Jobs Finder** (Flow screen component): list, calendar and map views over Volunteer
  Jobs and Shifts, with keyword, date, day-of-week and location filters. The selected job and
  shifts flow out to the next screen.
- **Volunteer Job Finder page** (Experience Cloud component): the same finder as a drop-in site
  page with a property editor. Records come from the packaged query or from a Flow you supply;
  job selectability, blocks per row, and search toasts are settings.
- **Volunteer Shift Selector**: a calendar shift picker for Form Templates, record pages, app
  pages and Experience Cloud. A Shift Filter Formula scopes it server-side, presentation fields on
  the Shift drive tile labels and disabled states, and a navigation target decides whether a
  picked shift opens in this window, a new tab, or not at all.
- **Registration and sign-up flows**: screen flows for job and shift sign-up, and overridable
  conversion flows that turn a Form Submission into a volunteer Contact, an Account, a Case, and
  Volunteer Hours.
- **Volunteer Hours conversion** with duplicate prevention and multi-shift sign-up.
- **Invocable actions**: Retrieve Volunteer Jobs (the finder's query, callable from any Flow) and
  Prevent Duplicate Volunteer Hours, each with its own property editor.
- **Record automation**: shift end time calculation and confirmation message sync from Job to
  Shift.
- **Translatable**: 58 custom labels cover the volunteer-facing text.

## Requirements

| Package | Version the current release was built against |
|---|---|
| Volunteers for Salesforce | 3.127 |
| Flow Tool Kit: Form and Table Builder | 4.31.0.1 |
| Date Time Sync | 0.12.0.1 |

Newer versions of each dependency are fine. The org also needs **Digital Experiences enabled**
(the package will not install without it) and **Lightning Web Security** turned on in Session
Settings, which every Flow Tool Kit component expects.

## Install

1. **Managed package**: install the current release (**0.44.0.1**):
   - Sandbox and scratch orgs: <https://test.salesforce.com/packaging/installPackage.apexp?p0=04tRQ000000AZAzYAO>
   - Production and Developer Edition: <https://login.salesforce.com/packaging/installPackage.apexp?p0=04tRQ000000AZAzYAO>
   - Always current: [latest release](https://github.com/common-unite/FlowToolKit_V4S_Extension_Public/releases/latest)
2. **Post-install configuration**: the `force-app-unpackaged-*` directories hold what a managed
   package cannot carry, authored in the shape an org with the package installed needs. Deploy
   them in this order, with the Salesforce CLI or CumulusCI. A MetaDeploy installer that runs
   these steps for you is in progress.

   | Directory | Contents |
   |---|---|
   | `force-app-unpackaged-objects` | The Volunteer Role object, `cUnite_` fields on Volunteer Job, Shift, Hours, Campaign, Account and Lead, and the Volunteer Application conversion picklist values on Form Template |
   | `force-app-unpackaged-themes` | Two Form Themes for the volunteer forms |
   | `force-app-unpackaged-contentAssets` | Images for the Volunteer Portal site |
   | `force-app-unpackaged-forms` | The Form definitions: job details, shift tables, registration, waiver, group sign-up |
   | `force-app-unpackaged-layouts` | Page layouts for the V4S objects |
   | `force-app-unpackaged-post` | The Volunteers Lightning app, record pages, the Volunteer Job and Volunteer Shift Form Template Sources, and the two permission sets |
   | `force-app-unpackaged-datetime-sync` | Date Time Sync configuration and triggers for the shift date and time fields |

## Permission sets

| Set | Grants |
|---|---|
| Form (Flow V4S Admin) | Everything an admin needs to configure the finder, the forms and the conversion flows |
| Form (Flow V4S User) | Volunteer-facing access: the screen flows, the finder and shift selector, and the Contact fields the registration form writes. Assign it to the site guest user for a public portal |

Both sets live in `force-app-unpackaged-post`. A guest user license allows Read and Create only,
so the User set carries no Edit access by design. Record access always follows the org's own
sharing model.

## This repository

The public companion to a private source repo: documentation, project configuration, and the
post-install configuration are mirrored here on every release, along with the release itself.
Issues and feature requests are welcome here.
