# Overriding the conversion flows

The flows that turn a volunteer application into records are **overridable**: you can replace one with your own copy without editing the package. The general pattern is in the Flow Tool Kit guide to [overridable conversion flows](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/form-template-framework/how-to/overridable-conversion-flows.md). This page lists the volunteer flows and what to change in each.

## The volunteer conversion flows

| Flow | What it does | What to change in your copy |
|---|---|---|
| `(Form Submission) Convert \| Process \| Form Submission (Volunteer) \| Overridable` | The conversion plan: organization and Contact, saved details, Volunteer Hours, files, confirmation email. One step per pass, until the application is complete. | Rarely needed. Override it only to add or reorder conversion steps. |
| `(Form Submission) Convert \| Process \| Contact Volunteer \| Overridable` | Finds or creates the volunteer's Contact and fills in the volunteer profile. | The field mapping only. Matching, duplicate handling, saving and logging stay in the shared Contact step. |
| `(Form Submission) Convert \| Process \| Account Volunteer \| Overridable` | Finds or creates the group's Account and marks it as a Volunteer Group. | The field mapping only. |
| `(Form Submission) Convert \| Process \| Volunteer Hours \| Overridable` | Creates one Hours record per picked shift, or one for an ongoing job, with status Confirmed, without duplicates on reprocessing. | The two build steps, **Volunteer Hours (Shifts)** and **Volunteer Hours (Ongoing Job)**, to fill more Hours fields. |

## How to override one

1. In Flow Builder, open the flow and **Save As** a new flow with your own name.
2. Change only the part listed above.
3. Activate your copy.
4. On the Form Template, select your copy in place of the packaged one. The Contact and Account mappings and the controller are Form Template picklist values; register your copy's API name as a value, the way the post-install configuration registers the packaged ones.
5. Submit a test application and check the resulting records.

Package upgrades never change your copy, and your template keeps using it. Check the release notes for changes to the packaged flow you copied, in case you want them too.

## Hours in your own flows

To create Volunteer Hours from a flow of your own without double booking, run the **Volunteer Hours | Prevent Dupes** action before saving. See [Volunteer Hours conversion](../features/volunteer-hours-conversion.md#no-double-booking).
