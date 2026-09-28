# Volunteer sign-up form

Volunteers sign up through one of two paths. Both collect the volunteer's details, the shifts they want and a signed waiver, and both end with a Contact and Volunteer Hours in your org.

| | Volunteer Application Form Templates | Job/Shift Signup Form flow |
|---|---|---|
| Built on | Flow Tool Kit [Form Templates](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/form-template-framework/form-templates.md) | A screen flow, **Volunteer \| (Job/Shift Signup Form)** |
| Where it runs | The Volunteer Job record page and any page that hosts a Form Template | The packaged Experience Cloud Job Detail and Shift Detail pages |
| Change the questions | Edit the template's pages and sections, no Flow Builder needed | Edit the forms the flow displays |
| Saves progress, applies per-job settings | Yes: every setting in [Job and shift settings](../configuration/job-and-shift-settings.md) | Shift signup limit and job details |
| Recommended for | New setups | Sites built on the packaged pages |

## Volunteer Application Form Templates

The post-install configuration creates two templates. Point a Volunteer Job at one of them with its **Form Template** field; a shift can point at a different one.

**Volunteer Application** (individuals)

1. **Volunteer Information**: how to reach the volunteer, their availability and skills, and a mailing address.
2. **Select Shifts**: the [Shift Selector](shift-selector.md) with the job's upcoming shifts, up to the job's signup limit. Each shift picked becomes part of the one signup.
3. **Sign Volunteer Waiver**: the liability waiver, signed and dated.

**Volunteer Group Application** (groups)

1. **Group Details**: the group or organization, its mailing address, and the primary contact or volunteer coordinator.
2. **Select Shifts**: shift capacity is checked against the group's headcount.
3. **Waiver**: the liability waiver.

The template reads the job (or shift) it is about through the **Volunteer Job** and **Volunteer Shift** Form Template Sources, so the form can show the job's name, subtitle, theme and confirmation message without any configuration per job. See [Form Templates for volunteers](../configuration/form-templates.md) to change what the forms ask.

<!-- screenshot: volunteer-application-shifts.png - the Select Shifts page of the Volunteer Application template -->

When the volunteer submits, the **Form Submission** is converted into a Contact, a group Account for group applications, and Volunteer Hours. See [Volunteer Hours conversion](volunteer-hours-conversion.md).

## Job/Shift Signup Form flow

The flow the packaged Experience Cloud job and shift pages run. From a job it walks the volunteer through:

1. **Job details**, with **Register as Individual** and **Register Group** buttons. The buttons only show while the job is active and, on a shift page, while the shift is still in the future.
2. **Step 1**: the volunteer's details, or the group's details and primary contact.
3. **Step 2**: pick shifts. A job with one shift asks the volunteer to confirm it; a job with several allows up to the job's **Shift Signup Limit** (five when blank). Ongoing jobs with no shifts skip this step.
4. **Step 3**: the waiver.
5. **Confirmation**.

On submit it creates or updates the volunteer's Contact and records the signup as Volunteer Hours.

All of the flow's headings and buttons are custom labels, so they follow the site's language. See [Translations](translations.md).

## Closing and reopening sign-up

Uncheck **Accepting Applications** on a job to stop new sign-ups for it and all its shifts, or on a single shift to close just that shift. The Volunteer Application templates then show the job's **Offline Message** (or the template's own) instead of the form. See [Job and shift settings](../configuration/job-and-shift-settings.md).
