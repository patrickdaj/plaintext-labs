#!/usr/bin/env python3
"""
score_report.py — Parse and diff two CIS-CAT Lite JSON reports.

Usage:
    python3 score_report.py before.json after.json [--min-score SCORE]

Outputs:
    - Overall score before and after
    - Per-control delta table (fail→pass, pass→fail, unchanged)
    - Summary statistics
    - Exit code 1 if --min-score is specified and after-score is below threshold
"""

import json
import sys
import argparse


def load_report(path):
    with open(path) as f:
        return json.load(f)


def diff_reports(before, after):
    before_rules = {r["id"]: r for r in before.get("rules", [])}
    after_rules = {r["id"]: r for r in after.get("rules", [])}

    all_ids = set(before_rules) | set(after_rules)

    improved = []
    regressed = []
    unchanged_fail = []
    unchanged_pass = []

    for rule_id in sorted(all_ids):
        b = before_rules.get(rule_id)
        a = after_rules.get(rule_id)

        if b and a:
            if b["result"] == "fail" and a["result"] == "pass":
                improved.append(a)
            elif b["result"] == "pass" and a["result"] == "fail":
                regressed.append(a)
            elif b["result"] == "fail" and a["result"] == "fail":
                unchanged_fail.append(a)
            else:
                unchanged_pass.append(a)

    return improved, regressed, unchanged_fail, unchanged_pass


def short_title(title, max_len=70):
    return title[:max_len] + "..." if len(title) > max_len else title


def main():
    parser = argparse.ArgumentParser(description="CIS-CAT Lite report differ")
    parser.add_argument("before", help="Path to before JSON report")
    parser.add_argument("after", help="Path to after JSON report")
    parser.add_argument("--min-score", type=int, default=None,
                        help="Exit 1 if after-score is below this threshold")
    args = parser.parse_args()

    before = load_report(args.before)
    after = load_report(args.after)

    print("=" * 70)
    print(f"  CIS-CAT Lite Compliance Delta Report")
    print(f"  Benchmark: {before.get('benchmark', 'Unknown')}")
    print(f"  Host:      {before.get('hostname', 'Unknown')}")
    print("=" * 70)
    print(f"  Before scan: {before.get('scan_date', 'unknown')} — Score: {before.get('score', '?')}%")
    print(f"  After scan:  {after.get('scan_date', 'unknown')}  — Score: {after.get('score', '?')}%")
    print(f"  Delta:       +{after.get('score', 0) - before.get('score', 0)} percentage points")
    print()

    improved, regressed, unchanged_fail, unchanged_pass = diff_reports(before, after)

    if improved:
        print(f"  IMPROVED ({len(improved)} controls moved fail → pass):")
        for r in improved:
            print(f"    [+] [{r['severity'].upper():6}] {short_title(r['title'])}")
        print()

    if regressed:
        print(f"  REGRESSED ({len(regressed)} controls moved pass → fail):")
        for r in regressed:
            print(f"    [-] [{r['severity'].upper():6}] {short_title(r['title'])}")
        print()

    if unchanged_fail:
        print(f"  STILL FAILING ({len(unchanged_fail)} controls):")
        for r in unchanged_fail[:5]:  # show top 5
            print(f"    [!] [{r['severity'].upper():6}] {short_title(r['title'])}")
        if len(unchanged_fail) > 5:
            print(f"    ... and {len(unchanged_fail) - 5} more (see full report)")
        print()

    print("-" * 70)
    print(f"  Controls improved:       {len(improved)}")
    print(f"  Controls regressed:      {len(regressed)}")
    print(f"  Controls still failing:  {len(unchanged_fail)}")
    print(f"  Controls passing both:   {len(unchanged_pass)}")
    print("-" * 70)

    after_score = after.get("score", 0)
    if args.min_score is not None:
        if after_score < args.min_score:
            print(f"\n  THRESHOLD FAILED: after-score {after_score}% < minimum {args.min_score}%")
            sys.exit(1)
        else:
            print(f"\n  THRESHOLD PASSED: after-score {after_score}% >= minimum {args.min_score}%")

    if regressed:
        print(f"\n  WARNING: {len(regressed)} controls regressed. Investigate before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()
