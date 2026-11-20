// DEV ORGS ONLY (#50): a separate script so the demo_portal plan, which shares setup-volunteer-portal-site.apex, never gains the Guest Save Override grant.

Set<String> siteNames = new Set<String>{'Volunteer Portal', 'LWR Volunteer Portal'};
Set<String> permissionSetNames = new Set<String>{'Form_Flow_User', 'Form_Flow_V4S_User', 'Form_Flow_Guest_User'};

Map<String, Id> guestUserIdBySiteName = new Map<String, Id>();
for(Site site : [SELECT MasterLabel, GuestUserId FROM Site WHERE MasterLabel IN :siteNames AND Status = 'Active' AND GuestUserId != null])
    guestUserIdBySiteName.put(site.MasterLabel, site.GuestUserId);

for(String siteName : siteNames)
    if(!guestUserIdBySiteName.containsKey(siteName)) System.debug(LoggingLevel.WARN, 'No active site "' + siteName + '" with a guest user - skipped.');

Map<Id, PermissionSet> permissionSetMap = new Map<Id, PermissionSet>([SELECT Id, Name FROM PermissionSet WHERE Name IN :permissionSetNames]);
if(permissionSetMap.size() < permissionSetNames.size()) System.debug(LoggingLevel.WARN, 'Found only ' + permissionSetMap.size() + ' of ' + permissionSetNames + '. Form_Flow_Guest_User comes from the base installer\'s guest save override.');

Set<String> heldKeySet = new Set<String>();
for(PermissionSetAssignment assignment : [SELECT AssigneeId, PermissionSetId FROM PermissionSetAssignment WHERE AssigneeId IN :guestUserIdBySiteName.values() AND PermissionSetId IN :permissionSetMap.keySet()])
    heldKeySet.add('' + assignment.AssigneeId + assignment.PermissionSetId);

List<PermissionSetAssignment> assignmentsToInsert = new List<PermissionSetAssignment>();
for(Id guestUserId : new Set<Id>(guestUserIdBySiteName.values()))
    for(Id permissionSetId : permissionSetMap.keySet())
        if(!heldKeySet.contains('' + guestUserId + permissionSetId)) assignmentsToInsert.add(new PermissionSetAssignment(AssigneeId = guestUserId, PermissionSetId = permissionSetId));

List<Database.SaveResult> results = Database.insert(assignmentsToInsert, false);
for(Integer i = 0; i < results.size(); i++)
    if(!results[i].isSuccess()) System.debug(LoggingLevel.WARN, 'Permission set assignment failed: ' + results[i].getErrors()[0].getMessage());

System.debug('Dev guest site setup: ' + guestUserIdBySiteName.size() + ' site(s), ' + assignmentsToInsert.size() + ' permission set assignment(s) added.');
