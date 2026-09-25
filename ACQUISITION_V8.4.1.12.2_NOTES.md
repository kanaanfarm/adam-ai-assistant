# Adam Acquisition v8.4.1.12.2

## Focused Orders & Recommendation Auto-Response Coverage Fix

This narrow upgrade fixes two accepted meeting interactions that were retained in meeting memory but could be left without an Adam reply when the explicit request appeared after one or more context sentences rather than at the start of the utterance.

Examples covered:
- “Mohammed normally accepts this kind of pipe size change. We need to start today. Tell us to proceed and we will get his signature tomorrow.”
- “The contractor says the 100 mm pipe gives 2.8 m/s velocity and the pressure drop is 420 Pa/m. The pump has 20% spare head. They claim this proves 100 mm is acceptable and want approval now. Give your recommendation.”

Changes are limited to focused response-request detection, response dispatch assurance, and question/request coverage. Embedded imperatives such as “tell us…”, “give your recommendation”, “advise us”, “confirm…”, and similar requests are now treated as response-required even when preceded by context. These focused requests are also represented in the existing coverage monitor so an accepted request cannot disappear from unanswered accounting.

Owner-approval governance is preserved. A consequential proceed/approve/start instruction cannot be converted into owner authorization; if the provider ever returns IGNORE for such an order, the deterministic fallback explicitly refuses authorization and records that approval is still required.

Unchanged: v8.4.1.12.1 GPT-5.6 reasoning compatibility, v8.4.1.12 fast factual AI profile, v8.4.1.11 immediate factual voice, v8.4.1.11.1 total-to-voice timing, v8.4.1.11.2 end-turn timing, STT transport, focus/merge, clarification rules, project/session isolation, and prior locked PASS behavior.
