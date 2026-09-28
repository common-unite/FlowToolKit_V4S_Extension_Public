# Job Finder

The Job Finder is where volunteers browse opportunities. It lists upcoming Volunteer Jobs in sections, lets volunteers search and filter, and opens a job's details and shift calendar when they pick one.

It comes in two forms:

| Component | Where it goes | Configured with |
|---|---|---|
| **Volunteer Job Finder** | An Experience Cloud page (drag it onto the page in Experience Builder) | Its property editor in Experience Builder |
| **Form (Volunteer Jobs Finder)** | A screen in a Flow; the packaged **Volunteer \| Job Finder** flow already uses it | Its property editor in Flow Builder |

<!-- screenshot: job-finder-sections.png - search, filter panel and the Featured / Today / Upcoming sections -->

## What volunteers see

1. **Search** by job name or job Type; the search runs when the volunteer presses Enter. You can hide the search box.
2. **Filters**, in collapsible panels:
   - **Volunteer Event**: a volunteer Campaign, and Campaign Type.
   - **Location**: a location Account, then State, City and Postal Code from the job's V4S location fields.
   - **Volunteer Job**: a specific job, its Type, Volunteer Types and Skills Needed.
   - **Date and Time**: a date range, Time of Day, Weekday or Weekend, and Day of the Week.
3. **Results in sections**: **Featured** jobs in a carousel, then **Today's Opportunities**, **This Week's Opportunities**, **Ongoing Opportunities** (jobs with no fixed schedule) and **Upcoming Opportunities**.
4. **Badges** on each job summarize its shifts: the days they fall on ("Monday | Wednesday", "Monday thru Friday", "Daily" or "Ongoing") and their start times.
5. **Picking a job** opens its **Overview** and a **Dates and Shifts** tab with a calendar of its upcoming shifts.

A toast tells volunteers how many jobs match their filters, or that none do. You can turn the toasts off.

## Which jobs appear

A job appears when it is **not Inactive** and either has a shift in the **next 12 months** or is marked **Ongoing** (a V4S field for jobs with no fixed shifts). The date filters narrow that window.

When the finder shows nothing, check those two conditions first, then the viewer's access: guests on a public site need the permission sets and sharing described in [Permissions and guest access](../configuration/permissions-and-guest-access.md).

## Settings

### Experience Cloud component

| Setting | What it does |
|---|---|
| Records Source | **Default** uses the packaged query described above. **Custom Flow** gets the records from an autolaunched Flow you choose, so you decide exactly which jobs and shifts appear. |
| Job Filter Formula / Shift Filter Formula | Formulas evaluated against each job or shift to hide some of them, for example only jobs of one Type. |
| Blocks per Row | 1 to 4 job cards per row on desktop (tablets show at most two). |
| Records per Category | How many jobs each section shows. |
| Job List Form / Featured Job List Form / Custom Job Filter Form | The Flow Tool Kit forms that render a job card, a featured card and an extra filter panel. The post-install configuration provides defaults. |
| Show Search Input | Show or hide the search box. |
| Show Search Toast Messages | Show or hide the "jobs found" and "no jobs found" toasts. |
| When Clicked | Open a picked job in the same tab or a new tab. |
| Campaign Label Field / Volunteer Job Label Field | Show another field instead of the record Name, for example a translated name field. See [Translations](translations.md). |

### Flow screen component

The Flow version takes its records as inputs (collections of Volunteer Jobs, Shifts, location Accounts and Campaigns), which the **Get Volunteer Jobs, Shifts, Campaigns and Accounts** action returns. Its settings match the ones above, plus:

- **Filter Section Configuration**: which filter panels show, in which order, and whether each starts open. By default all four show and only Date and Time starts open.
- **Job Navigation Target**: open a picked job in a new tab (default) or the same one.

It returns the **Selected Volunteer Job**, the **Selected Volunteer Shifts** and their count and Ids, so the next screen of your Flow can act on the volunteer's choice.

## The Get Volunteer Jobs action

**Get Volunteer Jobs, Shifts, Campaigns and Accounts** (Flow action category "Volunteer Job(s)") runs the finder's query in any Flow. Use it to feed the Flow screen component, or as the starting point of a Custom Flow records source.
