#!/usr/bin/env python3
"""
detect.py — Offline Sigma rule matcher against Wazuh-shaped alert JSON.

Usage:
    python3 detect.py --rule rules/mydetection.yml --alerts data/alerts.json

This is a teaching matcher for offline use. It supports the subset of Sigma
that is most common in host compromise detections:
  - detection.selection: field: value matching
  - detection.filter_*: exclusion conditions
  - condition: "selection and not filter_*"

It does NOT support all Sigma features (regex, near, etc.).
"""

import json
import yaml
import argparse
import sys
from pathlib import Path


def flatten(d, prefix=""):
    """Flatten nested dict to dot-separated keys."""
    result = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            result.update(flatten(v, key))
        else:
            result[key] = str(v)
    return result


def matches_selection(event_flat, selection):
    """Check if all fields in selection match the event."""
    for field, value in selection.items():
        event_val = event_flat.get(field, "")
        if isinstance(value, list):
            if not any(str(v) in event_val for v in value):
                return False
        else:
            if str(value) not in event_val:
                return False
    return True


def evaluate_rule(rule, alerts):
    """Evaluate a Sigma rule against a list of alert events. Returns matching alerts."""
    detection = rule.get("detection", {})
    condition = detection.get("condition", "selection")

    # Parse selections and filters
    selections = {}
    filters = {}
    for key, val in detection.items():
        if key == "condition":
            continue
        if key.startswith("filter"):
            filters[key] = val
        else:
            selections[key] = val

    matches = []
    for alert in alerts:
        flat = flatten(alert)

        # Evaluate all selections (AND between them if multiple)
        sel_result = all(matches_selection(flat, sel) for sel in selections.values())

        # Evaluate filters (any filter matching = exclude)
        filter_result = any(matches_selection(flat, filt) for filt in filters.values())

        # Evaluate condition
        if "and not" in condition:
            result = sel_result and not filter_result
        elif "and" in condition:
            result = sel_result and filter_result
        elif "not" in condition:
            result = not filter_result
        else:
            result = sel_result

        if result:
            matches.append(alert)

    return matches


def main():
    parser = argparse.ArgumentParser(description="Offline Sigma rule matcher")
    parser.add_argument("--rule", required=True, help="Path to Sigma rule YAML")
    parser.add_argument("--alerts", required=True, help="Path to Wazuh alert JSON")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    with open(args.rule) as f:
        rule = yaml.safe_load(f)

    with open(args.alerts) as f:
        alerts = json.load(f)

    matches = evaluate_rule(rule, alerts)

    print(f"Rule: {rule.get('title', args.rule)}")
    print(f"MITRE ATT&CK: {', '.join(rule.get('tags', []))}")
    print(f"Alerts scanned: {len(alerts)}")
    print(f"Matches: {len(matches)}")
    print()

    if matches:
        for m in matches:
            print(f"  [MATCH] ID={m['id']} | Agent={m['agent']} | Time={m['timestamp']}")
            print(f"          Rule: {m['rule']['description']}")
            if args.verbose:
                print(f"          Full event: {json.dumps(m, indent=10)}")
    else:
        print("  No matches found.")

    sys.exit(0 if matches else 1)


if __name__ == "__main__":
    main()
