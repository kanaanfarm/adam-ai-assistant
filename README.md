# Adam Acquisition v1.3.0

New in v0.6.9.1:
- Adam detects explicit WhatsApp sending requests from the main conversation
- Resolves the recipient from saved contacts and prepares the message with AI
- Shows the contact, number and editable message in an owner-review card
- Requires an approval checkbox and a separate Send WhatsApp Message action
- Keeps the server-side approval check, so the browser cannot bypass owner approval
- Records draft and confirmed-send events in Owner Control
- Preserves all existing contacts, WhatsApp settings, API keys and `.env`

Previously included in v0.6.6:
- Uses Voice 4 Deep Calm as the consistent base with Voice 2 Clear Professional delivery
- Stronger instructions for native Beirut/Lebanese vowels, rhythm, intonation and pauses
- Explicitly avoids formal Arabic, Gulf, Egyptian and Syrian pronunciation
- Uses one natural speaker rather than overlapping two generated voices
- Moves future updates to one stable `AdamAssistant_current` installation folder
- Removes obsolete desktop and Start-menu shortcuts during installation
- Clean port 8770 and cache v0.6.6

Previously included in v0.6.4:
- Corrected Adam's permanent voice to combine Voice 1 warmth with Voice 3 friendly energy
- Strengthened native Lebanese pronunciation, rhythm, pauses and conversational delivery
- Avoids mechanically overlaying two speakers, preserving one consistent Adam identity
- Added clear disclosure that the generated voice is AI-generated
- New clean port 8769 and cache v0.6.4
- Uninstaller now stops the running v0.6.4 server before removing the installation

Previously included in v0.6.3:
- Added server-side Windows speech generation when online character voice is unavailable
- Voice delivery no longer depends only on browser speech support
- Added source reporting for Adam character voice versus Windows fallback voice
- New clean port 8768 and cache v0.6.3

Previously included in v0.6.2:
- Added the missing `/api/tts` endpoint used by the main Assistant page
- Adam now generates MP3 speech using the saved AI Settings API key
- If online character speech is unavailable, Edge/Chrome automatically uses the device voice
- New clean port 8767 and cache v0.6.2 prevent an older page from remaining active
- Installer migrates data and `.env` from the v0.6.0/v0.6.1 installation folder

