"""Ports the base package's Volunteer Opportunity demo build (cUnite_FormBuilder
scratch-org/showcase/build_volunteer_page.py) onto the extension testing site's
Job Detail (Design Blocks) variation view (#12), record-driven: every block binds
recordId to the page's Volunteer Job and renders {{Field}} tokens, traversing the
Role (cUnite_Volunteer_Role__r), venue (cUnite_Location__r), and Campaign lookups.
Art ships in the VolunteerOpportunityArt static resource, deployed to the org.
Re-running replaces the page content wholesale."""

import json, uuid
# Motion stripped: entrance animations strand first-paint content invisible on this
# site until the visitor scrolls, so blocks render statically instead.
def apply_motion(props, index):
    for key in ('entrance', 'hover', 'countUp', 'shine'):
        props.pop(key, None)
    return props

VIEW = "scratch-org/showcase/experiences/testing1/views/volunteerJobDesignBlocks.json"
ART = "resource:VolunteerOpportunityArt"

NAVY = "#032D60"
NAVY_GLOW = "#155091"
GREEN = "#53B95B"
GREEN_DEEP = "#2E844A"
GREEN_TINT = "#F3FAF4"
GOLD = "#F4BE45"
GRAY = "#EEF1F4"

ROLE = "FlowToolKit__cUnite_Volunteer_Role__r"
VENUE = "FlowToolKit__cUnite_Location__r"
CAMPAIGN = "GW_Volunteers__Campaign__r"

_motion_index = [0]


def block(props):
    apply_motion(props, _motion_index[0])
    _motion_index[0] += 1
    return {
        "componentAttributes": {
            "properties": json.dumps(props),
            "recordId": "{!recordId}"
        },
        "componentName": "FlowToolKit:siteDesignBlock",
        "id": str(uuid.uuid4()),
        "renderPriority": "NEUTRAL",
        "renditionMap": {},
        "type": "component"
    }


def section(columns):
    """columns: list of (width, [components]). Returns a forceCommunity:section."""
    section_id = str(uuid.uuid4())
    column_configs, regions = [], []
    for index, (width, components) in enumerate(columns):
        column_id = str(uuid.uuid4())
        column_configs.append({
            "UUID": column_id,
            "columnKey": str(index + 1),
            "columnName": f"Column {index + 1}",
            "columnWidth": str(width),
            "seedComponents": []
        })
        regions.append({
            "components": components,
            "id": column_id,
            "regionLabel": f"Column {index + 1}",
            "regionName": str(index + 1),
            "renditionMap": {},
            "type": "region"
        })
    return {
        "componentAttributes": {
            "background": "background: rgba(0,0,0,0)",
            "backgroundOverlay": "rgba(0,0,0,0.5)",
            "contentAreaWidth": 100,
            "sectionConfig": {"UUID": section_id, "columns": column_configs},
            "sectionHeight": 300
        },
        "componentName": "forceCommunity:section",
        "id": section_id,
        "regions": regions,
        "renderPriority": "NEUTRAL",
        "renditionMap": {},
        "type": "component"
    }


# ── 1. Hero: the Job itself ───────────────────────────────────────────
hero = block({
    "sectionType": "hero", "width": "full",
    "background": NAVY, "backgroundAccentColor": NAVY_GLOW, "backgroundGradient": "horizontal",
    "brandColor": GREEN, "imageFloat": True,
    "badgePosition": "top", "badgeAlign": "left",
    "badges": json.dumps([
        {"title": "Part of {{" + CAMPAIGN + ".Name}}", "style": "accent"},
        {"title": "{{" + ROLE + ".FlowToolKit__Category__c}}", "style": "neutral"},
        {"title": "{{GW_Volunteers__Number_of_Volunteers_Still_Needed__c}} spots left", "style": "outline", "pulse": True}]),
    "heading": "{{Name}}",
    "subheading": "{{GW_Volunteers__Description__c}}",
    "buttons": json.dumps([
        {"label": "Sign up for this shift", "url": "#", "style": "accent"},
        {"label": "Sign up a group", "url": "#", "style": "outline"}]),
    "footnote": "Free · Ages {{" + ROLE + ".FlowToolKit__Minimum_Age__c}} and up · Service hours letter provided on request",
    "footnoteAlign": "left",
    "imageSource": "url", "imageUrl": f"{ART}/m-delight-check-clean.png",
    "imageAlt": "Volunteer mascot with a completed signup sheet",
    "imageStyle": "mascot", "imageBleed": "bottom", "splitRatio": "left"
})

