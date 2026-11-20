"""Generate the three #61 demo confirmation emails (scratch org only, never packaged).

Run: python3 scratch-org/demo-emails/build.py   (rewrites email/unfiled$public/*)
Deploy: sf project deploy start --source-dir scratch-org/demo-emails/email -o <dev org>

The templates live in unfiled$public (Lightning templates are visible under Setup or
App Launcher > Email Templates > Public Email Templates). A named folder is not used:
Lightning (SFX) templates need a Lightning EmailTemplateFolder, which neither source nor
metadata deploys accept here, and a classic EmailFolder is rejected ("Cannot find folder").
"""
from pathlib import Path

OUT = Path(__file__).parent / "email" / "unfiled$public"
SUB = "FlowToolKit__Form_Submission__c"
# Scratch-org public asset URLs (verified 200 image/jpeg). Demo only: a real build uses {[devName:...]}.
ASSET = "https://business-customization-9444.scratch.file.force.com/file-asset-public/FlowToolKit__{}?oid=00DQL00000gDYdB2AW"
SITE = "https://business-customization-9444.scratch.my.site.com/volunteerslwrvforcesite"
BRAND, INK, MUTED, TINT = "#0b5cab", "#181818", "#5c5c5c", "#eef4ff"
FONT = "'DM Sans', Arial, Helvetica, sans-serif"


def m(field):
    return "{{{%s.FlowToolKit__%s}}}" % (SUB, field)


NAME = m("Contact1_First_Name__c") + " " + m("Contact1_Last_Name__c")

TEMPLATES = [
    dict(
        dev="Volunteer_Confirmation_Event_Shift",
        name="Volunteer Confirmation - Event Shift (Gala Setup)",
        subject="You're on the Gala setup crew, " + m("Contact1_First_Name__c") + "!",
        banner="FlowToolKit_VolunteerEventSetup",
        program="Annual Foundation Gala",
        heading="You're signed up for Event Setup",
        intro="Thank you for volunteering at the Annual Foundation Gala. We received your sign-up and saved your spot on the setup crew.",
        rows=[("Name", NAME),
              ("Email", m("Contact1_Email__c")),
              ("Phone", m("Contact1_Phone__c")),
              ("Your shift", m("Start_Date_Time__c")),
              ("Guests joining you", m("Number_of_Guests__c"))],
        next=["Arrive 15 minutes before your shift and check in at the volunteer table by the main entrance.",
              "Wear closed-toe shoes; setup includes moving tables and carrying decor.",
              "You'll get a reminder email two days before the event with parking details."],
        contact="Questions? Reply to this email or call the events team at (816) 555-0142.",
        button=("View your shift", SITE + "/"),
    ),
    dict(
        dev="Volunteer_Confirmation_Ongoing_Role",
        name="Volunteer Confirmation - Ongoing Role (Therapy Horse)",
        subject="Welcome to Equine Therapy, " + m("Contact1_First_Name__c"),
        banner="FlowToolKit_VolunteerHorseTherapy",
        program="Equine Therapy",
        heading="Your Adopt a Therapy Horse application is in",
        intro="Thank you for committing to one of our therapy horses. This is an ongoing role, so here is what we have on file and how we get you started.",
        rows=[("Name", NAME),
              ("Email", m("Contact1_Email__c")),
              ("Phone", m("Contact1_Phone__c")),
              ("Preferred start date", m("Start_Date__c")),
              ("Weekly availability", m("Volunteer_Availability__c")),
              ("Skills you shared", m("Volunteer_Skills__c"))],
        next=["Our barn coordinator will call you within 5 business days to schedule a 90-minute orientation.",
              "At orientation you'll meet your horse, learn grooming and safety basics, and sign the barn waiver.",
              "After orientation we'll set a regular weekly time based on the availability above."],
        contact="Questions? Reply to this email or call the barn coordinator at (816) 555-0177.",
        button=("See the Equine Therapy program", SITE + "/"),
    ),
    dict(
        dev="Volunteer_Confirmation_Group_Shift",
        name="Volunteer Confirmation - Group Shift (Food Sorting)",
        subject="Your group is confirmed for Weekend Food Sorting",
        banner="FlowToolKit_VolunteerFoodSort",
        program="Food Distribution and Nutrition",
        heading="Your group is booked for Weekend Food Sorting",
        intro="Thank you for bringing a team to the Food Bank. We received your group sign-up and reserved space for everyone below.",
        rows=[("Group lead", NAME),
              ("Lead email", m("Contact1_Email__c")),
              ("Company or group", m("Company__c")),
              ("Group size", m("Number_of_Guests__c")),
              ("Your shift", m("Start_Date_Time__c"))],
        next=["Forward this email to your team so everyone has the shift time and address.",
              "Each volunteer signs a short waiver on arrival; anyone under 16 needs an adult with them.",
              "Sorting runs about 4 hours. We provide gloves and aprons; please wear closed-toe shoes."],
        contact="Questions? Reply to this email or call our group coordinator at (816) 555-0123.",
        button=("View your group's shift", SITE + "/"),
    ),
]