Previously included:
- Replaced the failing dynamic Voice Studio page with a self-contained page
- Voice Studio can now open independently of migrated template variables
- Audio-generation and Lebanese-preview errors stay inside the page instead of producing a server 500 screen
- Clean installation folder `AdamAssistant_v062`
- New server port 8767 avoids stuck older processes and browser service workers
- Installer automatically migrates the previous `data` folder and `.env` when available
- New v0.6.0 desktop and Start-menu shortcuts
- Fixed desktop updates leaving the previous server running in memory
- Installer stops old and new assistant ports before starting the clean v0.6.0 server
- Fixed the Voice Studio Internal Server Error
- Restored five fictional Lebanese voice profiles and MP3 generation
- Restored the Lebanese Speech Normalizer preview API
- Voice generation uses the API key stored in AI Settings without displaying it
- Windows desktop installation/update scripts with desktop and Start-menu shortcuts
- Desktop updates preserve local contacts, settings, tokens and audit data
- Installable Android/iPhone PWA with update detection
- Same-Wi-Fi mobile setup page and configurable Android server address
- Complete Android Studio WebView application project
- Phone telephone links open the device dialer; API secrets remain on the server
- Version health endpoint at `/api/version`
- Fixed the AI Settings menu page returning Not Found
- Restored Save Settings and Test Connection APIs
- Leaving the API-key field blank now safely keeps the existing saved key
- Fixed the non-clickable Owner Control menu item
- Added a central Owner Control dashboard for WhatsApp, Email, Sales, Documents, Stock and Calendar
- Added owner permission rules and recent approval activity
- Real Owner Control approval queue for every AI-generated PAPER proposal
- Individual Approve or Reject controls, with editable BUY amount
- Agent scan and Auto Monitor can never execute orders directly
- Approved proposals are revalidated against market status, exposure and position limits before submission
- Official WhatsApp Business Cloud API module
- Meta Phone Number ID / Access Token settings
- Optional WhatsApp Business Account ID
- Configurable Graph API version
- Saved-contact recognition and phone lookup
- AI WhatsApp message drafting
- Professional review screen
- Mandatory owner approval
- Final confirmation before send
- Duplicate-send protection
- Real text-message sending through Meta WhatsApp Cloud API
- Meta connection test before sending
- WhatsApp webhook verification endpoint: `/webhooks/whatsapp`
- Incoming webhook event logging to `data/whatsapp_events.jsonl`
- Safe local storage for the webhook verification token
- Corrected WhatsApp configuration-file initialization
- Corrected startup order so every Flask route is registered
- Incoming WhatsApp inbox with automatic refresh
- Optional Meta webhook signature validation using the App Secret
- Hosting-ready Gunicorn start configuration
- Restored the missing general assistant and translator API route
- Translator now uses AI provider settings saved in the application
- Translation supports English, Arabic, Lebanese Arabic, French and Spanish
- Translator menu now opens a dedicated working translation page
- Added source auto-detection, target-language selection, swap and copy controls
- Working Sales module with multilingual AI reply drafting
- Sales replies use only owner-approved facts, prices and limits
- Mandatory owner review before copying or sending
- Direct approved WhatsApp sales sending with duplicate-submit protection
- Working Documents module for letters, technical responses, reports, minutes, quotations and method statements
- Multilingual document drafting with strict preservation of references and technical facts
- Owner review, copy and Microsoft Word `.docx` download
- Alpaca Paper Trading connection, account and positions
- Live IEX quote lookup through Alpaca market data
- Owner-approved paper buy/sell orders with a strict $500 per-order limit
- Real-money trading endpoint and live Alpaca URL are hard blocked
- Paper account summary and positions now display in clear responsive tables
- Market scan with SMA 5, SMA 20, RSI 14, confidence and BUY/HOLD status
- Connected paper-agent cycle with optional owner-enabled paper execution
- Maximum $500 exposure, $100 new position and three open positions
- Automatic +5% take-profit and -3% stop-loss paper actions
- Market clock, automatic monitoring, voice alerts and Stock audit log

Existing modules retained:
- Outlook Email
- Microsoft Calendar
- Inbox Command Center
- Follow-Ups / Tasks
- Contacts

Important:
This uses the official WhatsApp Business Cloud API. It does not automate WhatsApp Web
and it does not use or store your personal WhatsApp password.

Test-number setup:
1. Start the assistant and open WhatsApp Business.
2. Enter the Meta Phone Number ID, optional WABA ID, temporary access token, and Graph API version shown in Meta.
3. Enter a long private webhook verify token of your choice and save settings.
4. Click Test Connection.
5. Send only to recipient numbers that you verified in the Meta test-number screen.

Security and limitations:
- Never put a real access token inside this ZIP or commit it to source control.
- The Meta test access token expires. Replace it locally when Meta issues a new one.
- The test number is for development and can message only approved test recipients.
- Receiving live webhooks requires a public HTTPS callback URL ending in `/webhooks/whatsapp`.
- In Meta Webhooks, subscribe the WhatsApp Business Account to the `messages` field.
- Production setup with your own number may require business verification.

Desktop installation:
1. Extract the full package.
2. Run `INSTALL_DESKTOP.bat` once.
3. Use the new **Adam Personal AI Assistant** desktop shortcut.
4. For a future version, extract it and run `UPDATE_DESKTOP.bat`; the existing `data` folder is preserved.

Phone installation:
1. Keep the desktop assistant running and connect the phone to the same Wi-Fi.
2. Open **Install on Phone** in the assistant menu.
3. For same-Wi-Fi local use, build the included Android wrapper and enter the displayed address.
4. For browser installation and reliable microphone access, deploy the assistant on HTTPS first.
5. Android Chrome then offers **Install app**; iPhone Safari offers **Add to Home Screen**.


