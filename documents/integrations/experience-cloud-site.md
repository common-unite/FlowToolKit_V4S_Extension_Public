# Experience Cloud volunteer site

A public site lets volunteers find and sign up for opportunities without a Salesforce login. The package ships the pieces; you assemble the site in Experience Builder.

## What the package provides

- **Volunteer Job Finder**: an Experience Cloud component with its own property editor. See [Job Finder](../features/job-finder.md).
- **Volunteer Shift Selector**: usable on any site page. See [Shift Selector](../features/shift-selector.md).
- **Page templates** for a Home page, a Job Finder page, a Job Detail page and a Shift Detail page. The Job and Shift Detail pages run the sign-up flow for the record they show.
- A **theme** and **branding set** for the volunteer site.
- The post-install configuration adds the **images** the pages use.

## Build the site

1. **Create the site**: Setup > Digital Experiences > All Sites > New, using the **Build Your Own (Aura)** template.
2. **Add the pages**: in Experience Builder, create pages from the packaged page templates, or add the **Volunteer Job Finder** component to your own page. Point the Volunteer Job and Volunteer Shift record detail routes at the Job Detail and Shift Detail pages.
3. **Configure the Job Finder**: select it on the page and set its properties, for example Blocks per Row and When Clicked.
4. **Make the pages public**: in Settings > General, allow guest users to access the site, and set each page's visibility to Public.
5. **Give guests access**: assign the permission sets to the site's guest user and share your volunteer Campaigns with a guest sharing rule. Follow [Permissions and guest access](../configuration/permissions-and-guest-access.md), including the step that keeps volunteer details private.
6. **Publish and activate** the site, then open it in a private browser window to test as a guest.

<!-- screenshot: site-job-finder-guest.png - the Job Finder on a published site, as a guest -->

## Languages

To offer the site in Spanish, add Spanish in Experience Builder (Settings > Languages). The package's Spanish translation covers the Job Finder, the shift selector and the sign-up flow. See [Translations](../features/translations.md) for what you translate yourself.

## Performance

Keep **Lightning Web Security** on (Setup > Session Settings). Without it, the Job Finder slows down sharply as the number of jobs and shifts grows.

## Demo portal

For demos and evaluation, the [public repository](https://github.com/common-unite/FlowToolKit_V4S_Extension_Public) includes sample volunteers, jobs and shifts and a captured demo site (the **Volunteer Portal** at `/volunteers`), with the scripts that create, publish and open it to guests. Use it in a sandbox or scratch org, never in production: its setup points every job at a Volunteer Application template and removes Campaign Members from volunteer Campaigns.

See also the Flow Tool Kit guide to [deploying to Experience Cloud](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/deployment/deploying-to-experience-cloud.md).
