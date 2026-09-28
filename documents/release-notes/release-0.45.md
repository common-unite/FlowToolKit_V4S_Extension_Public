# Release 0.45

Version **0.45.0.2**, released 2026-09-28. Install links are on the [release page](https://github.com/common-unite/FlowToolKit_V4S_Extension_Public/releases/tag/release/0.45.0.2).

## 🆕 New

### Volunteer sites in Spanish (#44, #41, #21)

The whole volunteer experience now ships in **Spanish**: all 68 custom labels in the Job Finder, the Shift Selector and the sign-up flow, the extension's field labels, help text and picklist values (Day of the Week, Time of Day, Weekday or Weekend, job Type, Volunteer Types, skills and availability), the Volunteer Application record type, and the Signup Form's screen headings and progress steps. The wording was written for a nonprofit volunteer audience, in neutral Latin American Spanish with formal *usted*.

- **Day badges translate** (#21). Single and mixed-day badges on job cards ("Monday | Wednesday") now show the Day of the Week picklist labels instead of the raw values, so they follow the viewer's language like the combined badges already did.
- **Signup Form headings and buttons are custom labels** (#41). The Step 2 "Select Shifts" headings were flow text templates, which Translation Workbench cannot translate in screen flows, and the seven navigation buttons were fixed text. All ten are now custom labels, so they translate and can be reworded.

Packaged labels and field labels show in Spanish without activating Spanish in Translation Workbench. Your own overrides always win over the packaged text, including after upgrades: use **New Local Translations / Overrides** on a custom label, or Translation Workbench **Override** for field labels. For picklist values, add Spanish and mark it **Active** in Translation Language Settings.

## 🛠 Fixes

- **Job Finder no longer fails for guests who cannot read the Location or Campaign lookup** (#40). A site guest with field access to a job's Location but no read access to Accounts (or to Campaigns) got "SObject row was retrieved via SOQL without querying the requested field" and the Job Finder did not load. The finder now reads those lookups only when the query could return them, so guests see the jobs and events they are allowed to see.

## 📚 Documentation (#45)

The public repository now has a full admin guide in [`documents/`](https://github.com/common-unite/FlowToolKit_V4S_Extension_Public/blob/main/documents/README.md): installation and post-install configuration, a quickstart, the Job Finder, the Shift Selector, the sign-up form, Volunteer Hours conversion, translations, job and shift settings, permissions and guest access (including how to keep volunteers' Campaign Member details private on a public site), the Experience Cloud site, and overriding the conversion flows.

## Setup notes for administrators

1. **Load each public page once after upgrading.** The first request after a package upgrade pays a one-time server-side compile of several seconds; visiting the pages yourself means a real volunteer does not.
2. **Spanish sites**: add Spanish under Experience Builder > Settings > Languages. See [Translations](https://github.com/common-unite/FlowToolKit_V4S_Extension_Public/blob/main/documents/features/translations.md).

## Dependencies

| Package | Version this release was built against |
|---|---|
| Volunteers for Salesforce | 3.127 |
| Flow Tool Kit: Form and Table Builder | 4.42.0.3 |
| Date Time Sync | 0.12.0.1 |