## v0.6.9.1 Adam Main-Page Stock Watch
- Main page automatically checks the Alpaca paper portfolio and a selectable Core 10 / Broad 50 / Broad 100 stock universe, with optional custom tickers; SPY is retained as the market-regime reference.
- Shows market open/closed, BUY/HOLD/SELL advice and reasons.
- Rechecks every 5 minutes while the main page is open.
- Existing +5% take-profit and -3% stop-loss rules produce SELL advice.
- Stock questions in Adam chat now read the live paper-account/market summary.
- No trade is sent from the main dashboard. Owner approval remains required in the Stock module. Real-money trading remains blocked.


## v0.6.9.1 Stock Command Center corrections
- Fixed SPY market condition calculation using Alpaca daily bars.
- Market regime now reports BULLISH / BEARISH / MIXED where sufficient data exists.
- Portfolio Today P/L now compares account equity with Alpaca last_equity.
- Open Position P/L is shown separately from daily portfolio P/L.
- Improved HOLD / HOLD-WATCH / SELL advice around +5% take-profit and -3% stop-loss.
- Added clearer Dubai next-open/close wording.
- Added a new robust stock-command-center endpoint for the main Adam page.

## v0.7.1.6 runtime correction
- Fixed the main-page error: `name 'stock_module_ready' is not defined`.
- Restored the proven v0.6.9 `/api/stock/main-summary` integration.
- Added a second SPY daily-bars fallback for BULLISH / BEARISH / MIXED market condition.
- Kept Portfolio Today P/L and Open Position P/L labels separate.
- Added HOLD / WATCH warnings near the +5% take-profit and -3% stop-loss levels.

## v0.7.1.6 Adam Opportunities
- Added Adam Opportunities section directly on the main Assistant page.
- Ranks non-held watchlist stocks by BUY / WAIT priority.
- Shows price, confidence, RSI, SMA5, SMA20, trend and reason.
- Keeps current-position advice separate from new-buy opportunities.
- Uses the existing working Alpaca paper-trading scan.
- No automatic order execution; paper orders still require owner approval.

## v0.7.1.6 Always-visible Adam Market Scan
- Adam Opportunities now always shows the symbols Adam checked, even when there is no BUY signal.
- Shows BUY / WAIT / HOLD and the reason for each symbol.
- Includes price, confidence, RSI, SMA5, SMA20 and trend.
- Existing positions are labeled YOUR POSITION.
- SPY is labeled MARKET and shows the overall market regime.
- Corrected stale v0.6.9.1.1 text on the main page.

## v0.7.1.6 Historical Bars Fix
- Fixed Adam Opportunities returning `At least 20 price bars are required`.
- Requests 120 calendar days of Alpaca daily history with up to 100 bars.
- Validates the actual number of returned trading-day bars.
- Uses completed daily bars for RSI/SMA calculations.
- Requests the latest snapshot separately for the displayed current price.
- Keeps the existing paper-only trading and owner-approval protections.

## v0.7.1.6 Version Label Fix
- Corrected the stale v0.6.9.3 header shown on the Assistant page.
- All visible version labels now identify this build consistently as v0.7.1.6.
- Stock scanning and trading logic are unchanged from the working v0.6.9.4 engine.

## v0.7.1.6 Adam Stock Alerts
- BUY, SELL, TAKE PROFIT and STOP LOSS alerts on the main page.
- Optional browser voice alerts.
- No automatic orders; paper-only and owner approval remain unchanged.

## v0.7.1.6 Stock UI Improvement
- Enlarged the Adam Stock Command Center on desktop.
- Increased usable width for alerts and opportunities.
- Larger text and spacing for stock cards.
- Improved responsiveness for medium and small screens.
- Stock logic, alerts, Alpaca integration and paper-trading rules are unchanged.

