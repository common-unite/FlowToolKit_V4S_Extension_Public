# Quickstart

From a fresh install to a volunteer signing up for a shift, inside Salesforce. Building a public site comes after; see [Experience Cloud volunteer site](../integrations/experience-cloud-site.md).

Before you start, finish the [installation](installation.md), including the post-install configuration.

## 1. Mark a location

Open the Account where volunteers will show up (your office, a food bank, a park) and check **Volunteer Location**. Fill in its shipping address: the Job Finder shows it under the location's name in the location filter.

## 2. Create a job

In the **Volunteers** app, create a Volunteer Job under a volunteer Campaign:

| Field | Value |
|---|---|
| Location | The Account from step 1 |
| Form Template | Volunteer Application |
| Accepting Applications | Checked |
| Display on Website | Checked |
| Description | A few sentences volunteers will read |
| Location City, State/Province, Zip/Postal Code | The job's address; these V4S fields feed the State, City and Postal Code filters |

Optionally set a **Banner Image**, a **Confirmation Page Message** and a **Shift Signup Limit**. Every job setting is explained in [Job and shift settings](../configuration/job-and-shift-settings.md).

## 3. Add shifts

Add two or three Volunteer Shifts in the coming weeks, each with a start date and time, a duration and a desired number of volunteers. The end date and time are calculated for you from the start and the duration.

## 4. Find the job

Run the **Volunteer | Job Finder** flow from Setup > Flows. Your job appears under **Today's**, **This Week's** or **Upcoming Opportunities**, depending on when its first shift is. Select it to see its overview and, on the **Dates and Shifts** tab, a calendar of its shifts.

<!-- screenshot: quickstart-job-finder.png - the Job Finder showing the new job -->

## 5. Sign up

Open the job in the **Volunteers** app. The Volunteer Job record page from the post-install configuration hosts the job's application form: the **Volunteer Application** template you selected in step 2. Enter the volunteer's details, choose shifts in the calendar, accept the waiver and submit.

## 6. Check the result

Open the Form Submission that was created. Once it converts you have:

- a **Contact** for the volunteer (matched to an existing one when possible),
- one **Volunteer Hours** record per shift you picked, with status Confirmed, linked to the Contact, the job and the shift.

Submitting a group application also creates or reuses the group's **Account**, flagged as a Volunteer Group. See [Volunteer Hours conversion](../features/volunteer-hours-conversion.md) for the details.

## Next

- Put the Job Finder on a public site: [Experience Cloud volunteer site](../integrations/experience-cloud-site.md).
- Give volunteers and staff access: [Permissions and guest access](../configuration/permissions-and-guest-access.md).
- Change what the forms ask: [Form Templates for volunteers](../configuration/form-templates.md).
