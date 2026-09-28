# Installation

The V4S Extension is a managed package plus a set of post-install configuration that a managed package cannot carry (the Volunteer Role object, forms, page layouts, record pages, permission sets and Form Templates).

## Requirements

| Package | Minimum version |
|---|---|
| Volunteers for Salesforce | 3.127 |
| Flow Tool Kit: Form and Table Builder | 4.31.0.1 |
| Date Time Sync | 0.12.0.1 |

Newer versions of each are fine. The org also needs:

- **Digital Experiences enabled** (Setup > Digital Experiences > Settings). The package will not install without it, even if you never build a site.
- **Lightning Web Security** turned on (Setup > Session Settings > "Use Lightning Web Security for Lightning web components"). Every Flow Tool Kit component expects it, and the Job Finder slows down badly on large data sets without it.

See the Flow Tool Kit [installation guide](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/getting-started/installation.md) for the base package.

## Install the managed package

Open the [latest release](https://github.com/common-unite/FlowToolKit_V4S_Extension_Public/releases/latest). Each release lists two install links: one for sandboxes and scratch orgs, one for production and Developer Edition orgs. Install for admins only; you grant access to other users through permission sets afterwards.

## Apply the post-install configuration

The configuration lives in the `force-app-unpackaged-*` folders of the [public repository](https://github.com/common-unite/FlowToolKit_V4S_Extension_Public), authored for an org where the package is installed.

**With CumulusCI** (recommended): clone the public repository, connect your org, and run the same flow the installer uses.

```
cci org import <your-org-alias> <your-org-alias>
cci flow run post_install_config --org <your-org-alias>
```

It deploys every folder in order, grants the System Administrator profile access to the new fields, adds the Volunteer Application conversion values, loads the two Volunteer Application Form Templates and assigns you the four Form permission sets. Each step is described in [Post-install configuration](post-install-config.md).

**Without CumulusCI**: deploy the folders in this order with the Salesforce CLI, then do the remaining steps by hand as described in [Post-install configuration](post-install-config.md).

1. `force-app-unpackaged-objects`
2. `force-app-unpackaged-themes`
3. `force-app-unpackaged-contentAssets`
4. `force-app-unpackaged-forms`
5. `force-app-unpackaged-datetime-sync`
6. `force-app-unpackaged-layouts`
7. `force-app-unpackaged-post`

> Running the configuration again overwrites the shipped forms, layouts, record pages and permission sets, including any changes you made to them. To move to a newer package version, upgrade the package only.

## Upgrade

Install the new version from the [latest release](https://github.com/common-unite/FlowToolKit_V4S_Extension_Public/releases/latest), after upgrading Flow Tool Kit and Date Time Sync if the release notes ask for newer versions. Upgrading the package does not touch your post-install configuration.

## Verify

1. Open the **Volunteers** app. The Volunteer Job and Volunteer Shift record pages should show the extension's fields.
2. Check that **Volunteer Application** and **Volunteer Group Application** exist under Form Templates.
3. Run the **Volunteer | Job Finder** flow from Setup > Flows. If you have a Volunteer Job with an upcoming shift, it appears in the list.

Nothing in the list usually means no job qualifies: see [Job Finder](../features/job-finder.md#which-jobs-appear).
