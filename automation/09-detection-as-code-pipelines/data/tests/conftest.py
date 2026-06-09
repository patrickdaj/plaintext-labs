"""
conftest.py — provides the match_rule(rule_path, event_path) fixture for detection tests.

The matcher evaluates a subset of Sigma condition syntax against JSONL event files.
It handles: contains, endswith, contains|all — sufficient for the five rules in this lab.
"""

import json
import re
from pathlib import Path

import pytest
import yaml


def _check_field(event: dict, field_spec: str, value) -> bool:
    """Evaluate a single Sigma field condition against an event."""
    if "|" in field_spec:
        field, *modifiers = field_spec.split("|")
    else:
        field, modifiers = field_spec, []

    event_val = event.get(field, "")
    if event_val is None:
        return False

    if isinstance(value, list):
        if "all" in modifiers:
            return all(_check_field(event, field_spec.replace("|all", ""), v) for v in value)
        return any(_check_field(event, field_spec, v) for v in value)

    value_str = str(value)
    event_str = str(event_val)

    if "endswith" in modifiers:
        return event_str.lower().endswith(value_str.lower())
    if "contains" in modifiers:
        return value_str.lower() in event_str.lower()
    if "startswith" in modifiers:
        return event_str.lower().startswith(value_str.lower())
    return event_str.lower() == value_str.lower()


def _matches_rule(rule: dict, event: dict) -> bool:
    """Evaluate whether a Sigma rule matches an event (simplified condition evaluation)."""
    detection = rule.get("detection", {})
    condition = detection.get("condition", "")

    named_groups = {k: v for k, v in detection.items() if k != "condition"}
    group_results = {}

    for group_name, group_def in named_groups.items():
        if not isinstance(group_def, dict):
            group_results[group_name] = False
            continue
        all_match = True
        for field_spec, value in group_def.items():
            if not _check_field(event, field_spec, value):
                all_match = False
                break
        group_results[group_name] = all_match

    # Evaluate simple conditions: single name or "not name"
    cond = condition.strip()
    if cond in group_results:
        return group_results[cond]
    if cond.startswith("not "):
        return not group_results.get(cond[4:].strip(), False)
    if " and " in cond:
        parts = cond.split(" and ")
        return all(group_results.get(p.strip(), False) for p in parts)
    if " or " in cond:
        parts = cond.split(" or ")
        return any(group_results.get(p.strip(), False) for p in parts)
    return False


def match_rule(rule_path: str, event_path: str) -> bool:
    """
    Load a Sigma rule YAML and a JSONL event file.
    Returns True if the rule matches at least one event in the file.
    """
    rule = yaml.safe_load(Path(rule_path).read_text())
    events = [json.loads(line) for line in Path(event_path).read_text().splitlines() if line.strip()]
    return any(_matches_rule(rule, event) for event in events)
