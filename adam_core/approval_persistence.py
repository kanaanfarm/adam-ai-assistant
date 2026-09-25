"""Bounded atomic persistence for owner-approval receipts."""
from __future__ import annotations
import json, os, tempfile
from datetime import datetime, timezone
from pathlib import Path

class ApprovalStore:
    def __init__(self, path, max_records=250, max_file_bytes=2_000_000):
        self.path=Path(path); self.max_records=max(1,int(max_records)); self.max_file_bytes=max(1024,int(max_file_bytes))
    def load(self):
        try:
            if not self.path.exists() or self.path.stat().st_size > self.max_file_bytes: return []
            rows=json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(rows,list): return []
            return [r for r in rows if isinstance(r,dict)][-self.max_records:]
        except Exception: return []
    def save(self, rows):
        clean=[r for r in (rows or []) if isinstance(r,dict)][-self.max_records:]
        raw=json.dumps(clean,ensure_ascii=False,indent=2)
        if len(raw.encode("utf-8")) > self.max_file_bytes: raise ValueError("approval persistence exceeds file-size bound")
        self.path.parent.mkdir(parents=True,exist_ok=True)
        fd,tmp=tempfile.mkstemp(prefix=self.path.name+".",suffix=".tmp",dir=str(self.path.parent)); os.close(fd)
        try:
            Path(tmp).write_text(raw,encoding="utf-8"); os.replace(tmp,self.path)
        finally:
            try:
                if Path(tmp).exists(): Path(tmp).unlink()
            except Exception: pass
    def record(self, workflow_id, step):
        row={"workflow_id":str(workflow_id or ""),"step":str(step or ""),"approved":True,"approved_at":datetime.now(timezone.utc).isoformat()}
        rows=self.load(); rows.append(row); self.save(rows); return row
    def is_approved(self, workflow_id, step):
        return any(r.get("approved") is True and str(r.get("workflow_id"))==str(workflow_id) and str(r.get("step"))==str(step) for r in self.load())
