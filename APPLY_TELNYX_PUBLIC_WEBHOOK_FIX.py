#!/usr/bin/env python3
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent
app_path = root / "app.py"
if not app_path.exists():
    raise SystemExit("app.py not found. Put this file in the ADAM repository root.")
text = app_path.read_text(encoding="utf-8")
backup = root / "app.py.before_telnyx_public_webhook_fix"
if not backup.exists():
    shutil.copy2(app_path, backup)

marker = "# ADAM TELNYX PUBLIC WEBHOOK AUTH BYPASS V2"
block = """
# ADAM TELNYX PUBLIC WEBHOOK AUTH BYPASS V2
_TELNYX_PUBLIC_ENDPOINTS_V2 = frozenset({"telnyx_voice_webhook_v1", "telnyx_voice_readiness_v1"})

def _install_telnyx_public_auth_bypass_v2():
    guards = list(app.before_request_funcs.get(None, []))
    if not guards:
        return 0
    wrapped = []
    for guard in guards:
        if getattr(guard, "_adam_telnyx_bypass_v2", False):
            wrapped.append(guard)
            continue
        def make_wrapper(original):
            def wrapper(*args, **kwargs):
                if request.endpoint in _TELNYX_PUBLIC_ENDPOINTS_V2:
                    return None
                return original(*args, **kwargs)
            wrapper.__name__ = getattr(original, "__name__", "before_request_guard") + "_telnyx_v2"
            wrapper._adam_telnyx_bypass_v2 = True
            return wrapper
        wrapped.append(make_wrapper(guard))
    app.before_request_funcs[None] = wrapped
    return len(wrapped)

_TELNYX_AUTH_GUARDS_WRAPPED_V2 = _install_telnyx_public_auth_bypass_v2()
"""

main_anchor = '\nif __name__ == "__main__":\n'
if marker not in text:
    if main_anchor not in text:
        raise SystemExit("__main__ anchor not found; no changes made.")
    text = text.replace(main_anchor, "\n" + block + "\n" + main_anchor, 1)

app_path.write_text(text, encoding="utf-8")
print("Telnyx public webhook authentication fix applied.")
print("Backup:", backup.name)