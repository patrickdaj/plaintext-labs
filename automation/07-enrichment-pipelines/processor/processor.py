#!/usr/bin/env python3
"""
Processor reference solution: picks up alerts from shared/pending/, enriches them,
writes to shared/processed/ or shared/errors/ on failure.
"""

import json
import os
import shutil
import time
from datetime import datetime
from pathlib import Path

import httpx
import schedule

SHARED = Path("/data/shared")
PENDING = SHARED / "pending"
PROCESSED = SHARED / "processed"
ERRORS = SHARED / "errors"
for d in (PENDING, PROCESSED, ERRORS):
    d.mkdir(parents=True, exist_ok=True)

API_BASE = os.environ.get("THREAT_API_URL", "http://localhost:8080")


def enrich_alert(alert: dict) -> dict:
    ip = alert.get("source_ip", "")
    try:
        resp = httpx.get(f"{API_BASE}/api/v3/ip/{ip}", timeout=httpx.Timeout(connect=5.0, read=10.0))
        if resp.status_code == 200:
            return resp.json()
        return {"verdict": "unknown", "status": resp.status_code}
    except httpx.TimeoutException:
        raise


def process_pending():
    for pending_file in PENDING.glob("*.json"):
        t0 = time.monotonic()
        try:
            alert = json.loads(pending_file.read_text())
        except json.JSONDecodeError:
            shutil.move(str(pending_file), str(ERRORS / pending_file.name))
            continue

        try:
            enrichment = enrich_alert(alert)
            alert["enrichment"] = enrichment
            alert["processed_at"] = datetime.utcnow().isoformat() + "Z"
            verdict = enrichment.get("verdict", "?")
            ms = int((time.monotonic() - t0) * 1000)
            (PROCESSED / pending_file.name).write_text(json.dumps(alert))
            pending_file.unlink()
            print(f"[PROCESSED] {pending_file.stem} verdict={verdict} duration={ms}ms", flush=True)
        except httpx.TimeoutException:
            shutil.move(str(pending_file), str(ERRORS / pending_file.name))
            print(f"[ERROR] {pending_file.stem} timeout — moved to errors/", flush=True)
        except Exception as e:
            shutil.move(str(pending_file), str(ERRORS / pending_file.name))
            print(f"[ERROR] {pending_file.stem} {e} — moved to errors/", flush=True)


schedule.every(3).seconds.do(process_pending)

print("[PROCESSOR] Starting — polling shared/pending/ every 3s", flush=True)
while True:
    schedule.run_pending()
    time.sleep(1)
