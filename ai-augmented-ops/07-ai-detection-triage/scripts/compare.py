#!/usr/bin/env python3
"""Compare triage results against ground truth and print a simple table."""
import json
import os

results_path = "results/triage-results.json"
truth_path = "data/ground-truth.json"

if not os.path.exists(results_path):
    print("No triage results found. Run: make triage (or make demo)")
    exit(1)

with open(results_path) as f:
    results = json.load(f)
with open(truth_path) as f:
    truth = json.load(f)

print(f"{'Match':<6} {'Alert ID':<14} {'Predicted':<10} {'True':<10}")
print("-" * 44)
correct = 0
for r in results:
    aid = r["id"]
    pred = r["severity"]
    true_sev = truth.get(aid, {}).get("severity", "?")
    match = "PASS" if pred == true_sev else "FAIL"
    if pred == true_sev:
        correct += 1
    print(f"{match:<6} {aid:<14} {pred:<10} {true_sev:<10}")

total = len(results)
print(f"\nAccuracy: {correct}/{total} ({100*correct//total if total else 0}%)")
print("Run 'make eval' for the full confusion matrix.")
