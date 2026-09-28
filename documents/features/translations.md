# Translations

Everything a volunteer reads can be translated, and the package ships a **Spanish** translation of all of it.

## What is translated

| Text | How it is translated |
|---|---|
| Job Finder, shift selector and Signup Form wording (headings, buttons, filters, messages, badges) | Custom labels, with Spanish included in the package |
| Filter headings and options that come from fields (Day of the Week, Time of Day, Weekday or Weekend, Type, Volunteer Types, skills and availability) | Field and picklist value translations, with Spanish included |
| Signup Form screen headings and progress steps | Flow translations, with Spanish included |
| Form Template pages, sections and form fields | Flow Tool Kit form labels; see the Flow Tool Kit guides on [field labels](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/form-configuration/themes-labels-styling.md) and [picklist option labels](https://github.com/common-unite/Flow_Tool_Kit_Public/blob/main/documents/form-configuration/picklist-option-labels.md) |
| Your records: job names, descriptions, campaign names | Not translated by Salesforce. Store a translated name in another field and point the Job Finder's **Campaign Label Field** and **Volunteer Job Label Field** at it. |

## How volunteers get their language

Salesforce shows each person the translation for their user language. On a public site that is the guest user's language, which follows the site's language settings in Experience Builder (Settings > Languages).

The labels and field labels that ship with the package show in Spanish **without** activating Spanish in Translation Workbench. For **picklist values**, and for any translation you add yourself, add the language and mark it **Active** in Setup > Translation Language Settings. Picklist translations can take several minutes to appear after you activate a language.

## Changing our wording

Your overrides of labels and field labels win over the packaged translation, including after upgrades:

- **Custom labels**: Setup > Custom Labels, open the label, **New Local Translations / Overrides**, pick the language and enter your text. The override shows in the Job Finder and the other components.
- **Field labels and picklist values**: Setup > Translation Workbench > **Override**, choose the Flow Tool Kit: V4S Extension package, the language and the component.

Two limits come from Salesforce: translations on standard objects in a package (the two Account fields) and on global value sets cannot be overridden.

## Adding a language

Add the language in Translation Workbench, mark it Active, then translate:

- the custom labels (Setup > Custom Labels, filter by the package),
- the field labels and picklist values (Translation Workbench > Override),
- the Signup Form flow (Translation Workbench, component **Flow**).

To have a language shipped in the package, open an issue on the [public repository](https://github.com/common-unite/FlowToolKit_V4S_Extension_Public/issues).

## What cannot be translated

- **Shift dates and times** in the Job Finder ("Oct 20, 2026 - Jan 21, 2027") come from text fields written by Date Time Sync, so they show in English.
- **Campaign Type and Job Type** shown as secondary text under an event or job in the filters are the stored values, not their translated labels.
