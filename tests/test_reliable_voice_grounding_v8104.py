from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_version_and_grounding_rule():
 s=(ROOT/'app.py').read_text(encoding='utf-8')
 assert 'VERSION = "v8.1.0.4.1"' in s
 assert 'FACTUAL GROUNDING: Never invent names, families' in s
 assert 'do not claim they permanently retrain' in s
def test_unified_voice_delivery_controller():
 s=(ROOT/'templates/guest_voice_session.html').read_text(encoding='utf-8')
 for x in ['voiceJobSeq','deliverChunk','withTimeout','chunks_spoken','tts_completed','tts_failed']:
  assert x in s
 assert 'for(let attempt=1;attempt<=2;attempt++)' in s
 assert "return 'browser'" in s
def test_voice_waits_then_resumes():
 s=(ROOT/'templates/guest_voice_session.html').read_text(encoding='utf-8')
 block=s[s.index('async function speak('):s.index('async function submit(')]
 assert block.index('await deliverChunk') < block.index('tts_completed=true') < block.index('setTimeout(startRecognition,450)')
def test_preserves_guest_boundaries():
 s=(ROOT/'app.py').read_text(encoding='utf-8')
 assert "Never expose or infer the owner's memory" in s
 assert 'Never claim to have sent, called, scheduled, purchased, traded' in s
