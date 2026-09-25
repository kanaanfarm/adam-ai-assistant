from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_long_tts_queue_present():
    s=(ROOT/'templates/guest_voice_session.html').read_text(encoding='utf-8')
    assert 'splitSpeechChunks' in s
    assert 'maxChars=520' in s
    assert 'for(let i=0;i<chunks.length;i++)' in s
    assert 'await playServerSpeechChunk(chunks[i],lang)' in s

def test_listening_resumes_only_after_queue():
    s=(ROOT/'templates/guest_voice_session.html').read_text(encoding='utf-8')
    block=s[s.index('async function speak('):s.index('async function submit(')]
    assert block.index('for(let i=0;i<chunks.length;i++)') < block.index('if(wantContinuous)setTimeout(startRecognition,350)')

def test_per_chunk_browser_fallback():
    s=(ROOT/'templates/guest_voice_session.html').read_text(encoding='utf-8')
    assert 'await browserSpeakChunk(chunks[i],lang)' in s
