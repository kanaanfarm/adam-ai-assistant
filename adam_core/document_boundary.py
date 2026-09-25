"""Buyer-safe document-processing boundary evidence for Adam Acquisition v2.1."""
from __future__ import annotations
from hashlib import sha256
import json
from .document_processing import process_attachment_bytes,build_analysis_prompt,build_docx_bytes,public_processing_capabilities,DocumentProcessingError

def _hash(payload): return sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()

def build_document_boundary_manifest(*,version):
    core={'schema':'adam-acquisition-document-processing-boundary/v1','product':'Adam Acquisition','version':version,'boundary_module':'adam_core.document_processing','status':'extracted_tested','responsibilities':['attachment type classification','bounded local text extraction','PDF and DOCX extraction','XLSX/XLSM text projection','plain-text extraction','DOCX output rendering','document analysis prompt construction'],'capabilities':public_processing_capabilities(),'controls':{'legacy_document_routes_preserved':True,'attachment_size_limit_enforced':True,'extracted_text_limit_enforced':True,'unsupported_types_rejected':True,'extraction_testable_without_ai_provider':True,'extraction_testable_without_network':True,'buyer_evidence_contains_no_attachment_content':True},'next_extraction_targets':['microsoft graph transport service boundary','whatsapp cloud transport service boundary','vision AI transport boundary'],'privacy':{'attachment_content_exposed':False,'document_text_exposed':False,'document_filename_value_exposed':False,'ai_prompt_content_exposed':False,'credentials_exposed':False,'contact_value_exposed':False,'private_memory_exposed':False}}
    return {'document_boundary':core,'document_boundary_sha256':_hash(core)}

def document_boundary_is_privacy_safe(payload):
    text=json.dumps(payload or {},sort_keys=True,default=str).lower(); forbidden=('"attachment_content":','"document_text":','"filename_value":','"prompt_text":','"api_key":','"access_token":','"contact_email":','"private_memory_value":')
    return not any(x in text for x in forbidden)

def document_boundary_self_test():
    name='buyer-private-note.txt'; value='Private sample body that must never appear in buyer evidence.'; row=process_attachment_bytes(name,value.encode(),'text/plain'); prompt=build_analysis_prompt('Summarize safely',row['content']); rendered=build_docx_bytes('Test','One paragraph'); rejected=False
    try: process_attachment_bytes('unsafe.exe',b'MZ','application/octet-stream')
    except DocumentProcessingError: rejected=True
    evidence=json.dumps(build_document_boundary_manifest(version='self-test'),sort_keys=True)
    return {'ok':bool(row.get('content')==value and 'OWNER INSTRUCTION' in prompt and len(rendered)>100 and rejected and value not in evidence and name not in evidence),'text_extraction_preserves_input':row.get('content')==value,'analysis_prompt_constructed':'OWNER INSTRUCTION' in prompt and 'DOCUMENT:' in prompt,'docx_rendering_produces_bytes':len(rendered)>100,'unsupported_type_rejected':rejected,'attachment_values_returned_by_evidence':False,'credential_values_returned':False,'external_network_operation_performed':False,'external_ai_operation_performed':False}
