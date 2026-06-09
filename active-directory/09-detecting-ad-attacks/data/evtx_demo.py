#!/usr/bin/env python3
"""
evtx_demo.py — Offline demo matcher for AD detection rules.
Reads JSON-shaped event data (since binary EVTX requires a live DC)
and applies simplified Sigma-style detection logic.

Usage: python3 evtx_demo.py <events.json> <rule_type>
rule_type: kerberoast | dcsync | asrep | pth
"""
import json
import sys
from datetime import datetime


RULES = {
    "kerberoast": {
        "description": "Kerberoasting — RC4 TGS request for service account",
        "attck": "T1558.003",
        "logic": lambda e: (
            e.get("System", {}).get("EventID") == 4769
            and e.get("EventData", {}).get("TicketEncryptionType") == "0x17"
            and not e.get("EventData", {}).get("ServiceName", "").endswith("$")
        ),
        "alert_fields": ["TargetUserName", "ServiceName", "TicketEncryptionType", "IpAddress"],
    },
    "dcsync": {
        "description": "DCSync — DS-Replication rights by non-DC account",
        "attck": "T1003.006",
        "logic": lambda e: (
            e.get("System", {}).get("EventID") == 4662
            and "1131f6ae-9c07-11d1-f79f-00c04fc2dcd2" in e.get("EventData", {}).get("Properties", "")
            and not e.get("EventData", {}).get("SubjectUserName", "").endswith("$")
        ),
        "alert_fields": ["SubjectUserName", "SubjectDomainName", "ObjectName", "Properties"],
    },
    "asrep": {
        "description": "AS-REP Roasting — no pre-authentication required",
        "attck": "T1558.004",
        "logic": lambda e: (
            e.get("System", {}).get("EventID") == 4768
            and e.get("EventData", {}).get("PreAuthType") == "0"
            and e.get("EventData", {}).get("Status") == "0x0"
            and not e.get("EventData", {}).get("TargetUserName", "").endswith("$")
        ),
        "alert_fields": ["TargetUserName", "PreAuthType", "TicketEncryptionType", "IpAddress"],
    },
    "pth": {
        "description": "Pass-the-Hash — NTLM Type 3 logon from unusual source",
        "attck": "T1550.002",
        "logic": lambda e: (
            e.get("System", {}).get("EventID") == 4624
            and e.get("EventData", {}).get("LogonType") == "3"
            and e.get("EventData", {}).get("AuthenticationPackageName") == "NTLM"
            and not e.get("EventData", {}).get("TargetUserName", "").endswith("$")
            and e.get("EventData", {}).get("TargetUserName") != "ANONYMOUS LOGON"
            and e.get("EventData", {}).get("IpAddress") not in ("127.0.0.1", "::1", "-")
        ),
        "alert_fields": ["TargetUserName", "AuthenticationPackageName", "LogonType", "IpAddress", "WorkstationName"],
    },
}


def match(events_file: str, rule_type: str) -> None:
    rule = RULES[rule_type]
    with open(events_file) as f:
        events = json.load(f)

    print(f"Rule:   {rule['description']}")
    print(f"ATT&CK: {rule['attck']}")
    print(f"Events: {len(events)} records in {events_file}")
    print()

    matches = []
    for event in events:
        if rule["logic"](event):
            matches.append(event)

    if not matches:
        print("[NO MATCH] Rule did not fire on any event.")
        return

    print(f"[ALERT] {len(matches)} match(es) found:")
    for i, m in enumerate(matches, 1):
        ts = m.get("System", {}).get("TimeCreated", "unknown")
        host = m.get("System", {}).get("Computer", "unknown")
        print(f"\n  Match {i}:")
        print(f"    Timestamp:  {ts}")
        print(f"    Host:       {host}")
        for field in rule["alert_fields"]:
            val = m.get("EventData", {}).get(field, "(not present)")
            print(f"    {field:<35} {val}")
        if "_description" in m:
            print(f"    Note:       {m['_description']}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: evtx_demo.py <events.json> <rule_type>")
        print("rule_type: kerberoast | dcsync | asrep | pth")
        sys.exit(1)

    events_file = sys.argv[1]
    rule_type = sys.argv[2]

    if rule_type not in RULES:
        print(f"Unknown rule type: {rule_type}. Choose: {list(RULES.keys())}")
        sys.exit(1)

    match(events_file, rule_type)
