# Adam Acquisition v8.1.0.3 — Long Response Voice Queue Fix

- Long guest replies are split into bounded speech chunks and played sequentially.
- Text remains displayed as one complete answer while TTS processes the queue.
- Continuous listening stays paused until the final speech chunk finishes, then resumes automatically.
- Each failed server-TTS chunk falls back independently to browser speech instead of dropping the remainder.
- Existing Lebanese Arabic session preference, single-introduction behavior, privacy isolation, and external-action protections are unchanged.
