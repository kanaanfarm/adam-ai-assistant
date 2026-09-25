from pathlib import Path
from adam_core.document_processing import classify_attachment,extract_text_bytes,process_attachment_bytes,build_analysis_prompt,build_docx_bytes,safe_filename,DocumentProcessingError
from adam_core.document_boundary import build_document_boundary_manifest,document_boundary_is_privacy_safe,document_boundary_self_test

def test_text_extraction_and_classification_are_local_and_bounded():
    assert classify_attachment('note.txt','text/plain')=='text'
    assert classify_attachment('photo.jpg','image/jpeg')=='image'
    assert extract_text_bytes('note.txt',b'hello')=='hello'
    assert process_attachment_bytes('note.md',b'# Test','text/markdown')=={'name':'note.md','kind':'text','content':'# Test'}

def test_unsupported_attachment_is_rejected():
    try: process_attachment_bytes('bad.exe',b'MZ','application/octet-stream')
    except DocumentProcessingError: return
    raise AssertionError('unsupported type should be rejected')

def test_analysis_prompt_and_docx_rendering():
    prompt=build_analysis_prompt('Check clause 4','Clause 4 says test')
    assert 'OWNER INSTRUCTION' in prompt and 'Clause 4 says test' in prompt
    data=build_docx_bytes('Adam Test','Line one\n\nLine two')
    assert data[:2]==b'PK'
    assert safe_filename('Adam / Test')=='Adam_Test'

def test_manifest_is_privacy_safe_and_fingerprinted():
    payload=build_document_boundary_manifest(version='v2.1.0')
    assert payload['document_boundary']['status']=='extracted_tested'
    assert payload['document_boundary']['capabilities']['network_required_for_extraction'] is False
    assert len(payload['document_boundary_sha256'])==64
    assert document_boundary_is_privacy_safe(payload)

def test_self_test_is_ai_free_network_free_and_content_private():
    r=document_boundary_self_test()
    assert r['ok'] is True
    assert r['attachment_values_returned_by_evidence'] is False
    assert r['credential_values_returned'] is False
    assert r['external_network_operation_performed'] is False
    assert r['external_ai_operation_performed'] is False

def test_app_delegates_document_processing_to_core():
    source=(Path(__file__).resolve().parents[1]/'app.py').read_text(encoding='utf-8')
    assert 'VERSION = "v8.1.0.1"' in source
    assert 'core_document_extract_text' in source
    assert 'core_process_attachment' in source
    assert 'core_document_analysis_prompt' in source
    assert 'core_document_build_docx' in source
    assert '/api/acquisition/document-boundary' in source