# ── 2. Key details strip: Job schedule + venue + capacity ─────────────
details = block({
    "sectionType": "statsBar", "width": "full",
    "background": NAVY, "backgroundGradient": "off",
    "accentColor": "#8EE39A",
    "overlapTop": True, "overlapMargin": 24,
    "borderTop": True, "borderWidth": 1, "borderColor": "#FFFFFF", "borderColorOpacity": 14,
    "statCards": False, "statOrder": "label", "statLayout": "inline", "iconStyle": "tile",
    "statDistribution": "spread", "paddingTop": "x-small", "paddingBottom": "x-small",
    "bodyAlign": "left",
    "items": json.dumps([
        {"title": "Setting", "value": "{{" + ROLE + ".FlowToolKit__Indoor_Outdoor__c}} work", "iconType": "image", "iconImage": f"{ART}/icon-waitlist-timer.png"},
        {"title": "Commitment", "value": "{{" + ROLE + ".FlowToolKit__Typical_Time_Commitment__c}}", "iconType": "image", "iconImage": f"{ART}/icon-settings-sliders.png"},
        {"title": "Location", "value": "{{FlowToolKit__cUnite_Location_Name__c}}", "iconType": "image", "iconImage": f"{ART}/icon-search-data.png"},
        {"title": "Spots open", "value": "{{GW_Volunteers__Number_of_Volunteers_Still_Needed__c}} across {{GW_Volunteers__Number_of_Shifts__c}} shifts", "iconType": "image", "iconImage": f"{ART}/icon-user-admin.png"}])
})

# ── 3. Your role: what to wear / what we provide / accommodations ────
roles = block({
    "sectionType": "cards", "width": "full",
    "brandColor": GREEN_DEEP,
    "sectionLabel": "Your Role",
    "heading": "{{" + ROLE + ".Name}}",
    "subheading": "{{" + ROLE + ".FlowToolKit__Physical_Requirements__c}}",
    "headingAlign": "left", "bodyAlign": "left",
    "columns": "3", "cardStyle": "outlined", "iconStyle": "plain",
    "items": json.dumps([
        {"title": "What to wear", "description": "{{" + ROLE + ".FlowToolKit__What_to_Wear__c}}",
         "iconType": "image", "iconImage": f"{ART}/icon-user.png"},
        {"title": "What we provide", "description": "{{" + ROLE + ".FlowToolKit__What_We_Provide__c}}",
         "iconType": "image", "iconImage": f"{ART}/icon-form-completion.png"},
        {"title": "Accommodations", "description": "{{" + ROLE + ".FlowToolKit__Accommodations_Available__c}}",
         "iconType": "image", "iconImage": f"{ART}/icon-scale-rocket.png",
         "backgroundColor": GREEN_TINT}])
})

# ── 4. Good to know: ages, supervision, cancellation, training ───────
schedule = block({
    "sectionType": "cards", "width": "full",
    "background": GRAY, "brandColor": GREEN_DEEP,
    "arrangement": "split",
    "sectionLabel": "Good To Know",
    "heading": "The fine print, minus the fine print.",
    "subheading": "{{" + ROLE + ".FlowToolKit__Cancellation_Policy__c}}",
    "headingAlign": "left", "bodyAlign": "left",
    "columns": "4", "cardStyle": "joined",
    "items": json.dumps([
        {"eyebrow": "Ages", "title": "{{" + ROLE + ".FlowToolKit__Minimum_Age__c}}+",
         "description": "Volunteers under {{" + ROLE + ".FlowToolKit__Adult_Supervision_Age__c}} need an adult on the same shift."},
        {"eyebrow": "Cancel", "title": "{{FlowToolKit__cUnite_Cancellation_Notice_Hours__c}} hours",
         "description": "Notice that helps us fill your spot from the waitlist."},
        {"eyebrow": "Shifts", "title": "Up to {{FlowToolKit__cUnite_Shift_Signup_Limit__c}}",
         "description": "Per signup. Pick what fits your schedule."},
        {"eyebrow": "Hours", "title": "Tracked",
         "description": "Service hours post automatically; request a signed letter any time.",
         "backgroundColor": GREEN_TINT}])
})

