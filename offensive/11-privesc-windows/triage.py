#!/usr/bin/env python3
"""
winPEAS output triage — Windows privilege escalation shortlist.

Parses winPEAS text output and extracts high-priority vectors, ranked by
exploitability.  Works on macOS/Linux (no Windows needed for the analysis).

The Windows-side workflow:
  1. On the target VM: winPEAS.exe | Out-File winpeas_out.txt
  2. Copy winpeas_out.txt to your analysis machine
  3. python3 triage.py winpeas_out.txt   (or: python3 triage.py  for the demo)

Usage:
    python3 triage.py [winpeas_output.txt]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DIVIDER = "─" * 64

# Each rule: (pattern, priority, vector_name, exploit_technique, gtfobins_link)
RULES: list[tuple[str, int, str, str, str]] = [
    (
        r"AlwaysInstallElevated set to 1",
        1,
        "AlwaysInstallElevated",
        "msfvenom -p windows/x64/shell_reverse_tcp ... -f msi > shell.msi; msiexec /quiet /i shell.msi",
        "LOLBAS: msiexec",
    ),
    (
        r"SeImpersonatePrivilege.*Enabled",
        1,
        "SeImpersonatePrivilege",
        "PrintSpoofer.exe -i -c cmd.exe  (or GodPotato/RoguePotato for older OS)",
        "github.com/itm4n/PrintSpoofer",
    ),
    (
        r"Unquoted service path",
        2,
        "Unquoted service path",
        "Place malicious binary at the missing-quote position (e.g. C:\\Program.exe)",
        "GTFOBins-Windows: unquoted service paths",
    ),
    (
        r"Everyone \[AllAccess\].*service binary|service binary.*Everyone \[AllAccess\]|File Permissions: Everyone \[AllAccess\]",
        2,
        "Weak service binary ACL",
        "Replace binary with reverse shell; sc start <service>",
        "LOLBAS: sc.exe",
    ),
    (
        r"World-writable script runs as SYSTEM|Everyone \[AllAccess\].*SYSTEM",
        2,
        "Writable SYSTEM scheduled task/script",
        "Append payload to writable script; wait for schedule or trigger manually",
        "T1053.005 (Scheduled Task)",
    ),
    (
        r"Potential DLL hijack",
        3,
        "DLL hijack opportunity",
        "Drop malicious DLL into writable directory in service PATH",
        "LOLBAS: DLL hijacking",
    ),
    (
        r"Everyone \[Modify\].*autorun|autorun.*Everyone \[Modify\]",
        3,
        "Writable autorun entry",
        "Replace autorun binary with reverse shell; reboot or log on as target user",
        "T1547.001 (Registry Run Keys)",
    ),
    (
        r"Missing patches",
        4,
        "Missing Windows patches",
        "Check missing KB against exploit-db / msrc; run appropriate exploit",
        "msrc.microsoft.com / exploit-db",
    ),
]


def triage(text: str) -> list[dict]:
    findings = []
    for pattern, priority, name, technique, ref in RULES:
        matches = re.findall(r"[^\n]*" + pattern + r"[^\n]*", text, re.IGNORECASE)
        if matches:
            findings.append({
                "priority": priority,
                "name": name,
                "technique": technique,
                "ref": ref,
                "evidence": matches[0].strip(),
            })
    findings.sort(key=lambda x: x["priority"])
    return findings


def demo() -> int:
    # Use command-line arg if given, otherwise use sample data
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if not path.exists():
            print(f"File not found: {path}", file=sys.stderr)
            return 1
        text = path.read_text(errors="replace")
        label = path.name
    else:
        path = DATA_DIR / "winpeas_sample.txt"
        text = path.read_text()
        label = "winpeas_sample.txt (bundled demo data)"

    print("=" * 64)
    print("Windows Privilege Escalation — winPEAS Triage")
    print(f"Input: {label}")
    print("=" * 64)

    findings = triage(text)

    if not findings:
        print("\n  No high-priority vectors matched. Review raw output manually.")
        return 0

    print(f"\nFound {len(findings)} vectors:\n")
    priority_labels = {1: "P0 — Critical (reliable, immediate)", 2: "P1 — High", 3: "P2 — Medium", 4: "P3 — Info/Patching"}

    current_p = None
    for f in findings:
        if f["priority"] != current_p:
            current_p = f["priority"]
            print(f"\n  {priority_labels.get(current_p, f'P{current_p}')}")
            print(f"  {DIVIDER[:50]}")

        print(f"\n  Vector:    {f['name']}")
        print(f"  Technique: {f['technique']}")
        print(f"  Reference: {f['ref']}")
        print(f"  Evidence:  {f['evidence'][:100]}")

    print(f"\n{DIVIDER}")
    print("Next steps:")
    print("  1. Verify the P0 vectors first — confirm the preconditions hold.")
    print("  2. Look up the technique on LOLBAS / GTFOBins-Windows before exploiting.")
    print("  3. A model can explain the technique; YOU verify the preconditions on the target.")
    print("  4. For production evidence: capture 'whoami /priv' output after escalation.")
    print()
    print(f"{'=' * 64}\n")
    return 0


if __name__ == "__main__":
    sys.exit(demo())
