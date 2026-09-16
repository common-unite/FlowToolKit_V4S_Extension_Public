// Runs in EVERY org right after load_form_templates, including client production orgs.
//
// Two jobs, in this order:
//   1. delete the empty default page/section that base package triggers auto-insert
//   2. repoint each section's FormQualifiedApiName__c at the form this org actually has
//
// Order matters. Step 1 filters on the RAW namespaced default value, so it has to run
// before step 2 rewrites anything. Safe to re-run. Never touches Volunteer Jobs.
// See issues #26 and #27.

Map<String, Id> templateIdByNameMap = new Map<String, Id>();
for(FlowToolKit__Form_Template__c formTemplate : [SELECT Id, Name FROM FlowToolKit__Form_Template__c WHERE Name IN ('Volunteer Application', 'Volunteer Group Application')])
    templateIdByNameMap.put(formTemplate.Name, formTemplate.Id);

if(templateIdByNameMap.size() < 2) throw new IllegalArgumentException('Expected both Volunteer Application templates, found: ' + templateIdByNameMap.keySet());

/** 1. Remove the trigger auto-created children, which duplicate what the recipe supplies **/
List<FlowToolKit__Form_Template_Page__c> autoCreatedPages = [
    SELECT Id FROM FlowToolKit__Form_Template_Page__c
    WHERE FlowToolKit__Form_Template__c IN :templateIdByNameMap.values()
    AND FlowToolKit__Page_Label__c = 'Primary Contact Information'
];
if(!autoCreatedPages.isEmpty()) delete autoCreatedPages;

// Component_Type filter is load-bearing: FormQualifiedApiName__c defaults to Primary_Contact_Default on EVERY insert, so LWC sections carry it too
List<FlowToolKit__Form_Template_Page_Section__c> autoCreatedSections = [
    SELECT Id FROM FlowToolKit__Form_Template_Page_Section__c
    WHERE FlowToolKit__Form_Template_Page__r.FlowToolKit__Form_Template__c IN :templateIdByNameMap.values()
    AND FlowToolKit__FormQualifiedApiName__c = 'FlowToolKit__Primary_Contact_Default'
    AND FlowToolKit__Component_Type__c = 'Field Set'
];
if(!autoCreatedSections.isEmpty()) delete autoCreatedSections;

/**
 * 2. The recipe hardcodes namespaced form names because it was authored in a namespaced
 * dev org. The Form__mdt records it points at ship UNPACKAGED, so they are local: they
 * carry the org namespace in a namespaced scratch org and NO namespace in a subscriber
 * org. FormQualifiedApiName__c is free text with no validation, so a stale reference
 * saves happily and silently renders nothing.
 *
 * Resolve against what this org actually has. Local wins over packaged, because every
 * form the recipe references is one we ship in force-app-unpackaged-forms; the packaged
 * twins of Primary_Contact_Default and Form_b76cg7fi8_* come from the base package and
 * are not what our config means.
 **/
Map<String, String> qualifiedNameByDeveloperNameMap = new Map<String, String>();
for(FlowToolKit__Form__mdt form : [SELECT DeveloperName, NamespacePrefix FROM FlowToolKit__Form__mdt]) {
    Boolean isLocal = String.isBlank(form.NamespacePrefix);
    String qualifiedName = isLocal ? form.DeveloperName : form.NamespacePrefix + '__' + form.DeveloperName;
    if(isLocal || !qualifiedNameByDeveloperNameMap.containsKey(form.DeveloperName))
        qualifiedNameByDeveloperNameMap.put(form.DeveloperName, qualifiedName);
}

List<FlowToolKit__Form_Template_Page_Section__c> sectionsToRepoint = new List<FlowToolKit__Form_Template_Page_Section__c>();
List<String> unresolvedForms = new List<String>();
for(FlowToolKit__Form_Template_Page_Section__c section : [
        SELECT Id, FlowToolKit__FormQualifiedApiName__c
        FROM FlowToolKit__Form_Template_Page_Section__c
        WHERE FlowToolKit__Form_Template_Page__r.FlowToolKit__Form_Template__c IN :templateIdByNameMap.values()
        AND FlowToolKit__FormQualifiedApiName__c != NULL]) {

    String storedName = section.FlowToolKit__FormQualifiedApiName__c;
    String developerName = storedName.contains('__') ? storedName.substringAfterLast('__') : storedName;
    String resolvedName = qualifiedNameByDeveloperNameMap.get(developerName);

    if(resolvedName == null) { unresolvedForms.add(storedName); continue; }
    if(resolvedName == storedName) continue;

    section.FlowToolKit__FormQualifiedApiName__c = resolvedName;
    sectionsToRepoint.add(section);
}
if(!sectionsToRepoint.isEmpty()) update sectionsToRepoint;

if(!unresolvedForms.isEmpty())
    throw new IllegalArgumentException('No Form__mdt in this org matches: ' + unresolvedForms + '. Deploy the unpackaged forms (deploy_unpackaged_config) before loading templates.');

System.debug('Cleanup: deleted ' + autoCreatedPages.size() + ' auto pages, ' + autoCreatedSections.size() + ' auto sections; repointed ' + sectionsToRepoint.size() + ' sections.');
