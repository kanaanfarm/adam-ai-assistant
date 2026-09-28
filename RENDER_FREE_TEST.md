# Adam on Render Free: temporary owner test

This is the full Adam v8.4.1.15.1 application with an owner login page.
The page includes a Show password checkbox. Every route is protected, including
APIs and webhooks. Set a unique password of at least 20 characters as the
secret `ADAM_OWNER_PASSWORD`; the server refuses requests until it is set.
Browser sign-in name: `adam`.

Use a private GitHub repository containing these extracted files. Do not add
your existing `data`, `.env`, tokens, API keys, or passwords to GitHub. Connect
the repository in Render as a new Web Service using `render.yaml`, Free plan.
Enter `ADAM_OWNER_PASSWORD` in Render's environment settings, not in a file.
Render provides the HTTPS web address after a successful deployment.

This is for temporary testing. Render Free spins down when idle and its file
system is ephemeral. Adam's saved contacts, tokens, settings, memory, stock
config and logs can disappear after a restart, redeploy or sleep. Do not enter
real credentials or rely on stored decisions or meeting records in this test.
The separate Windows Guest Voice gateway and tunnel are not launched by this
web service; their functionality is not validated online.

Render's free running-hour allowance is shared with other Free services in the
same workspace. The online service may become unavailable when the allowance
is exhausted. Move to persistent storage and review authentication, webhooks,
cross-site request protection and operational monitoring before ongoing use.
