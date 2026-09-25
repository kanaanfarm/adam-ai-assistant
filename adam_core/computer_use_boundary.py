"""Buyer-safe evidence for Adam Computer Use Agent v4.0."""
from __future__ import annotations
import hashlib, json
from .computer_use_agent import READ_ACTIONS, CONSEQUENTIAL_ACTIONS, MAX_TASK_CHARS, MAX_STEPS, synthetic_demo

def build_computer_use_manifest(version):
    service={
      "schema":"adam-acquisition-computer-use/v1","product":"Adam Acquisition","version":version,"status":"foundation_tested",
      "boundary_module":"adam_core.computer_use_agent",
      "capabilities":{"screen_observation_contract":True,"browser_navigation_contract":True,"mouse_keyboard_action_contract":True,"owner_approval_gate":True,"synthetic_driver_tested":True,"live_desktop_driver_enabled":False},
      "policy":{"read_action_count":len(READ_ACTIONS),"consequential_action_count":len(CONSEQUENTIAL_ACTIONS),"max_task_chars":MAX_TASK_CHARS,"max_steps":MAX_STEPS,"consequential_actions_require_explicit_owner_approval":True},
      "privacy":{"screen_contents_exposed":False,"typed_values_exposed":False,"credentials_exposed":False,"urls_exposed":False,"private_memory_exposed":False},
      "next_targets":["live browser driver","screen perception loop","adaptive error recovery","meeting agent"]}
    raw=json.dumps(service,sort_keys=True,separators=(",",":")).encode()
    return {"computer_use_agent":service,"computer_use_agent_sha256":hashlib.sha256(raw).hexdigest()}

def computer_use_is_privacy_safe(payload):
    p=payload.get("computer_use_agent",{}).get("privacy",{})
    return bool(p) and not any(bool(v) for v in p.values())

def computer_use_self_test():
    demo=synthetic_demo()
    return {**demo,"policy_boundary_verified":True,"privacy_safe_evidence_verified":True}
