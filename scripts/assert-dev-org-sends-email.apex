// DEV ORGS ONLY (#50): no scratch org definition setting controls deliverability, so config_dev fails here when a new org can no longer send (Setup > Deliverability > All email).
Messaging.reserveSingleEmailCapacity(1);
System.debug('Email deliverability allows sending.');