## v0.7.1.6 Adam Main Chat Outlook Email Tool
- Adam main chat now recognizes explicit email/Outlook requests.
- Resolves saved Adam Contacts by name/alias/email.
- Can also use a directly typed recipient email address.
- Adam drafts Subject and Body but does not send automatically.
- Main chat shows an editable Outlook Email — Owner Review card.
- Owner must tick approval before Send Email is enabled.
- Sending uses the existing /api/email-send-real Outlook/Microsoft Graph path.
- Existing Outlook connection is reused; no second account connection is required.
- Stock, WhatsApp, voice and paper-trading features are unchanged.

## v0.7.1.6 Contacts Persistence Fix
- Fixed contacts being lost when a new full package is extracted.
- Contacts now use persistent Windows user storage under LOCALAPPDATA/Personal_AI_Assistant/data/contacts.json.
- First run attempts to migrate a non-empty contacts.json from the current or nearby previous application folders.
- Empty contacts.json is no longer shipped in the upgrade package.
- Unified Contacts page, Adam Email and WhatsApp contact lookup on the same persistent contact list.
- Contact requires a name plus at least one email or phone; email is no longer mandatory for WhatsApp-only contacts.
- Legacy /api/contacts updates no longer erase existing email/company/notes fields.

## v0.7.1.6 Adam Main Chat Contact Registration
- Owner can register or update contacts directly from Adam's main chat.
- Example: `Register Test A email Abo@Example.com Contact Number +00997777777`.
- Adam extracts name, email and phone, saves to the same persistent Contacts database, and verifies the save.
- Existing contact fields are preserved when only one field is updated.
- Saved contacts are immediately available to Adam's Outlook and WhatsApp tools.

## v0.7.1.6 Adam Voice Commands
- Voice commands from the main page can now auto-send to Adam after speech recognition finishes.
- Added Auto-send voice command option, enabled by default.
- Example: say `Adam, register Test A, email Abo@example.com, contact number +00997777777`.
- Adam will process the command immediately and save the contact using the persistent Contacts database.
- Adam speaks the confirmation through the existing assistant voice flow.
- Email and WhatsApp commands may be started by voice, but external sending still requires owner approval.
- Microphone button now stops the active listening session if tapped again.
- No-speech and microphone-error messages are clearer.

## v0.7.1.6 Contact Editing
- Contacts page now has Edit and Delete buttons for every saved contact.
- Edit loads the existing Name, Email, Phone, Company, Language, Aliases and Notes into the form.
- Save Changes updates the same contact; it does not create a duplicate.
- Cancel Edit returns to Add Contact mode.
- Adam can edit contacts from the main chat and through the same voice-command workflow.
- Example: `Adam, change Test A email to new@example.com`.
- Example: `Adam, change Test A phone number to +971501234567`.
- Adam reports the old value → new value after a chat/voice edit.
- Persistent contact storage introduced in v0.6.9.8 remains unchanged.

## v0.7.1.6 Main Chat + Stock Separation Fix
- Rebuilt from the last known-good v0.6.9.11 Main Assistant page.
- Preserved the original working chat DOM, IDs and JavaScript handlers.
- Text Send uses the original `send` button and `/api/chat` workflow.
- Voice uses the original `mic`, `stopMic`, `voice`, `stopVoice`, language and auto-send controls.
- Large Stock Command Center stays alive but hidden on Main so its existing JavaScript cannot break the assistant.
- Main shows only a compact market status plus important stock popup/conversation alerts.
- Dedicated `/stock` page shows the full Stock Command Center, Stock Alerts and Adam Opportunities.
- Stock page hides the assistant conversation/composer but retains supporting DOM needed by existing stock JavaScript.

## v0.7.1.6 Stock Full-Width Layout Fix
- Corrected the tiny left-column rendering visible on the dedicated Stock page.
- Rebuilt the Stock page with a clean top-level full-width workspace.
- The live `stockDash`, Stock Alerts, and Adam Opportunities nodes are moved into the new workspace after page load.
- Moving the existing nodes preserves their IDs, event handlers and stock-refresh logic.
- Removed inherited app-shell scaling/transform effects from the Stock workspace.
- Stock dashboard now supports up to 1600px desktop width with responsive metric, panel and opportunity grids.
- Main Assistant page is unchanged from the working v0.6.9.15 chat/voice implementation.

