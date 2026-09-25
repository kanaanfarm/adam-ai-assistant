# Adam Acquisition v8.2.0.2 — Secure Guest Voice / HTTPS

- Adds local HTTPS on port 8770 for same-Wi-Fi guest voice sessions.
- Generates a private Adam Local CA and a LAN certificate containing the current LAN IP as a SAN.
- Keeps the CA private key only on the Adam computer; only the public CA certificate is installed on guest devices.
- Guest Voice now reports `microphone_requires_https` separately from a missing microphone API.
- Preserves v8.2.0 advanced intelligence/research routing and v8.2.0.1 microphone fallback.

## iPhone one-time trust
1. Start Adam once so `data/local_https/adam-local-ca.crt` is generated.
2. Transfer only `adam-local-ca.crt` to the iPhone and install the profile.
3. iPhone: Settings > General > About > Certificate Trust Settings > enable full trust for Adam Acquisition Local CA.
4. Open the guest link with `https://<Adam-PC-LAN-IP>:8770/...` (not http).
5. Allow microphone permission when Safari asks.

If the PC LAN IP changes, restart Adam; the server certificate is regenerated for the new IP. The same CA remains valid/trusted.
