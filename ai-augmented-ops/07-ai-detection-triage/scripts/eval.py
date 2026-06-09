#!/usr/bin/env python3
"""
eval.py — Evaluate triage results against ground truth labels.
Computes confusion matrix, accuracy, precision, recall, and F1 per severity class.

Usage:
    python3 scripts/eval.py
    python3 scripts/eval.py --results results/triage-results.json --truth data/ground-truth.json
"""

import argparse
import json
import os

SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]


def compute_metrics(results: list[dict], ground_truth: dict) -> dict:
    matched = {r["id"]: r for r in results if r["id"] in ground_truth}
    if not matched:
        return {}

    # Confusion matrix: true_label → predicted_label → count
    matrix = {s: {s2: 0 for s2 in SEVERITY_ORDER} for s in SEVERITY_ORDER}
    for alert_id, result in matched.items():
        true_sev = ground_truth[alert_id]["severity"]
        pred_sev = result["severity"]
        if true_sev in SEVERITY_ORDER and pred_sev in SEVERITY_ORDER:
            matrix[true_sev][pred_sev] += 1

    # Per-class metrics
    class_metrics = {}
    for sev in SEVERITY_ORDER:
        tp = matrix[sev][sev]
        fp = sum(matrix[other][sev] for other in SEVERITY_ORDER if other != sev)
        fn = sum(matrix[sev][other] for other in SEVERITY_ORDER if other != sev)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        class_metrics[sev] = {
            "tp": tp, "fp": fp, "fn": fn,
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
        }

    total = sum(matrix[s][s] for s in SEVERITY_ORDER)
    accuracy = total / len(matched) if matched else 0.0

    # False negatives on CRITICAL/HIGH (the dangerous ones)
    fn_critical = [(aid, ground_truth[aid]["severity"], matched[aid]["severity"])
                   for aid in matched
                   if ground_truth[aid]["severity"] in ("CRITICAL", "HIGH")
                   and SEVERITY_ORDER.index(matched[aid]["severity"]) > SEVERITY_ORDER.index(ground_truth[aid]["severity"])]

    return {
        "total_evaluated": len(matched),
        "accuracy": round(accuracy, 3),
        "confusion_matrix": matrix,
        "class_metrics": class_metrics,
        "false_negatives_critical_high": fn_critical,
    }


def print_report(metrics: dict):
    print(f"\n=== Triage Accuracy Report ===")
    print(f"Alerts evaluated: {metrics['total_evaluated']}")
    print(f"Overall accuracy: {metrics['accuracy']:.1%}\n")

    # Confusion matrix
    print("Confusion matrix (rows = true label, cols = predicted):")
    header = f"{'':10}" + "".join(f"{s:10}" for s in SEVERITY_ORDER)
    print(header)
    print("-" * (10 + 10 * len(SEVERITY_ORDER)))
    for true_sev in SEVERITY_ORDER:
        row = f"{true_sev:10}"
        for pred_sev in SEVERITY_ORDER:
            row += f"{metrics['confusion_matrix'][true_sev][pred_sev]:10}"
        print(row)

    print("\nPer-class metrics:")
    print(f"{'Class':10} {'Precision':12} {'Recall':10} {'F1':8}")
    print("-" * 42)
    for sev in SEVERITY_ORDER:
        m = metrics["class_metrics"][sev]
        print(f"{sev:10} {m['precision']:12.3f} {m['recall']:10.3f} {m['f1']:8.3f}")

    if metrics["false_negatives_critical_high"]:
        print(f"\nFALSE NEGATIVES on CRITICAL/HIGH alerts ({len(metrics['false_negatives_critical_high'])}):")
        for alert_id, true_sev, pred_sev in metrics["false_negatives_critical_high"]:
            print(f"  {alert_id}: true={true_sev}, predicted={pred_sev}")
    else:
        print("\nNo false negatives on CRITICAL/HIGH alerts.")

    print()
    print("Copy these results into results/accuracy-report.md.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", default="results/triage-results.json")
    parser.add_argument("--truth", default="data/ground-truth.json")
    args = parser.parse_args()

    with open(args.results) as f:
        results = json.load(f)
    with open(args.truth) as f:
        truth = json.load(f)

    metrics = compute_metrics(results, truth)
    print_report(metrics)

    os.makedirs("results", exist_ok=True)
    with open("results/accuracy-metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)


if __name__ == "__main__":
    main()
