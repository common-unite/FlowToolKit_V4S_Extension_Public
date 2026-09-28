# Flow Tool Kit: V4S Extension

Volunteer sign-up for [Volunteers for Salesforce](https://github.com/SalesforceFoundation/Volunteers-for-Salesforce) (V4S), built on the [Flow Tool Kit](https://github.com/common-unite/Flow_Tool_Kit_Public) form framework.

Volunteers find opportunities on a public Experience Cloud site or inside a Flow, pick the shifts that suit them, sign a waiver and register as an individual or a group. Your org gets the result back as V4S records: the volunteer Contact, the group Account and one Volunteer Hours record per shift, created by conversion flows you can override.

<!-- screenshot: job-finder-overview.png - the Job Finder on a portal page, list view with filters open -->

## What it adds

- **Job Finder**: upcoming volunteer opportunities grouped into Featured, Today, This Week, Ongoing and Upcoming, with search and event, location, job, date, time-of-day and day-of-week filters. Picking a job opens its overview and a calendar of its shifts. Available as a Flow screen component and as a drop-in Experience Cloud component.
- **Shift Selector**: a calendar shift picker for Form Templates, record pages and site pages. It respects shift capacity, party size and a per-job signup limit.
- **Volunteer Application forms**: two Form Templates (individual and group) that run the registration, shift selection and waiver steps.
- **Volunteer Hours conversion**: a submitted application becomes a Contact, a group Account and Volunteer Hours, without duplicates when a submission is processed again.
- **Job and shift settings**: turn applications on or off, set confirmation messages and emails, and override forms and themes per job or per shift.
- **Spanish included**: every volunteer-facing label ships with a Spanish translation, and your own overrides always take priority.

## Start here

- [Installation](getting-started/installation.md): requirements, the managed package and the post-install configuration.
- [Post-install configuration](getting-started/post-install-config.md): what each configuration step adds to your org.
- [Quickstart](getting-started/quickstart.md): from a fresh install to a volunteer signing up for a shift.

## Features

- [Job Finder](features/job-finder.md)
- [Shift Selector](features/shift-selector.md)
- [Volunteer sign-up form](features/signup-form.md)
- [Volunteer Hours conversion](features/volunteer-hours-conversion.md)
- [Translations](features/translations.md)

## Configuration

- [Job and shift settings](configuration/job-and-shift-settings.md)
- [Form Templates for volunteers](configuration/form-templates.md)
- [Permissions and guest access](configuration/permissions-and-guest-access.md)

## Integrations

- [Experience Cloud volunteer site](integrations/experience-cloud-site.md)
- [Overriding the conversion flows](integrations/overriding-conversion-flows.md)

## Built on the Flow Tool Kit

The forms, themes, Form Templates and the conversion framework come from the Flow Tool Kit base package. These pages explain what the V4S Extension adds and link to the [Flow Tool Kit documentation](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/README.md) for the framework itself.

## Release notes

Every release, with its install links, is on the [Releases](https://github.com/common-unite/FlowToolKit_V4S_Extension_Public/releases) page.
