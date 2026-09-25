from __future__ import annotations
import json, os, tempfile
from pathlib import Path

MAX_WORKFLOW_FILE_BYTES = 2_000_000

class WorkflowStore:
    """Small injected persistence boundary for orchestration workflow records."""
    def __init__(self, path, max_records=100, max_file_bytes=MAX_WORKFLOW_FILE_BYTES):
        self.path=Path(path); self.max_records=max(1,int(max_records)); self.max_file_bytes=max(1024,int(max_file_bytes))

    def load(self):
        if not self.path.exists(): return []
        try:
            if self.path.stat().st_size > self.max_file_bytes: return []
            data=json.loads(self.path.read_text(encoding='utf-8'))
            if not isinstance(data,list): return []
            return [x for x in data if isinstance(x,dict)][-self.max_records:]
        except Exception:
            return []

    def save(self, records):
        safe=[x for x in (records or []) if isinstance(x,dict)][-self.max_records:]
        raw=json.dumps(safe,ensure_ascii=False,indent=2)
        if len(raw.encode('utf-8')) > self.max_file_bytes: raise ValueError('Workflow persistence payload exceeds size limit.')
        self.path.parent.mkdir(parents=True,exist_ok=True)
        fd,tmp=tempfile.mkstemp(prefix=self.path.name+'.',suffix='.tmp',dir=str(self.path.parent))
        try:
            with os.fdopen(fd,'w',encoding='utf-8') as f: f.write(raw)
            os.replace(tmp,self.path)
        finally:
            try:
                if os.path.exists(tmp): os.unlink(tmp)
            except Exception: pass
        return len(safe)
