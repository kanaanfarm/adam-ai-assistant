# Adam Acquisition v8.2.0.7 — Cloudflared STDERR Compatibility Fix

- Fixes Windows PowerShell 5.1 treating normal `cloudflared` INFO output on STDERR as a terminating `NativeCommandError`.
- Starts cloudflared with `Start-Process` and redirects stdout/stderr to log files instead of piping native STDERR through a `Stop` error pipeline.
- Polls both tunnel logs for the generated `https://*.trycloudflare.com` address for up to 45 seconds.
- Writes the trusted HTTPS address only after it is actually detected.
- Shows the final tunnel output when startup fails, so Guest Voice no longer reports a misleading generic tunnel failure.
- Keeps the owner UI on `http://127.0.0.1:8770` and the isolated Guest Voice gateway on `127.0.0.1:8771`.