def html(t):
    rows = "".join(
        f'<tr><td style="padding:10px 16px;color:{MUTED};font-size:14px;width:40%;border-bottom:1px solid #e5e5e5;">{k}</td>'
        f'<td style="padding:10px 16px;color:{INK};font-size:16px;font-weight:600;border-bottom:1px solid #e5e5e5;">{v}</td></tr>'
        for k, v in t["rows"])
    steps = "".join(f'<li style="margin:0 0 10px;">{s}</li>' for s in t["next"])
    label, href = t["button"]
    return f"""<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f3f3f3;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f3f3f3;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:12px;overflow:hidden;font-family:{FONT};color:{INK};">
<tr><td style="background:{BRAND};padding:14px 24px;color:#ffffff;font-size:14px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;">commonUNITE Volunteers &middot; {t["program"]}</td></tr>
<tr><td><img src="{ASSET.format(t["banner"])}" alt="{t["program"]}" width="600" style="display:block;width:100%;height:auto;max-height:260px;object-fit:cover;border:0;"></td></tr>
<tr><td style="padding:32px 32px 8px;">
<h1 style="margin:0 0 12px;font-size:26px;line-height:1.25;color:{INK};">{t["heading"]}</h1>
<p style="margin:0 0 8px;font-size:16px;line-height:1.5;">Hi {m("Contact1_First_Name__c")},</p>
<p style="margin:0 0 24px;font-size:16px;line-height:1.5;">{t["intro"]}</p>
<h2 style="margin:0 0 8px;font-size:18px;color:{BRAND};">What we received</h2>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{TINT};border-radius:8px;margin:0 0 24px;">{rows}</table>
<h2 style="margin:0 0 8px;font-size:18px;color:{BRAND};">What happens next</h2>
<ol style="margin:0 0 24px;padding-left:20px;font-size:16px;line-height:1.5;">{steps}</ol>
<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 24px;"><tr><td style="background:{BRAND};border-radius:8px;">
<a href="{href}" style="display:inline-block;padding:14px 28px;color:#ffffff;font-size:16px;font-weight:600;text-decoration:none;">{label}</a></td></tr></table>
<p style="margin:0 0 32px;font-size:16px;line-height:1.5;">{t["contact"]}</p>
</td></tr>
<tr><td style="background:#f8f8f8;padding:20px 32px;color:{MUTED};font-size:13px;line-height:1.5;border-top:1px solid #e5e5e5;">
commonUNITE Volunteer Center &middot; 1200 Main Street, Kansas City, MO 64105<br>You're receiving this because you signed up to volunteer with us.</td></tr>
</table></td></tr></table></body></html>
"""


META = """<?xml version="1.0" encoding="UTF-8"?>
<EmailTemplate xmlns="http://soap.sforce.com/2006/04/metadata">
    <available>true</available>
    <encodingKey>UTF-8</encodingKey>
    <name>{name}</name>
    <relatedEntityType>{sub}</relatedEntityType>
    <style>none</style>
    <subject>{subject}</subject>
    <type>custom</type>
    <uiType>SFX</uiType>
</EmailTemplate>
"""

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for t in TEMPLATES:
        (OUT / f'{t["dev"]}.email').write_text(html(t))
        (OUT / f'{t["dev"]}.email-meta.xml').write_text(
            META.format(name=t["name"], sub=SUB, subject=t["subject"].replace("&", "&amp;")))
    print(f"wrote {len(TEMPLATES)} templates to {OUT}")
