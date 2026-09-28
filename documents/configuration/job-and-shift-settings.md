# Job and shift settings

The package adds fields to Volunteer Job and Volunteer Shift that control how each opportunity is presented and how its application behaves. Most are optional: blank means "use the default".

## How settings are inherited

**Form Template defaults, then the job, then the shift.** A setting left blank on a shift falls back to its job; a setting left blank on a job falls back to the job's Form Template. So you set a program-wide default once on the template, adjust it for one job, and adjust it again for one shift only when you need to.

Formula fields on Volunteer Shift marked **(Effective)** or **(Synced)** show the value that actually applies after inheritance. They are read-only; set the job or shift field instead.

## Job settings

| Field | What it does |
|---|---|
| Form Template | The application form for this job, for example **Volunteer Application** or **Volunteer Group Application**. |
| Accepting Applications | Uncheck to stop new sign-ups for this job and all its shifts. |
| Offline Message | Shown instead of the form while the job is not accepting applications. Blank uses the Form Template's offline message. |
| Confirmation Page Message | Shown on the confirmation page after a volunteer submits. Copied to every shift that has no message of its own, and kept in step when you change it. |
| Email Template Name (Confirmation) | The developer name of the Email Template sent when an application for this job is submitted. |
| Shift Signup Limit | How many shifts one application can include. Blank or 0 means five. |
| Subtitle | The subtitle on this job's form. Blank uses the Form Template's. |
| Form Theme (ApiName) | A Form Theme to restyle this job's form. Blank uses the Form Template's theme. See [themes and styling](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/form-configuration/themes-labels-styling.md). |
| Pre-fill Template (Override) | A Pre-fill Template submission with default answers for this job's form. Blank uses the Form Template's. See [prefill templates](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/form-template-framework/prefill-templates.md). |
| Featured | Shows the job in the Job Finder's **Featured** carousel. |
| Banner Image | The image shown with the job. |
| Location | The Account where the work happens. Check **Volunteer Location** on that Account. |
| Type, Volunteer Types | Categories volunteers can filter by in the Job Finder. |
| Contact, Waiver, Job Page, Hours \| Group (FormQualifiedApiName) | Advanced: the API name of a Flow Tool Kit form to use instead of the default one for that part of this job's forms, for example a waiver with different legal text. |

V4S's own job fields still apply: **Inactive** hides the job everywhere, **Ongoing** marks a job with no fixed shifts, **Display on Website** controls browse mode in the [Shift Selector](../features/shift-selector.md), and the **Location City / State / Zip** fields feed the Job Finder's location filters.

## Shift settings

A shift can override its job for:

| Field | What it does |
|---|---|
| Form Template | A different application form for this shift only. |
| Accepting Applications | Uncheck to close this shift only. The job's checkbox controls all shifts. |
| Confirmation Page Message | This shift's own confirmation message. Blank inherits the job's. |
| Email Template Name (Confirmation) | This shift's own confirmation email. |
| Subtitle, Form Theme (ApiName) | This shift's own form subtitle and theme. |

The post-install configuration adds more shift fields, including **Featured**, **Hold**, **Status**, application start and end dates, and the three **Portal Shift Selector** fields described in [Shift Selector](../features/shift-selector.md#tile-labels-and-disabled-shifts).

## Automatic shift fields

You do not maintain these; the package keeps them up to date:

- **End date and time** are calculated from the start and the duration whenever a shift is saved.
- **Day of the Week, Month, Year, Time of Day, Weekday or Weekend, First Shift of the Day and First Shift of the Month** are derived from the start, and power the Job Finder's filters and badges.
- The separate date and time fields stay in step with the Date/Time fields through Date Time Sync.