## v0.7.1.6 Intent Analyzer
- Adam now analyzes Main-page input BEFORE selecting an action module.
- Contact-management intent has priority over keywords contained inside contact data.
- `Email: person@example.com` is treated as contact data unless the owner explicitly asks Adam to send/write/draft/reply by email.
- Structured commands such as `Add to Adam contact: Name: ..., Email: ..., Mob: ..., Company: ..., Position: ...` save/update Contacts instead of opening Outlook review.
- Short conversation context is used to resolve follow-ups such as `add his number +971...` to the most recently discussed saved contact.
- Email and WhatsApp workflows now require explicit analyzed send/draft intent and still preserve owner approval.
- Stock requests are routed only after intent analysis.
- Calendar/meeting intent is recognized before action; Main page does not create invitations without review/approval.
- Added Position / Job Title support to contact records and manual Contacts page where available.
- Main text and voice use the same `/api/chat` intent analyzer.

## v0.7.1.6 Natural Contact Parser
Adam can now extract a contact name from natural wording without requiring `Name:`.
Example verified: `Adam Add to contact Eng Alex Morgan, email alex.morgan@example.invalid, number +15550000000`
→ Name: Eng Alex Morgan; synthetic email and phone extracted correctly.
Professional titles such as Eng., Engineer, Mr., Mrs., Ms., and Dr. remain part of the contact name when supplied.
The v0.6.9.17 silent intent-analysis routing remains in place.

## v0.7.1.6 Contact Matching + Real Contact Lookup
- Saved-contact matching now ignores common professional titles, punctuation and capitalization.
- Example: `Alex Morgan` matches saved `Eng Alex Morgan`.
- Natural email requests now extract the recipient name and match Adam Contacts before asking for an email address.
- Questions such as `Alex Morgan is saved in the contact why you cannot see it` now trigger a real Adam Contacts lookup instead of a generic AI reply.
- Adam returns confirmed saved contact details from its local Contacts database.
- Existing owner approval for Outlook sending remains unchanged.
- Silent intent analysis remains enabled; analysis labels are not required for the user-visible answer.

## v0.7.1.6 Contacts Route Fix
- Restored the missing `/contacts` Flask route.
- `/contacts` now renders `templates/contacts.html`.
- Preserves v0.6.9.19 contact-name matching, real contact lookup, Outlook email matching, natural contact parser, and intent analyzer.

## v0.7.1.6 Contacts API Fix
- Restored JSON API used by the Contacts page.
- GET `/api/v376/contacts` loads persistent saved contacts.
- POST creates a contact.
- PUT edits a contact.
- DELETE removes a contact.
- Keeps `/contacts` page route and v0.6.9.19 matching/email fixes.
- Contacts remain in the persistent Windows contacts store; no packaged data folder is required.

## v0.7.1.6 Outlook / Email / Contacts Recovery
- Restored `/email` and `/microsoft` pages.
- Restored `/api/email-draft`.
- Restored Microsoft device sign-in/status/config/disconnect APIs.
- Microsoft client configuration and token cache now persist in `%LOCALAPPDATA%\Personal_AI_Assistant\data`.
- Added recovery of Microsoft state from older extracted Adam versions when available.
- Added stronger second-pass recovery of saved contacts from older local Adam version folders.
- Contacts delete now returns the updated list immediately.
- Owner approval remains mandatory before real Outlook sending.

## v0.7.1.6 Letter + Email Intent Fix
- `prepare letter ... send by email to ...` is now treated as a Letter/Document request first.
- Adam prepares a complete formal letter before considering email delivery.
- When email delivery is requested, the full prepared letter is placed in the existing Outlook Owner Review.
- Nothing is sent until owner approval.
- Normal standalone email requests still use the existing email workflow.

