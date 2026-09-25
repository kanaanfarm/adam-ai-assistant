# Adam Acquisition v8.3.4.0 — Universal Assistant + One-Task Focus

## Purpose
Physical testing showed that the strict Real Meeting Attendance pipeline can be intentionally selective, but the owner also needs a normal Adam assistant that always accepts direct owner requests, answers any topic, can prepare supported actions, remembers the current task, and does not mix unrelated subjects.

## New behavior
- Added **Adam — Universal AI Assistant** directly on the Real Meeting Attendance page.
- Universal Assistant is independent of Meeting Focus Lock, project isolation, wake-name holds, and meeting question-coverage filtering.
- Supports **text queries/orders** and **browser voice queries**.
- Uses the normal `/api/chat` intelligence/action router, so existing contacts, email/WhatsApp/calendar review, follow-ups, stock, document/letter, and general-answer behavior remain available where configured.
- Added **Current task / subject focus** and **Start New Task**. The active task keeps its own short conversation history; Start New Task clears that thread so previous subjects are not mixed into the next one.
- `/api/chat` now accepts `task_focus` + `isolate_task=true` and instructs the AI to use only relevant prior turns, switch cleanly when the owner changes topic, and avoid importing facts or assumptions from unrelated earlier subjects.
- Universal answers may be spoken automatically.
- Prepared action/review state is displayed; consequential external actions still require Adam's normal owner approval and configured connectors.

## Preserved behavior
- Real Meeting Attendance / Owner Representative remains available separately with Meeting Focus Lock and project isolation.
- No approval boundary was weakened.
- No claim of autonomous external action or autonomous Teams/Zoom joining was added.
