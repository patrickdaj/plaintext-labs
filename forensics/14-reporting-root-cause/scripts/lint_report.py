#!/usr/bin/env python3
"""
lint_report.py — structural completeness checker for forensic incident reports.

Checks that all required sections are present and key elements (IOC table, findings,
executive summary) are populated with real content rather than placeholder text.

Usage: python3 lint_report.py <report.md>
       python3 lint_report.py <report.md> --strict   (also checks word count, ATT&CK tags)

Exit code: 0 = pass, 1 = structural failures found.
"""

import sys
import re
import argparse

REQUIRED_SECTIONS = [
    "Executive Summary",
    "Incident Timeline",
    "Technical Findings",
    "Root-Cause Analysis",
    "Indicators of Compromise",
    "Scope Assessment",
    "Remediation Recommendations",
    "Methodology",
]

PLACEHOLDER_PATTERNS = [
    r"\[REQUIRED",
    r"\[Organisation Name\]",
    r"\[Case ID\]",
    r"\[Name\]",
    r"replace this placeholder",
]

IOC_TYPES = ["IP Address", "Domain", "File Hash", "File Path", "IAM"]

ATTCK_PATTERN = re.compile(r"T\d{4}(?:\.\d{3})?")


def check_report(path, strict=False):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    failures = []
    warnings = []

    # 1. Required sections present
    for section in REQUIRED_SECTIONS:
        pattern = re.compile(r"^#{1,3}\s+" + re.escape(section), re.MULTILINE | re.IGNORECASE)
        if not pattern.search(content):
            failures.append(f"MISSING SECTION: '{section}' not found in report")

    # 2. No placeholder text remaining
    for pattern_str in PLACEHOLDER_PATTERNS:
        matches = [(i + 1, lines[i]) for i, line in enumerate(lines)
                   if re.search(pattern_str, line, re.IGNORECASE)]
        for lineno, line in matches:
            failures.append(f"PLACEHOLDER NOT FILLED (line {lineno}): {line.strip()[:80]}")

    # 3. IOC table populated
    ioc_section_match = re.search(r"## Indicators of Compromise.*?(?=^##|\Z)", content,
                                  re.MULTILINE | re.DOTALL)
    if ioc_section_match:
        ioc_section = ioc_section_match.group(0)
        populated_rows = [l for l in ioc_section.splitlines()
                          if l.startswith("|") and "Type" not in l and "----" not in l
                          and l.count("|") >= 4]
        # Filter out rows that are entirely empty cells
        real_rows = [r for r in populated_rows
                     if any(cell.strip() not in ("", "| |") for cell in r.split("|")[1:-1]
                            if cell.strip())]
        if len(real_rows) < 3:
            failures.append(
                f"IOC TABLE: fewer than 3 populated rows found ({len(real_rows)} detected). "
                "Ensure IP, Domain, and File Hash rows are filled."
            )
        # Check for at least one of each key type
        for ioc_type in ["IP", "Domain", "Hash"]:
            if not any(ioc_type.lower() in r.lower() for r in real_rows):
                warnings.append(f"IOC TABLE: no '{ioc_type}' entry found")

    # 4. Technical findings — at least 6
    finding_matches = re.findall(r"^###\s+Finding\s+\d+", content, re.MULTILINE | re.IGNORECASE)
    if len(finding_matches) < 6:
        failures.append(
            f"TECHNICAL FINDINGS: only {len(finding_matches)} findings found; minimum 6 required"
        )

    # 5. Root cause statement
    if "Root Cause Statement" in content:
        rca_match = re.search(
            r"Root Cause Statement.*?(?=^###|^##|\Z)", content, re.MULTILINE | re.DOTALL
        )
        if rca_match:
            rca_text = rca_match.group(0)
            if len(rca_text.strip().splitlines()) < 3:
                failures.append(
                    "ROOT CAUSE STATEMENT: appears to be empty or one-line; "
                    "must include the causal chain and specific control gap"
                )

    # 6. Strict mode: ATT&CK tags in findings, executive summary word count
    if strict:
        findings_section = re.search(
            r"## Technical Findings.*?(?=^##|\Z)", content, re.MULTILINE | re.DOTALL
        )
        if findings_section:
            attck_tags = ATTCK_PATTERN.findall(findings_section.group(0))
            if len(attck_tags) < 4:
                warnings.append(
                    f"STRICT: only {len(attck_tags)} ATT&CK technique IDs found in findings; "
                    "aim for one per finding"
                )

        exec_section = re.search(
            r"## Executive Summary.*?(?=^##|\Z)", content, re.MULTILINE | re.DOTALL
        )
        if exec_section:
            exec_words = len(exec_section.group(0).split())
            if exec_words > 300:
                warnings.append(
                    f"STRICT: Executive Summary is ~{exec_words} words; target is under 250 words"
                )

    # Print results
    print(f"\nForensic Report Linter — {path}")
    print("=" * 60)

    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        for f in failures:
            print(f"  [FAIL] {f}")
    else:
        print("\nAll structural checks PASSED.")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  [WARN] {w}")

    print()
    total = len(failures)
    print(f"Result: {'FAIL' if total else 'PASS'} — {total} failure(s), {len(warnings)} warning(s)")
    print()

    return 1 if failures else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Forensic incident report structural linter")
    parser.add_argument("report", help="Path to the report Markdown file")
    parser.add_argument("--strict", action="store_true",
                        help="Enable strict checks (ATT&CK tags, word count)")
    args = parser.parse_args()

    exit_code = check_report(args.report, strict=args.strict)
    sys.exit(exit_code)
