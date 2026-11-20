# Release 0.46

Version **0.46.0.2**, released 2026-11-20. Install links are on the [release page](https://github.com/common-unite/FlowToolKit_V4S_Extension_Public/releases/tag/release/0.46.0.2).

## 🆕 New

### Set the space between job cards

{% embed url="https://vimeo.com/1245191505" %}

The Volunteer Job Finder's panel in Experience Builder has a new **Card Spacing** group in its Layout section, with three pick lists: **Above**, **Below** and **Beside**. Until now the space between job cards was fixed, and on a three-per-row grid the columns could sit far apart with no way to close them up.

Each pick list offers Default plus nine sizes, from none to xx-large (the same sizes as the Form (Dynamic Repeater) panel). Above and Below add space over and under every card. Beside adds space on the left and right of each card when cards sit side by side, so the gap between columns is twice the size you pick. Every section on the page uses the same values, and **Default** keeps the standard spacing. A page saved before the upgrade keeps exactly the spacing it has today.

The Flow version of the finder takes its card spacing from the flow's **Configure Form (Repeater)** action, under Record Spacing (Top, Bottom, Sides).

Learn more: [Job Finder](../features/job-finder.md)

## 🛠 Fixes

### Job Finder: jobs stay in date order after you filter

{% embed url="https://vimeo.com/1248707249" %}

When a visitor filters the Job Finder, for example to Monday shifts only, each job is now placed in Today's, This Week's or Upcoming Opportunities by its soonest shift that still shows, and each section lists its jobs by that shift, earliest first. Before, a filtered job kept the place and section its first shift overall gave it, so Today's Opportunities could hold a job whose next Monday shift was months away. With no filters nothing changes; Ongoing Opportunities stay in name order. Both the Experience Cloud component and the Flow version get the fix.

Learn more: [Job Finder](../features/job-finder.md)

### Job Finder: Shift Range dates now match

The date range on each job card now shows both dates in the same format. Before, a card could read "10/8/26 - Dec 31, 2026", because the two halves came from two stored text fields that Date Time Sync can format differently. The finder now builds both dates from the shifts' actual dates and times, in the visitor's language and the job's Volunteer Website Time Zone, and shows one date when both fall on the same day.

Using LWR sites? Publish your site after upgrading so it picks up the latest package code from the LWR cache. [LWR site component support](https://common-unite.gitbook.io/flow-tool-kit-or-form-and-table-builder/experience-cloud/lwr-site-component-support)

## Dependencies

| Package | Version this release was built against |
|---|---|
| Volunteers for Salesforce | 3.127.0.2 |
| Flow Tool Kit: Form and Table Builder | 5.4.0.2 |
| Date Time Sync | 0.12.0.1 |
