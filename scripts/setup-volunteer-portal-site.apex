// Guest users cannot be given object access by profile alone here: the V4S permission sets carry it, and a guest with no permset renders an empty Job Finder (config_dev step 52, re-runnable).

String siteName = 'Volunteer Portal';

List<Network> networks = [SELECT Id, Name, Status FROM Network WHERE Name = :siteName LIMIT 1];
if(networks.isEmpty()) {
    System.debug(LoggingLevel.WARN, 'Network "' + siteName + '" not found - skipping guest setup.');
    return;
}

if(networks[0].Status != 'Live') System.debug(LoggingLevel.WARN, 'Site is ' + networks[0].Status + '. Guests are redirected to login until it is activated in Experience Builder - see scratch-org/site/README.md.');

List<Site> sites = [SELECT Id, Name, GuestUserId, UrlPathPrefix FROM Site WHERE Status = 'Active' AND GuestUserId != null];
Id guestUserId;
String siteDeveloperName;
for(Site site : sites) {
    if(!site.Name.replace(' ', '_').startsWithIgnoreCase(siteName.replace(' ', '_'))) continue;
    guestUserId = site.GuestUserId;
    siteDeveloperName = site.Name;
}

if(guestUserId == null) {
    System.debug(LoggingLevel.WARN, 'No active site with a guest user matched "' + siteName + '" - skipping guest setup.');
    return;
}

Set<String> permissionSetNames = new Set<String>{'Form_Flow_User', 'Form_Flow_V4S_User'};
Map<Id, PermissionSet> permissionSetMap = new Map<Id, PermissionSet>([SELECT Id, Name FROM PermissionSet WHERE Name IN :permissionSetNames]);

Set<Id> assignedPermissionSetIdSet = new Set<Id>();
for(PermissionSetAssignment assignment : [SELECT PermissionSetId FROM PermissionSetAssignment WHERE AssigneeId = :guestUserId])
    assignedPermissionSetIdSet.add(assignment.PermissionSetId);

List<PermissionSetAssignment> assignmentsToInsert = new List<PermissionSetAssignment>();
for(Id permissionSetId : permissionSetMap.keySet())
    if(!assignedPermissionSetIdSet.contains(permissionSetId)) assignmentsToInsert.add(new PermissionSetAssignment(AssigneeId = guestUserId, PermissionSetId = permissionSetId));

if(!assignmentsToInsert.isEmpty()) {
    List<Database.SaveResult> results = Database.insert(assignmentsToInsert, false);
    for(Integer i = 0; i < results.size(); i++)
        if(!results[i].isSuccess()) System.debug(LoggingLevel.WARN, 'Permission set assignment failed: ' + results[i].getErrors()[0].getMessage());
}

// V4S adds a CampaignMember per volunteer, and its mirror PII reaches guests through the Campaign sharing rule. See documents/security/campaign-sharing-guest-pii-summary.md
List<CampaignMember> campaignMembers = [SELECT Id FROM CampaignMember WHERE CampaignId IN (SELECT GW_Volunteers__Campaign__c FROM GW_Volunteers__Volunteer_Job__c)];
if(!campaignMembers.isEmpty()) delete campaignMembers;

System.debug('Site guest setup complete for "' + siteDeveloperName + '". Guest user: ' + guestUserId + ', permission sets assigned: ' + assignmentsToInsert.size() + ', campaign members removed: ' + campaignMembers.size());
System.debug('Remaining manual step: assign the packaged pages (Volunteer Job Finder, Volunteer Home, Job/Shift Detail) in Experience Builder, then capture the site into scratch-org/site - see its README.');
