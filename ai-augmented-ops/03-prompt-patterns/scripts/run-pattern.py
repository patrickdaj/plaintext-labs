#!/usr/bin/env python3
"""
run-pattern.py — Run a single prompt pattern from data/prompt-patterns.md
against the local Ollama instance and print the result.

Usage:
    python3 scripts/run-pattern.py --pattern 3
    python3 scripts/run-pattern.py --pattern 3 --model phi3:mini
    python3 scripts/run-pattern.py --prompt "custom prompt text"
"""

import argparse
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "requests"], check=True)
    import requests

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "tinyllama")

# Built-in example prompts for each pattern number
PATTERN_EXAMPLES = {
    1: (
        "Role Prompting — Alert Severity",
        """You are a SOC analyst at Meridian Financial. Your job is to classify the severity of
security alerts and recommend an immediate action.
Always respond in two sentences: first the severity (CRITICAL/HIGH/MEDIUM/LOW), then
the recommended action. If you are uncertain, say so explicitly.
Do not fabricate tool names, CVE IDs, hash values, or IP addresses.

Alert: Outbound connection from MERIDIAN-WKS-047 to 45.33.32.156:4444. Process: explorer.exe. Duration: 3 minutes.""",
    ),
    2: (
        "Chain-of-Thought — Threat Model",
        """You are a security engineer. Think step by step.

Given the following system description:
A Python web application running behind nginx. It reads from a PostgreSQL database.
It processes uploaded CSV files and stores results in S3. Staff access it from VPN only.

1. List the trust boundaries.
2. For each boundary, list the top 2 threats (use STRIDE categories).
3. For each threat, assign a risk rating (High/Medium/Low) and explain your reasoning.
4. Summarise the top 2 risks in one sentence each.

Show all four steps.""",
    ),
    3: (
        "Structured JSON Output — IOC Extraction",
        """You are a threat intelligence analyst. Extract all indicators of compromise (IOCs) from the
text below. Return ONLY valid JSON matching this schema — no prose, no markdown, no code fences:

{"iocs": [{"type": "ip|domain|hash|url|email", "value": "...", "context": "one sentence"}]}

If no IOCs are present, return: {"iocs": []}
Do not invent values. Only extract what is explicitly stated in the text.

TEXT:
The threat actor used the domain update-checker.net for C2 communication. The initial dropper
had MD5 hash 3d4f2bf07dc1be38b20cd6e46949a1b1. Lateral movement was observed from 10.0.14.22 to 10.0.14.35.""",
    ),
    4: (
        "Structured Output — Alert Triage",
        """You are a security analyst. Classify the following alert. Return ONLY valid JSON:

{"severity": "CRITICAL|HIGH|MEDIUM|LOW",
 "confidence": "HIGH|MEDIUM|LOW",
 "technique": "ATT&CK technique ID or null",
 "action": "one-sentence recommended action",
 "rationale": "one sentence explaining the severity assignment"}

Do not add any other fields. Do not wrap in code fences.

ALERT:
Process cmd.exe spawned by winword.exe with argument: /c powershell -EncodedCommand ZQBjAGgAbwAgAGgAZQBsAGwAbwA=""",
    ),
    5: (
        "Few-Shot Classification — Phishing",
        """Classify the following email as PHISHING or BENIGN. Return only the label and a one-sentence reason.

EMAIL: "Your account will be suspended. Click here: http://secure-login.amaz0n-verify.com"
LABEL: PHISHING — Urgency + lookalike domain impersonating Amazon.

EMAIL: "Hi, the Q3 report is attached. Let me know if you have questions. — Sarah"
LABEL: BENIGN — Internal communication, no suspicious links or urgency.

EMAIL: "Confirm your wire transfer of $142,000. Approval needed in 30 minutes."
LABEL: PHISHING — Business email compromise pattern: financial urgency, compressed timeline.

Now classify:
EMAIL: "Your IT helpdesk account password expires today. Reset it here: http://helpdesk-reset.meridian-it.co/reset?token=8f3a"
LABEL:""",
    ),
}


def call_ollama(prompt: str, model: str) -> dict:
    """Send a prompt to Ollama and return the full response."""
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    try:
        resp = requests.post(url, json=payload, timeout=180)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        print(f"ERROR: Cannot connect to Ollama at {OLLAMA_HOST}")
        print("Run 'make up' first.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("ERROR: Ollama request timed out after 180 seconds.")
        sys.exit(1)


def validate_json_output(text: str) -> tuple[bool, str]:
    """Try to parse JSON from model output, stripping code fences if present."""
    # Strip common code fence patterns
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    try:
        parsed = json.loads(text)
        return True, json.dumps(parsed, indent=2)
    except json.JSONDecodeError as e:
        return False, f"JSON parse error: {e}"


def main():
    parser = argparse.ArgumentParser(description="Run a prompt pattern against Ollama")
    parser.add_argument("--pattern", type=int, choices=range(1, 10),
                        help="Pattern number from data/prompt-patterns.md (1–8, or 9 for custom)")
    parser.add_argument("--prompt", type=str, help="Custom prompt text (overrides --pattern)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name")
    args = parser.parse_args()

    if args.prompt:
        name = "Custom prompt"
        prompt = args.prompt
    elif args.pattern and args.pattern in PATTERN_EXAMPLES:
        name, prompt = PATTERN_EXAMPLES[args.pattern]
    else:
        print("Specify --pattern (1-8) or --prompt 'text'. Pattern 9 requires --prompt.")
        parser.print_help()
        sys.exit(1)

    print(f"=== Pattern: {name} ===")
    print(f"Model: {args.model}  |  Host: {OLLAMA_HOST}")
    print()
    print("PROMPT:")
    print("-" * 60)
    print(prompt[:500] + ("..." if len(prompt) > 500 else ""))
    print("-" * 60)
    print()

    t0 = time.time()
    result = call_ollama(prompt, args.model)
    elapsed = time.time() - t0

    response = result.get("response", "").strip()
    toks = result.get("eval_count", 0)
    throughput = toks / elapsed if elapsed > 0 else 0

    print("RAW OUTPUT:")
    print("-" * 60)
    print(response)
    print("-" * 60)
    print()

    # JSON validation for patterns 3 and 4
    if args.pattern in (3, 4):
        ok, parsed_or_err = validate_json_output(response)
        if ok:
            print("JSON VALIDATION: PASS")
            print(parsed_or_err)
        else:
            print(f"JSON VALIDATION: FAIL — {parsed_or_err}")
            print("Tip: check for code fences or extra prose before the JSON object.")
    print()
    print(f"Latency: {elapsed:.1f}s | Tokens: {toks} | Throughput: {throughput:.1f} tok/s")
    print()
    print("Paste the prompt and raw output into results/pattern-validation.md and")
    print("classify: Hallucination / Off-format / Overconfidence observed?")


if __name__ == "__main__":
    main()