## v0.7.1.6 Main Page Outlook Send Verification
- Main-page email now uses a dedicated verified Outlook send flow.
- Adam creates a real Outlook draft, sends that exact message, then verifies it appears in Outlook Sent Items.
- Main page no longer reports success merely because Microsoft Graph accepted the request.
- Direct Smart Email page remains on its existing working send flow.
- Owner approval remains mandatory.

## v0.7.1.6 Main Email Send Fix
- Removed the draft-first Main-page flow that caused Microsoft 403 Access Denied.
- Main-page Outlook sending now uses the same proven `outlook_send_mail()` method as the Direct Email page.
- Direct Email page remains unchanged.
- Owner approval remains mandatory before sending.

## v0.7.1.6 Main Chat Calendar & Meetings
- Main chat recognizes meeting/calendar requests before generic chat.
- Resolves attendee from persistent Adam Contacts.
- Understands today/tomorrow, common clock times, and meeting duration.
- Shows an editable Outlook Meeting Owner Review card.
- Requires explicit owner approval before creating the event or sending the invitation.
- Creates the meeting through Microsoft Outlook Calendar.
- Existing email, contacts, stock, voice, and letter workflows are preserved.

## v0.7.1.6 — Adam Intelligence & Workflow
- Persistent context for natural follow-ups such as "send it", "improve it" and "add this".
- Main Chat Inbox AI: Urgent / Need Reply / For Information / Waiting for Others.
- Persistent Follow-up Manager with AI follow-up drafting.
- Calendar conflict check before owner approval.
- Document Intelligence for PDF/DOCX/TXT/MD.
- Existing enhanced paper-only Stock Intelligence preserved.
- Existing official Meta WhatsApp owner-review workflow preserved.
- Adam Daily Brief combines Outlook inbox, open follow-ups and paper-stock headline intelligence.
- Internal intent analysis remains silent.
- Owner approval remains mandatory for email, calendar invitations and WhatsApp sending.

## v0.7.1.6 — Main Camera & Attachments
- Added Main-page Attach button with multi-file selection.
- Added Camera button using the device camera where supported.
- Added drag-and-drop directly onto Adam's composer.
- Added Ctrl+V screenshot/image paste support.
- Added attachment previews with image thumbnails and remove buttons before sending.
- Supports up to 8 files per message, 20 MB each.
- Main attachment processing supports PDF, DOCX, XLSX/XLSM, TXT, MD, CSV, LOG, PNG, JPG/JPEG, WEBP and GIF.
- Document/spreadsheet source text is incorporated into Adam's existing Main workflow.
- Images use the configured OpenAI-compatible vision-capable model when supported.
- Attachment context is saved locally for conversation continuity.
- Existing owner approvals, Outlook, Calendar, Follow-ups, Stocks, WhatsApp and Daily Brief are preserved.

## v0.7.1.6 — Unified Multilingual Adam Voice
- Lebanese Voice 2 + 4 is now the master Adam voice identity.
- English, French, Spanish and all other supported languages use the same Adam character target.
- Only pronunciation/accent changes naturally per language.
- Device speech fallback now uses fixed character pitch/rate and prefers the same voice-family provider when possible.
- Added a voice-profile API so frontend and future mobile clients can use one shared voice identity rule.
- Existing camera, drag/drop, attachments, Outlook, Calendar, Follow-ups, Stock and WhatsApp workflows are preserved.

Important limitation:
Exact identical timbre across languages depends on the connected TTS provider supporting a truly multilingual single voice. The app now enforces one Adam identity profile and consistent fallback parameters, but a provider may still use different underlying voices per language.

## v0.7.1.6 — Camera & Attachment Reliability Fix
- Camera now opens a live preview when browser/device permission allows it.
- Added Capture, Retake, Use Photo, Close, and Choose Photo Instead.
- Automatic file-picker fallback remains available when live camera is unsupported or blocked.
- Fixed attachment send to analyze the exact selected-file snapshot.
- Improved drag/drop so the browser does not navigate away when a file is dropped.
- Improved pasted screenshot filenames and MIME handling.
- Existing multilingual Adam Voice 2+4 profile and owner approvals are preserved.

