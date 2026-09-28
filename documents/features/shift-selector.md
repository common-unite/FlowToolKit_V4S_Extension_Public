# Shift Selector

The **Volunteer Shift Selector** is a calendar of upcoming shifts that a volunteer picks from. It works inside a Form Template, on Volunteer Job and Volunteer Shift record pages, on app and home pages, and on Experience Cloud pages.

<!-- screenshot: shift-selector-calendar.png - calendar with shift tiles, one selected -->

## What it shows depends on where it is

| Placement | Shifts shown | What a pick does |
|---|---|---|
| Inside a **Form Template** (the Volunteer Application forms) | The upcoming shifts of the job the form is about | Adds the shift to the application. Each picked shift becomes its own child Form Submission and, after conversion, its own Volunteer Hours record. |
| A **Volunteer Job** page | That job's upcoming shifts | Opens the shift (see Navigation Target) |
| A **Volunteer Shift** page | Just that shift | Opens the shift |
| Anywhere with no job or shift (**browse mode**) | Every upcoming shift in the next 6 months whose job is marked **Display on Website** and not Inactive, labelled with the job name | Opens the shift |

On Experience Cloud pages, bind **Record Id** to `{!recordId}` on job and shift pages, or leave it blank for browse mode.

## Capacity and party size

A shift only appears while it has room: its **Number of Volunteers Still Needed** (a V4S field) must be at least the size of the party signing up. In a group application the party size comes from the form's number-of-guests answer, so a group of six never sees a shift with four spots left. When nothing fits, the selector says so and suggests a smaller group.

## Signup limit

In a Form Template, a volunteer can pick up to the job's **Shift Signup Limit** shifts in one application. A blank or zero limit means five. Outside a Form Template, a volunteer picks one shift at a time.

## Settings

| Setting | What it does |
|---|---|
| Shift Filter Formula | Optional formula evaluated against each shift to hide some of them, for example `GW_Volunteers__Desired_Number_of_Volunteers__c > 5`. Applies in every placement. A formula with an error is ignored rather than hiding every shift. |
| Navigation Target | Outside a Form Template, where a picked shift opens: **This Window**, **New Tab** (default), or **Do not navigate** (the pick only highlights the tile). |
| Maximum Shifts | Browse mode only: how many upcoming shifts to load. Defaults to 200. |

## Tile labels and disabled shifts

Three fields on Volunteer Shift, added by the post-install configuration, change how a shift's tile looks:

| Field | Effect |
|---|---|
| Portal Shift Selector Label | Replaces the tile's text, for example "Morning crew" or "Almost full". |
| Portal Shift Selector Disabled | Shows the shift but prevents picking it. |
| Portal Shift Selector Class | A style class for the tile, for theming. |

Set them by hand, or keep them up to date with a record-triggered Flow (for example, disable shifts on Hold).
