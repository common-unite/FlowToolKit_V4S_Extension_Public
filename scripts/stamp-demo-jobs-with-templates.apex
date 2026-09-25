// DEMO ORGS ONLY. Never run this against a client org.
//
// Points every Volunteer Job in the org at a Volunteer Application template and
// resets its prefill mapping. There is deliberately no filter, because a demo
// org's jobs all come from datasets/snowfakery_recipe.yml and all want stamping.
//
// In a real org that is destructive: it would overwrite Form_Template__c and
// blank cUnite_Form_Prefill_Mapping__c on jobs the client set up by hand.
// One client org had 21 such jobs when this was split out. See issue #26.

Map<String, Id> templateIdByNameMap = new Map<String, Id>();
for(FlowToolKit__Form_Template__c formTemplate : [SELECT Id, Name FROM FlowToolKit__Form_Template__c WHERE Name IN ('Volunteer Application', 'Volunteer Group Application')])
    templateIdByNameMap.put(formTemplate.Name, formTemplate.Id);

if(templateIdByNameMap.size() < 2) throw new IllegalArgumentException('Expected both Volunteer Application templates, found: ' + templateIdByNameMap.keySet());

String prefillMapping = '{}';
List<GW_Volunteers__Volunteer_Job__c> volunteerJobs = [SELECT Id, FlowToolKit__cUnite_Volunteer_Types__c FROM GW_Volunteers__Volunteer_Job__c];
for(GW_Volunteers__Volunteer_Job__c volunteerJob : volunteerJobs) {
    Boolean groupOnly = volunteerJob.FlowToolKit__cUnite_Volunteer_Types__c == 'Groups';
    volunteerJob.FlowToolKit__Form_Template__c = groupOnly ? templateIdByNameMap.get('Volunteer Group Application') : templateIdByNameMap.get('Volunteer Application');
    volunteerJob.FlowToolKit__cUnite_Form_Prefill_Mapping__c = prefillMapping;
}
update volunteerJobs;

System.debug('Stamped ' + volunteerJobs.size() + ' demo jobs.');
