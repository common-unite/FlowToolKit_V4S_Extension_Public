# Form Templates for volunteers

The volunteer application is a Flow Tool Kit **Form Template**. Everything you can do with a Form Template (pages and sections, conditional pages, prefill, save and resume, confirmation pages and emails) works here. This page covers what the V4S Extension adds; the Flow Tool Kit [Form Template overview](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/form-template-framework/overview.md) covers the rest.

## The two packaged templates

The post-install configuration creates **Volunteer Application** and **Volunteer Group Application**; see [Volunteer sign-up form](../features/signup-form.md) for their pages. Use them as they are, edit them, or clone one as the starting point for your own.

> Running the post-install configuration again reloads these templates and overwrites your edits. Clone a template before customizing it if you might re-run the configuration.

## Jobs and shifts as Form Template Sources

The package registers **Volunteer Job** and **Volunteer Shift** as [Form Template Sources](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/form-template-framework/form-template-sources.md). When a template opens for a job or a shift, it reads that record, so the same template serves every job while showing each job's own:

- name and subtitle,
- theme,
- pre-fill answers,
- accepting-applications state and offline message,
- confirmation page message and confirmation email.

Each comes from the shift, then the job, then the template, as described in [Job and shift settings](job-and-shift-settings.md#how-settings-are-inherited). The **Form Prefill Mapping** field on Volunteer Job is maintained by the Pre-fill tab of the source configurator on the job's record page; edit mappings there rather than in the field.

## Shift selection in a template

A template for volunteers needs a page with the [Shift Selector](../features/shift-selector.md). Every shift picked becomes its own child Form Submission of the application, which the conversion turns into one Volunteer Hours record per shift.

## Making a template convert to Volunteer Hours

A template only creates volunteer records when it is set up for it. The packaged templates already are; for your own, set:

| Template setting | Value |
|---|---|
| Conversion Type | Volunteer Application |
| Conversion Rules | Volunteer Application |
| Conversion controller | `(Form Submission) Convert \| Process \| Form Submission (Volunteer) \| Overridable` |
| Contact mapping | `(Form Submission) Convert \| Process \| Contact Volunteer \| Overridable` |
| Account mapping (group templates) | `(Form Submission) Convert \| Process \| Account Volunteer \| Overridable` |

See [Volunteer Hours conversion](../features/volunteer-hours-conversion.md) for what each step does.

## Forms you can reuse

The post-install configuration adds forms for building volunteer templates: volunteer contact details, skills and availability, head shot, volunteer group and new volunteer group, primary contact, waiver (with or without notes), group sign-up, hours reporting, and the job detail, overview, highlight and upcoming-shift views. Add them to template sections like any other Flow Tool Kit form.
