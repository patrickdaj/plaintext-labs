#!/usr/bin/env python3
"""
triage.py — AI-assisted alert triage using a local Ollama model.

Reads alerts from data/alerts.jsonl, classifies each one with a structured prompt,
and writes results to results/triage-results.json.

Usage:
    python3 scripts/triage.py                        # triage all alerts
    python3 scripts/triage.py --sample 5             # triage first 5 alerts (demo)
    python3 scripts/triage.py --threshold HIGH       # also write escalate/below-threshold splits
    python3 scripts/triage.py --model phi3:mini      # use a different model
"""

import argparse
import json
import os
import sys
import time

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "tinyllama")
SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

SYSTEM_PROMPT = """You are a SOC analyst performing alert triage. Classify each security alert.

Return ONLY valid JSON with no markdown fences, no prose, no extra fields:
{"severity": "CRITICAL|HIGH|MEDIUM|LOW",
 "confidence": "HIGH|MEDIUM|LOW",
 "technique": "ATT&CK technique ID or null",
 "action": "one-sentence recommended immediate action",
 "rationale": "one sentence explaining the severity assignment"}

Rules:
- When uncertain between two severities, choose the HIGHER one.
- CRITICAL: active exploitation, data exfiltration in progress, ransomware, credential dumping.
- HIGH: confirmed malicious indicator, likely attack activity requiring same-day investigation.
- MEDIUM: suspicious but unconfirmed, policy violation, requires investigation.
- LOW: expected activity, operational event, no security indicators.

Examples:
Alert: "winword.exe spawned cmd.exe which executed powershell.exe -EncodedCommand..."
{"severity":"CRITICAL","confidence":"HIGH","technique":"T1059.001","action":"Isolate host immediately and initiate IR process.","rationale":"Office spawning encoded PowerShell is a confirmed T1059.001 indicator with high confidence of compromise."}

Alert: "Scheduled nightly backup completed successfully."
{"severity":"LOW","confidence":"HIGH","technique":null,"action":"No action required; log for audit trail.","rationale":"Expected operational activity with no security indicators."}
"""


def install_deps():
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "requests"], check=True)


try:
    import requests
except ImportError:
    install_deps()
    import requests


def classify_alert(alert: dict, model: str) -> dict:
    """Send an alert to Ollama and parse the structured classification."""
    prompt = f"""{SYSTEM_PROMPT}

Now classify:
Alert: "{alert['title']}. {alert['description']}"
Host: {alert['host']}
"""
    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        raw = resp.json().get("response", "").strip()

        # Strip code fences if model wraps the JSON
        if raw.startswith("```"):
            lines = raw.splitlines()
            raw = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

        parsed = json.loads(raw)

        # Validate required fields
        required = {"severity", "confidence", "technique", "action", "rationale"}
        if not required.issubset(parsed.keys()):
            raise ValueError(f"Missing fields: {required - set(parsed.keys())}")
        if parsed["severity"] not in SEVERITY_ORDER:
            raise ValueError(f"Invalid severity: {parsed['severity']}")

        return {"id": alert["id"], "status": "ok", "raw": raw, **parsed}

    except (json.JSONDecodeError, ValueError, KeyError) as e:
        # Parse failure → flag for human review, default to HIGH
        return {
            "id": alert["id"],
            "status": "parse_error",
            "severity": "HIGH",  # conservative default
            "confidence": "LOW",
            "technique": None,
            "action": "MANUAL REVIEW REQUIRED — model output could not be parsed.",
            "rationale": f"Parse error: {e}. Raw output flagged for human review.",
            "raw": resp.json().get("response", "") if "resp" in dir() else "",
        }


def main():
    parser = argparse.ArgumentParser(description="AI-assisted alert triage")
    parser.add_argument("--sample", type=int, default=None, help="Only process first N alerts")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--threshold", choices=SEVERITY_ORDER, default=None,
                        help="Write HIGH+ alerts to escalate.json, below-threshold to separate file")
    args = parser.parse_args()

    alerts = []
    with open("data/alerts.jsonl") as f:
        for line in f:
            line = line.strip()
            if line:
                alerts.append(json.loads(line))

    if args.sample:
        alerts = alerts[:args.sample]

    print(f"Triaging {len(alerts)} alerts with model '{args.model}'...")
    print()

    results = []
    for i, alert in enumerate(alerts, 1):
        t0 = time.time()
        result = classify_alert(alert, args.model)
        elapsed = time.time() - t0
        status_icon = "OK" if result["status"] == "ok" else "FAIL"
        print(f"[{i:2}/{len(alerts)}] {alert['id']} | {result['severity']:8} | {elapsed:.1f}s | {status_icon}")
        if result["status"] != "ok":
            print(f"         WARNING: {result['rationale']}")
        results.append(result)

    os.makedirs("results", exist_ok=True)
    out_path = "results/triage-results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults written to {out_path}")

    # Summary
    severity_counts = {}
    for r in results:
        s = r["severity"]
        severity_counts[s] = severity_counts.get(s, 0) + 1
    print("\nSeverity distribution:")
    for sev in SEVERITY_ORDER:
        print(f"  {sev:8}: {severity_counts.get(sev, 0)}")

    # Threshold split
    if args.threshold:
        threshold_idx = SEVERITY_ORDER.index(args.threshold)
        escalate = [r for r in results if SEVERITY_ORDER.index(r["severity"]) <= threshold_idx]
        below = [r for r in results if SEVERITY_ORDER.index(r["severity"]) > threshold_idx]
        with open("results/escalate.json", "w") as f:
            json.dump(escalate, f, indent=2)
        with open("results/below-threshold.json", "w") as f:
            json.dump(below, f, indent=2)
        print(f"\nThreshold '{args.threshold}': {len(escalate)} to escalate, {len(below)} to hold queue.")


if __name__ == "__main__":
    main()
