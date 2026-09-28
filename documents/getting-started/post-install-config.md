# Post-install configuration

A managed package cannot ship everything a working volunteer program needs. The post-install configuration adds the rest. `cci flow run post_install_config` runs these steps in order; if you apply them by hand, follow the same order.

| # | Step | What it adds |
|---|---|---|
| 1 | Volunteer Role and volunteer fields (`force-app-unpackaged-objects`) | The **Volunteer Role** object, extra fields on Volunteer Job, Shift, Hours, Campaign, Account and Lead, and the Form Object definitions the volunteer forms are built on. |
| 2 | Form Themes (`force-app-unpackaged-themes`) | Two Form Themes that style the volunteer forms. |
| 3 | Site images (`force-app-unpackaged-contentAssets`) | The banner and illustration images the forms and portal pages display. |
| 4 | Volunteer forms (`force-app-unpackaged-forms`) | The form definitions: job details, upcoming shifts, registration, waiver, group sign-up, skills and availability, hours reporting. |
| 5 | Shift date and time sync (`force-app-unpackaged-datetime-sync`) | Date Time Sync configuration and a trigger that keep each shift's start and end Date/Time in step with its separate date and time fields. |
| 6 | Page layouts (`force-app-unpackaged-layouts`) | Layouts for Volunteer Job, Shift, Hours and Volunteer Role with the extension's fields placed. |
| 7 | App, record pages and permission sets (`force-app-unpackaged-post`) | The **Volunteers** Lightning app, record pages for Job, Shift and Hours, the Form Template Sources that let a Form Template read a Volunteer Job or Shift, and the two V4S permission sets. |
| 8 | Admin access | Grants the System Administrator profile access to everything deployed above. Without it the Form Template Sources drop out of queries and the templates loaded in step 11 come up incomplete. |
| 9 | Conversion type and rule | Adds **Volunteer Application** to Flow Tool Kit's Conversion Type picklist and to the Conversion Rules picklist, and maps the rule to the type (Conversion Rules is a dependent picklist). All four volunteer conversion flows check for this rule before they run. |
| 10 | Conversion flows | Registers the volunteer controller flow, the volunteer Contact mapping and the volunteer group Account mapping so they can be selected on a Form Template. |
| 11 | Volunteer Application Form Templates | Creates **Volunteer Application** (Volunteer Information, Select Shifts, Sign Waiver) and **Volunteer Group Application** (Group Details, Select Shifts, Waiver). |
| 12 | Template clean-up | Removes the empty page and section Flow Tool Kit adds to every new template, which would otherwise render as a blank first page. |
| 13 | Permission sets for you | Assigns Form (Builder Admin), Form (Flow User), Form (Flow V4S Admin) and Form (Flow V4S User) to the user running the configuration. Other users are assigned in Setup; see [Permissions and guest access](../configuration/permissions-and-guest-access.md). |

## The Volunteer Role object

A Volunteer Role describes a kind of volunteer work once, so many jobs can share it: category, description and excerpt, minimum age and adult-supervision age, background check and training requirements, what to wear and what you provide, waiver language, FAQ, a testimonial, indoor or outdoor, remote, skills, accommodations, whether a service-hours letter is available, an icon, a banner image and whether the role is active. Each Volunteer Job can point at a Role.

## Fields added to V4S objects

- **Volunteer Job**: waitlisting and a waitlist limit, application start and end dates, cancellation notice hours, the Volunteer Role, up to three related jobs, a primary contact and on-site phone, the next shift, a sign-up link, an "open to groups" badge, the campaign event name and URL, a banner URL, an excerpt and a remote flag.
- **Volunteer Shift**: application start and end dates, Featured, Hold, Status, a sign-up link, a time zone, and three **Portal Shift Selector** fields (Label, Class, Disabled) that control how the shift appears in the [Shift Selector](../features/shift-selector.md).
- **Volunteer Hours**: e-signature, signature date and time zone.
- **Campaign**: banner, excerpt and up to three impact metric labels.
- **Account**: accessibility, entrance, parking and transit instructions, and a photo URL, for the locations volunteers travel to.
- **Lead**: age, birthdate, relationship and e-signature.

The managed package itself adds the job and shift settings described in [Job and shift settings](../configuration/job-and-shift-settings.md).

## Sample data and a demo site

The public repository also carries sample volunteers, jobs and shifts and a captured demo volunteer portal, used for demos and evaluation. They are separate from the configuration above and never needed in a production org.
