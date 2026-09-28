# Permissions and guest access

## Permission sets

The post-install configuration adds two permission sets. They work alongside the Flow Tool Kit base package's own sets; see the Flow Tool Kit [permission sets](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/getting-started/permission-sets.md) guide.

| User | Assign |
|---|---|
| Admins who configure jobs, forms, the Job Finder and conversion | **Form (Flow V4S Admin)**, plus the base **Form (Builder Admin)** |
| Staff who run the sign-up forms inside Salesforce | **Form (Flow V4S User)**, plus the base **Form (Flow User)** |
| The guest user of a public volunteer site | **Form (Flow V4S User)** and **Form (Flow User)** |

**Form (Flow V4S Admin)** covers Campaign, Contact, Volunteer Job, Shift, Hours and Volunteer Role, the package's Apex (including the property editors) and the three volunteer screen flows.

**Form (Flow V4S User)** gives what a volunteer needs to browse and sign up: read access to campaigns, jobs, shifts and roles, create access for the records a sign-up makes, the screen flows and the components' Apex. It has **no Edit** permission on purpose: the Guest User license only allows Read and Create, and a set with Edit cannot be assigned to a guest.

Permission sets grant object and field access. Which **records** someone sees still follows your org's sharing model.

## Giving a public site's guests access

A guest on your volunteer site sees jobs and shifts only if both of these are true:

1. **The guest user has the two permission sets.** In Experience Builder, open Settings > General, click the guest user profile, then the guest user, and assign **Form (Flow User)** and **Form (Flow V4S User)**.
2. **A guest sharing rule shares your volunteer Campaigns.** Volunteer Jobs and Shifts are shared through their Campaign, so create a guest user sharing rule on Campaign with Read access, for example *Active equals true*. Narrow it (a Campaign Type or record type) if you run non-volunteer campaigns you do not want public.

Test by opening the site in a private browser window.

## Keep volunteer details private

V4S adds a Campaign Member for every volunteer who signs up. With the default Campaign Member sharing ("Controlled by Campaign"), a guest sharing rule on a Campaign also shares its **Campaign Members**, and with them the volunteers' names and contact details.

Before you open the site to guests, do one of the following:

- **Remove Campaign Members from volunteer Campaigns** and keep them removed. The demo portal setup script does exactly this.
- Or set Campaign Member sharing to **Controlled by Campaign Member** (Setup > Sharing Settings), so members are no longer shared with their Campaign. In a large org this change triggers a sharing recalculation that can take a long time.

Then confirm from a private window that no volunteer's details are visible on the site.

## Related

- [Experience Cloud volunteer site](../integrations/experience-cloud-site.md): building the site itself.
- Flow Tool Kit: [Deploy to Experience Cloud](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/deployment/deploying-to-experience-cloud.md).
