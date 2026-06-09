#!/usr/bin/env python3
"""
Reference solution: read alerts.json, deduplicate, filter, write CSV and rich table.
"""

import csv
import json
import os
from pathlib import Path

from rich.console import Console
from rich.table import Table

DATA_FILE = Path(__file__).parent / "data" / "alerts.json"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_CSV = OUTPUT_DIR / "report.csv"

KEEP_SEVERITIES = {"HIGH", "CRITICAL"}
SEVERITY_COLORS = {"CRITICAL": "red", "HIGH": "yellow"}
FIELDNAMES = ["timestamp", "severity", "rule_id", "source_ip", "destination_ip", "dst_port", "description"]


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    console = Console()

    with DATA_FILE.open() as f:
        raw_alerts = json.load(f)

    total_raw = len(raw_alerts)
    seen_fingerprints: set[tuple] = set()
    deduplicated: list[dict] = []

    for alert in raw_alerts:
        severity = alert.get("severity")  # Defensive: null-safe
        if severity not in KEEP_SEVERITIES:
            continue
        fp = (
            alert.get("rule_id", ""),
            alert.get("source_ip", ""),
            alert.get("destination_ip", ""),
            str(alert.get("dst_port", "")),
        )
        if fp in seen_fingerprints:
            continue
        seen_fingerprints.add(fp)
        deduplicated.append(alert)

    # Write CSV
    with OUTPUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(deduplicated)

    # Render rich table
    table = Table(title="Meridian Security Alert Report", show_lines=True)
    table.add_column("Timestamp", style="dim")
    table.add_column("Severity", justify="center")
    table.add_column("Rule", style="bold")
    table.add_column("Source IP")
    table.add_column("Dst IP")
    table.add_column("Port")
    table.add_column("Description")

    for alert in deduplicated:
        sev = alert.get("severity", "")
        color = SEVERITY_COLORS.get(sev, "white")
        table.add_row(
            str(alert.get("timestamp", ""))[:19],
            f"[{color}]{sev}[/{color}]",
            str(alert.get("rule_id", "")),
            str(alert.get("source_ip", "")),
            str(alert.get("destination_ip", "")),
            str(alert.get("dst_port", "")),
            str(alert.get("description", "")),
        )

    console.print(table)
    console.print(
        f"\n[bold]Total raw alerts:[/bold] {total_raw} → "
        f"[bold]HIGH/CRITICAL (deduplicated):[/bold] {len(deduplicated)}"
    )
    console.print(f"[dim]Report written to {OUTPUT_CSV}[/dim]")


if __name__ == "__main__":
    main()
