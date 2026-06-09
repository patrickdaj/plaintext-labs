#!/usr/bin/env python3
"""
Reference solution: parse Meridian's SSH auth log, find brute-force sources.
Standard library only — no third-party dependencies.
"""

import re
import collections
import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent / "data" / "sshd.log"

# Named-group regex for failed-password lines.
# Matches: Nov 15 08:00:06 meridian-jump sshd[1234]: Failed password for root from 192.168.100.200 port 41234 ssh2
FAILED_RE = re.compile(
    r"(?P<month>\w+)\s+(?P<day>\d+)\s+(?P<time>\d{2}:\d{2}:\d{2})\s+"
    r"\S+\s+sshd\[\d+\]:\s+Failed password for (?P<user>\S+) "
    r"from (?P<ip>\d{1,3}(?:\.\d{1,3}){3}) port \d+"
)

BRUTE_THRESHOLD = 10
WINDOW_SECONDS = 60


def parse_timestamp(month: str, day: str, time_str: str) -> datetime.datetime:
    """Parse a syslog-style timestamp; assume current year."""
    return datetime.datetime.strptime(
        f"2024 {month} {day} {time_str}", "%Y %b %d %H:%M:%S"
    )


def main() -> None:
    failures: dict[str, list[datetime.datetime]] = collections.defaultdict(list)
    counter: collections.Counter = collections.Counter()

    for line in LOG_FILE.open():
        m = FAILED_RE.search(line)
        if not m:
            continue
        ip = m.group("ip")
        ts = parse_timestamp(m.group("month"), m.group("day"), m.group("time"))
        counter[ip] += 1
        failures[ip].append(ts)

    print("=== Top 5 IPs by failed-login count ===")
    for ip, count in counter.most_common(5):
        print(f"  {ip:<20} {count:>4} failures")

    print("\n=== Brute-force sources (>= 10 failures in 60 s) ===")
    brute_sources = []
    for ip, times in failures.items():
        times_sorted = sorted(times)
        for i, t_start in enumerate(times_sorted):
            window = [t for t in times_sorted[i:] if (t - t_start).total_seconds() <= WINDOW_SECONDS]
            if len(window) >= BRUTE_THRESHOLD:
                brute_sources.append((ip, len(window), t_start))
                break

    if brute_sources:
        for ip, count, when in sorted(brute_sources, key=lambda x: -x[1]):
            print(f"  {ip:<20} {count} failures in {WINDOW_SECONDS}s window starting {when}")
    else:
        print("  (none detected)")


if __name__ == "__main__":
    main()
