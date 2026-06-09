#!/usr/bin/env python3
"""Collector: generates alert JSON every 5 seconds and writes to shared/pending/."""

import json
import os
import random
import time
import uuid
from datetime import datetime
from pathlib import Path

import schedule

SHARED = Path("/data/shared")
PENDING = SHARED / "pending"
PENDING.mkdir(parents=True, exist_ok=True)

SOURCE_IPS = ["185.220.101.1", "198.51.100.77", "8.8.8.8", "203.0.113.10", "172.16.0.5"]
RULES = ["RULE-001", "RULE-002", "RULE-003", "RULE-004", "RULE-005"]
SEVERITIES = ["HIGH", "HIGH", "CRITICAL", "MEDIUM"]


def generate_alert():
    alert_id = str(uuid.uuid4())
    alert = {
        "alert_id": alert_id,
        "rule_id": random.choice(RULES),
        "source_ip": random.choice(SOURCE_IPS),
        "severity": random.choice(SEVERITIES),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    (PENDING / f"{alert_id}.json").write_text(json.dumps(alert))
    print(f"[COLLECTOR] Generated alert {alert_id}", flush=True)


schedule.every(5).seconds.do(generate_alert)

print("[COLLECTOR] Starting — writing alerts to shared/pending/ every 5s", flush=True)
while True:
    schedule.run_pending()
    time.sleep(1)