# ── 5. Skills: required and preferred, from the Role ─────────────────
skills_left = block({
    "sectionType": "pills",
    "brandColor": GREEN,
    "sectionLabel": "Skills and Requirements",
    "heading": "No experience required. Bring what you have.",
    "subheading": "{{" + ROLE + ".FlowToolKit__Requirements__c}}",
    "headingAlign": "left", "bodyAlign": "left",
    "items": json.dumps([
        {"title": "Needed: {{" + ROLE + ".FlowToolKit__Skills_Needed__c}}", "style": "neutral"},
        {"title": "A plus: {{" + ROLE + ".FlowToolKit__Preferred_Skills__c}}", "style": "neutral"},
        {"title": "{{" + ROLE + ".FlowToolKit__Indoor_Outdoor__c}} work", "style": "neutral"},
        {"title": "{{" + ROLE + ".FlowToolKit__Typical_Time_Commitment__c}}", "style": "neutral"}])
})

skills_right = block({
    "sectionType": "cards",
    "brandColor": GREEN_DEEP,
    "bodyAlign": "left",
    "columns": "2", "cardStyle": "outlined",
    "items": json.dumps([
        {"title": "Physical demands", "description": "{{" + ROLE + ".FlowToolKit__Physical_Requirements__c}}"},
        {"title": "Waiver", "description": "{{" + ROLE + ".FlowToolKit__Waiver_Language__c}}"},
        {"title": "Accommodations", "description": "{{" + ROLE + ".FlowToolKit__Accommodations_Available__c}}"},
        {"title": "Questions", "description": "{{" + ROLE + ".FlowToolKit__FAQ__c}}",
         "backgroundColor": GREEN_TINT}])
})

# ── 6. Location: the venue Account ───────────────────────────────────
location = block({
    "sectionType": "showcase", "width": "full",
    "background": GRAY, "brandColor": NAVY,
    "sectionLabel": "Where To Go",
    "headingAlign": "left", "bodyAlign": "left", "buttonAlign": "left",
    "blockTitle": "{{FlowToolKit__cUnite_Location_Name__c}}",
    "description": "{{GW_Volunteers__Location_Street__c}}<br>{{" + VENUE + ".FlowToolKit__cUnite_Entrance_Instructions__c}}<br>{{GW_Volunteers__Location_City__c}}, {{GW_Volunteers__Location__c}} {{GW_Volunteers__Location_Zip_Postal_Code__c}}",
    "showcaseItems": "cards",
    "items": json.dumps([
        {"title": "Parking", "description": "{{" + VENUE + ".FlowToolKit__cUnite_Parking_Instructions__c}}"},
        {"title": "Transit", "description": "{{" + VENUE + ".FlowToolKit__cUnite_Transit_Instructions__c}}"},
        {"title": "Accessibility", "description": "{{" + VENUE + ".FlowToolKit__cUnite_Accessibility_Info__c}}"}]),
    "buttons": json.dumps([
        {"label": "Get directions", "url": "#", "style": "brand"},
        {"label": "Add to calendar", "url": "#", "style": "outline"}]),
    "reversed": True,
    "imageSource": "url", "imageUrl": f"{ART}/location-placeholder.svg",
    "imageAlt": "Map of the volunteer location entrance",
    "imageStyle": "clean"
})

