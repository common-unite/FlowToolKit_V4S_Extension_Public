# Volunteer Hours conversion

A submitted volunteer application is a **Form Submission**. Conversion turns it into the V4S records your program runs on: the volunteer's Contact, the group's Account and one Volunteer Hours record per shift. It uses the Flow Tool Kit [submission conversion](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/form-template-framework/submission-conversion.md) framework, with volunteer versions of three steps and one new step.

## What gets created

| Step | Result |
|---|---|
| Organization (group applications) | Finds or creates the group's Account and checks **Is Volunteer Group**, so the group can be used for volunteering from then on. |
| Contact | Finds or creates the volunteer's Contact and fills in their volunteer profile: availability, skills, the organization they volunteer with, their address and any notes. Availability and skills land in the V4S Contact fields. |
| Volunteer Hours | One Hours record for each shift the volunteer picked, or a single record for the job when the job is ongoing and has no shifts. Every record links the volunteer, the job and the shift, with status **Confirmed**. |
| Uploaded files and confirmation email | As for any Flow Tool Kit template. The confirmation email is the job's or shift's **Email Template Name (Confirmation)**; see [Job and shift settings](../configuration/job-and-shift-settings.md). |

Each picked shift is its own child Form Submission linked to the application, so the Hours for each shift can be traced back to what the volunteer submitted.

## No double booking

Reprocessing or resubmitting the same application updates the Hours records it already created instead of adding new ones. A volunteer is never booked twice for the same shift by the same application.

For your own flows, the **Volunteer Hours | Prevent Dupes** action (Flow action category "Volunteer Hours") does the same check: give it the Hours records you are about to save, and it returns them split into records to **insert**, existing matches to **update** (same volunteer and the same job or shift), and **invalid** ones (missing a required value, or duplicated within the request).

## How it is switched on

The post-install configuration sets this up; for your own templates, choose these on the Form Template:

1. **Conversion Type**: Volunteer Application.
2. **Conversion Rules**: Volunteer Application. All four volunteer conversion steps check for this rule before they run.
3. **Controller flow**: `(Form Submission) Convert | Process | Form Submission (Volunteer) | Overridable`. It is the standard controller with the Volunteer Hours step added.
4. **Contact and Account mapping**: the `Contact Volunteer` and `Account Volunteer` conversion flows.

If a template reaches the Volunteer Hours step without the Volunteer Application rule, or before the Contact exists, the Form Submission is marked with an error and nothing is saved, so a misconfigured template never creates stray Hours.

## Changing what gets filled in

Each step is an **overridable** flow. To change the field mapping (for example to fill a custom Hours field), clone the flow, change only its mapping, and select your copy on the Form Template. Matching, duplicate handling, saving and logging stay in the shared steps. See [Overriding the conversion flows](../integrations/overriding-conversion-flows.md).
