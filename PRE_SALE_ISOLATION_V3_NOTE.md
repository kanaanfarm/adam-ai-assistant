# Adam Acquisition v3.6.0 — PRE-SALE ISOLATION V3

Purpose: targeted buyer-isolation repair after the V2 contact test.

- Buyer contacts use installation-local `.adam_acquisition_buyer_v3/data/contacts.json`.
- Legacy contact and Microsoft state migration is hard-disabled in this buyer distribution.
- The launcher refuses to start when port 8770 is already occupied, preventing the browser from accidentally showing an older Adam process.
- The Contacts page displays `PRE-SALE ISOLATION V3` so the tester can verify the correct process/package is running.
- Personal Adam data is not modified.
