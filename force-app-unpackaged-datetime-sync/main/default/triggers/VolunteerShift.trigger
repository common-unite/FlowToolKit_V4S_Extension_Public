/**
 * Created by robertwright on 2/4/23.
 * Common-Unite
 * Use to calculate datetime on Shift records
 */

trigger VolunteerShift on GW_Volunteers__Volunteer_Shift__c (before insert, before update) {
    cUnite.CombineDateTime.process(Trigger.new,Trigger.old,GW_Volunteers__Volunteer_Shift__c.getSObjectType().getDescribe());
}