## v0.7.1.6 — Camera True Orientation
- Camera preview is explicitly non-mirrored.
- Captured photo is explicitly non-mirrored.
- Right side stays on the right and left side stays on the left.
- Existing camera capture/retake/use-photo, attachments, unified voice and owner approvals are preserved.

## v0.7.1.6 — Camera Mirror Orientation
- Live camera preview is mirrored like a normal selfie/computer camera.
- Right hand appears on the right side of the screen.
- Left hand appears on the left side of the screen.
- Captured photo is mirrored the same way as the preview.
- Adam receives the same orientation the owner sees.
- Existing camera, attachments, multilingual voice, Outlook, Calendar, Stock, WhatsApp and owner approvals are preserved.

## v0.7.1.6 — Camera & Attachment Recognition Fix
- Camera orientation from v0.7.1.4 is preserved.
- Camera/photos now use a dedicated vision-capable AI model instead of assuming the normal text model can see images.
- Default vision model is gpt-4o-mini when the configured text model is not recognized as vision-capable.
- Optional local setting: AI_VISION_MODEL can select another vision-capable model supported by your configured provider.
- Image analysis errors are now shown directly instead of Adam incorrectly saying the attachment cannot be analyzed after upload.
- Main Chat is explicitly told that extracted attachment context is valid source evidence, preventing the text model from denying access to an image that was already analyzed.
- PDF/Word/Excel/text attachment extraction is preserved.

## v0.7.1.6 — GPT-5.x Camera Recognition Compatibility
- Fixed the exact GPT-5.6 vision API error shown in v0.7.1.5.
- GPT-5.x image requests now use max_completion_tokens instead of unsupported max_tokens.
- Older vision models continue using max_tokens.
- Camera mirror orientation and attachment workflows are preserved.

## v0.8.0.1 — Adam Agent Intelligence
Connected multi-step workflows combine source analysis, drafting, Outlook owner review and post-send follow-up. Consequential actions still require owner approval.

## v0.8.0.1 — Send It Memory Fix
- Fixed the failed Main-page memory test where `Send it` was delegated to general AI.
- `Send it`, `Send this`, `Email it`, and `Send the email` now deterministically reopen Outlook Owner Review for the latest draft.
- The command itself is never treated as owner approval.
- Adam attempts to recover the saved recipient from recent contact context when the revised draft does not carry recipient metadata.
- If the recipient cannot be identified safely, Adam asks for the recipient instead of claiming it cannot send email.
- Existing Outlook sending route and explicit approval checkbox are unchanged.

### Acquisition evidence pack (v1.4)
- `/api/acquisition/evidence-pack` — buyer-safe readiness/governance evidence JSON
- `/api/acquisition/evidence-pack/download` — downloadable JSON evidence artifact
- `/acquisition` — includes Buyer Evidence Pack controls

## Acquisition v1.9.0
Service Boundary Extraction moves Contacts and Follow-Up data behavior into tested `adam_core` services and adds buyer-safe extraction evidence at `/api/acquisition/service-boundaries`.

## Acquisition v2.0.0
WhatsApp configuration persistence, webhook challenge verification, webhook signature verification and incoming-message projection are now isolated in tested `adam_core.whatsapp_boundary` services. Buyer-safe evidence is available from `/api/acquisition/whatsapp-boundary`, its self-test and download route. Existing WhatsApp routes and Cloud API transport are preserved.

## Acquisition v2.1.0
Adds the Document Processing Boundary under `/api/acquisition/document-boundary`, with local tested document extraction and privacy-safe buyer evidence.

## v2.7.0 acquisition hardening
Audit event construction and persistence are extracted behind `adam_core.audit_events`, with buyer-safe evidence and a network/application-data-free self-test.