# ── 7. Campaign band: parent Campaign with dynamic labels ────────────
campaign = block({
    "sectionType": "showcase", "width": "full",
    "background": NAVY, "backgroundAccentColor": NAVY_GLOW, "backgroundGradient": "horizontal",
    "brandColor": GREEN,
    "overlapTop": True, "overlapMargin": 24,
    "sectionLabel": "This Shift Is Part Of",
    "headingAlign": "left", "bodyAlign": "left", "buttonAlign": "left",
    "blockTitle": "{{" + CAMPAIGN + ".Name}}",
    "description": "{{" + CAMPAIGN + ".FlowToolKit__cUnite_Excerpt__c}}",
    "stats": json.dumps([
        {"value": "3,180", "title": "{{" + CAMPAIGN + ".FlowToolKit__cUnite_Impact_Metric_1_Label__c}}"},
        {"value": "742", "title": "{{" + CAMPAIGN + ".FlowToolKit__cUnite_Impact_Metric_2_Label__c}}"},
        {"value": "6", "title": "{{" + CAMPAIGN + ".FlowToolKit__cUnite_Impact_Metric_3_Label__c}}"}]),
    "buttons": json.dumps([
        {"label": "See all opportunities", "url": "#", "style": "accent"},
        {"label": "Follow the campaign", "url": "#", "style": "outline"}]),
    "reversed": True,
    "imageSource": "url", "imageUrl": f"{ART}/m-roadmap-clean.png",
    "imageAlt": "Mascot presenting the campaign roadmap",
    "imageStyle": "mascot", "imageBleed": "bottom"
})

# ── 8. Testimonial: from the Role ────────────────────────────────────
testimonial = block({
    "sectionType": "callout", "width": "full",
    "background": GRAY, "brandColor": GREEN_DEEP,
    "overlapTop": True, "overlapMargin": 24,
    "borderTop": True, "borderWidth": 4, "borderColor": GOLD,
    "subheading": "{{" + ROLE + ".FlowToolKit__Testimonial_Quote__c}}",
    "footnote": "{{" + ROLE + ".FlowToolKit__Testimonial_Attribution__c}}"
})

# ── 9. Final CTA ─────────────────────────────────────────────────────
cta = block({
    "sectionType": "cta", "width": "full",
    "background": "#1D305E", "backgroundMidColor": "#2B525C", "backgroundAccentColor": "#57BA59",
    "backgroundGradient": "horizontal",
    "brandColor": NAVY,
    "overlapTop": True, "overlapMargin": 24,
    "arrangement": "split",
    "headingAlign": "left", "bodyAlign": "left",
    "heading": "{{GW_Volunteers__Number_of_Volunteers_Still_Needed__c}} spots left for {{Name}}.",
    "subheading": "{{FlowToolKit__cUnite_Subtitle__c}}",
    "buttons": json.dumps([
        {"label": "Sign up for this shift", "url": "#", "style": "brand"},
        {"label": "Sign up a group", "url": "#", "style": "outline"}])
})

# ── 10. Cross-sell: the three Related Jobs ───────────────────────────
questions = block({
    "sectionType": "cards", "width": "full",
    "brandColor": GREEN_DEEP,
    "sectionLabel": "You Might Also Like",
    "headingAlign": "left", "bodyAlign": "left",
    "columns": "3", "cardStyle": "clean",
    "items": json.dumps([
        {"title": "{{FlowToolKit__cUnite_Related_Job_1__r.Name}}", "description": "{{FlowToolKit__cUnite_Related_Job_1__r.FlowToolKit__cUnite_Subtitle__c}}"},
        {"title": "{{FlowToolKit__cUnite_Related_Job_2__r.Name}}", "description": "{{FlowToolKit__cUnite_Related_Job_2__r.FlowToolKit__cUnite_Subtitle__c}}"},
        {"title": "{{FlowToolKit__cUnite_Related_Job_3__r.Name}}", "description": "{{FlowToolKit__cUnite_Related_Job_3__r.FlowToolKit__cUnite_Subtitle__c}}"}])
})

content = [
    section([(12, [hero, details, roles, schedule])]),
    section([(6, [skills_left]), (6, [skills_right])]),
    section([(12, [location, campaign, testimonial, cta, questions])])
]

doc = json.load(open(VIEW))
for region in doc["regions"]:
    if region["regionName"] == "content":
        region["components"] = content
        print(f"wrote {sum(len(c['regions']) for c in content)} regions across {len(content)} sections to the variation page")
json.dump(doc, open(VIEW, "w"), indent=2)
