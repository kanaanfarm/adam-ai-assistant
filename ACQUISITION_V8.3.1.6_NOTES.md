# Adam Acquisition v8.3.1.6 — Clarification-First Full-Duplex Meeting Dialogue

This maintenance release strengthens Owner Representative meeting behavior after physical rehearsal testing.

## New behavior

- Adam keeps a visible **Adam reply history** for the current meeting. The latest reply remains editable, while prior replies are retained in a separate read-only history area.
- **Clear Screen** now clears only the visible transcript/input. It does not remove Adam's latest reply, reply history, or the server-side ephemeral meeting memory.
- **End Meeting / New Session** remains the explicit reset boundary for transcript memory, conversation history, reply history, language preference, and meeting state.
- Added a **speech-recognition clarity gate**. Adam must not confidently answer a garbled, substituted, contradictory, or contextually suspicious transcript. He must ask the participant to repeat or clarify.
- If the context suggests a likely intended question, Adam asks for confirmation rather than silently guessing.
- A participant's clarification is automatically routed back to Adam even when it does not repeat the wake name or contain a question mark.
- Full-duplex behavior remains enabled: while Adam speaks, participant speech is still captured and remembered. Direct questions can interrupt/yield Adam's speech and are queued so multiple questions are handled sequentially rather than lost or spoken over.
- Consequential owner boundaries remain unchanged: no approval of variations, costs, payments, purchases, contractual commitments, or date changes without a separate exact owner approval.

## Physical acceptance focus

1. Ask a deliberately unclear/misrecognized question. Adam should ask for clarification instead of answering the wrong subject.
2. Clarify without saying “Adam” again. Adam should continue the dialogue automatically.
3. Ask one question, then interrupt Adam with another direct question while he is speaking. Adam should capture the interruption, yield, and answer the queued question without losing the meeting note.
4. Click Clear Screen and verify Adam's latest reply/reply history and meeting memory are still available.
