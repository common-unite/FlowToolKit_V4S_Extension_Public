/**
 * Created by robertwright on 2/7/23.
 */

@IsTest
public class VolunteerShift_Test {
    @IsTest
    static void testBehavior() {
        /**This just needs to trigger the VolunteerShift Trigger**/
        try {
            insert new GW_Volunteers__Volunteer_Shift__c();
        } catch (Exception ex) {

        }
    }
}