# Adam Acquisition v6.4.2 — Personal Context Memory Backend Fix

Fixes the HTTP 500 found during Test 205. The v6.4 memory routes referenced an undefined `ADAM_STATE_DIR`. They now use the buyer-isolated installation-local `PERSONAL_CONTEXT_FILE` under `.adam_acquisition_buyer_v3/data/`. Recall also returns a JSON error instead of a Flask HTML 500 if the local store cannot be read.

Acceptance scope is unchanged: Tests 1–204 remain locked PASS; only Test 205 is re-tested.
