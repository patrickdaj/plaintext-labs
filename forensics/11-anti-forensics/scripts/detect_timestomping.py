#!/usr/bin/env python3
"""
detect_timestomping.py — detects timestamp manipulation in disk images using Sleuth Kit.

Approach: Run 'fls -r -l' to get file listing with MAC timestamps (SI attribute),
then compare to mactime output where FN timestamps can be derived from -m flag output.

For a true SI vs FN comparison, the script uses 'istat' on each inode and parses both
attribute sections. This is the gold-standard approach used in actual forensic investigations.

Usage: python3 detect_timestomping.py <disk_image>
"""

import subprocess
import re
import sys
from datetime import datetime, timezone


def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr


def parse_fls(image):
    """Return list of (inode, name) for all files."""
    out = run(f"fls -r -l {image}")
    files = []
    for line in out.splitlines():
        # fls -l output: type inode name mtime atime ctime crtime size uid gid
        m = re.match(r'^[rd-]\S+\s+(\d+).*\s(\S+)\s*$', line)
        if not m:
            # Try simpler pattern
            parts = line.split()
            if len(parts) >= 2 and parts[0].startswith(('r/', 'd/')):
                # Format: r/r 12: filename
                inode_match = re.search(r'(\d+):', parts[1] if ':' in parts[1] else '')
                if inode_match and len(parts) > 2:
                    files.append((inode_match.group(1), parts[-1]))
        else:
            files.append((m.group(1), m.group(2)))
    return files


def parse_fls_simple(image):
    """Simpler fls parser for inode + name extraction."""
    out = run(f"fls -r {image}")
    files = []
    for line in out.splitlines():
        # Format: r/r 14:  filename
        m = re.match(r'^[rd]/[rrd-]\s+(\d+):\s+(.+)$', line)
        if m:
            files.append((m.group(1).strip(), m.group(2).strip()))
    return files


def parse_istat_timestamps(image, inode):
    """
    Parse istat output for an inode and return SI and FN timestamps.
    Returns dict with keys 'si' and 'fn', each with subkeys 'modified', 'accessed', 'changed', 'created'.
    """
    out = run(f"istat {image} {inode} 2>&1")
    timestamps = {"si": {}, "fn": {}}
    current_attr = None

    for line in out.splitlines():
        line = line.strip()
        if "Attributes:" in line or "$STANDARD_INFORMATION" in line or "Standard Information" in line:
            current_attr = "si"
        elif "$FILE_NAME" in line or "File Name" in line:
            current_attr = "fn"

        if current_attr:
            for label, key in [
                ("Modified:", "modified"),
                ("Accessed:", "accessed"),
                ("Created:", "created"),
                ("Changed:", "changed"),
                ("MFT Modified:", "mft_modified"),
            ]:
                if label in line:
                    val = line.split(label, 1)[-1].strip()
                    if current_attr in timestamps:
                        timestamps[current_attr][key] = val

    return timestamps


def check_timestomping(image):
    print(f"Analysing: {image}")
    print("=" * 70)

    files = parse_fls_simple(image)
    if not files:
        # Fall back to the raw fls output for display
        print("File listing (fls):")
        print(run(f"fls -r {image}"))
        print()
        print("Note: istat-based SI/FN comparison requires a parseable file listing.")
        print("Run 'fls -r <image>' manually to get inode numbers, then:")
        print("  istat <image> <inode>  — look for divergence between")
        print("  '$STANDARD_INFORMATION' and '$FILE_NAME' timestamp sections.")
        return

    flagged = []
    print(f"{'Inode':<8} {'File':<30} {'SI Modified':<25} {'FN Modified':<25} {'Flag'}")
    print("-" * 100)

    for inode, name in files:
        ts = parse_istat_timestamps(image, inode)
        si_mod = ts["si"].get("modified") or ts["si"].get("created", "n/a")
        fn_mod = ts["fn"].get("modified") or ts["fn"].get("created", "n/a")

        flag = ""
        if si_mod and fn_mod and si_mod != "n/a" and fn_mod != "n/a":
            if si_mod != fn_mod:
                flag = "SI/FN MISMATCH"
                flagged.append((inode, name, si_mod, fn_mod))

        print(f"{inode:<8} {name:<30} {si_mod:<25} {fn_mod:<25} {flag}")

    print()
    if flagged:
        print(f"*** {len(flagged)} POTENTIAL TIMESTOMPING FINDING(S) ***")
        for inode, name, si, fn in flagged:
            print(f"  Inode {inode} ({name}): SI={si}  FN={fn}")
        print()
        print("Next step: run 'istat <image> <inode>' on each flagged file for")
        print("full attribute detail before citing this as a confirmed finding.")
    else:
        print("No SI/FN timestamp divergence detected.")
        print("Note: this script requires istat to expose both SI and FN attributes.")
        print("On ext2/FAT images, NTFS-style dual-attribute comparison is not applicable.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <disk_image>")
        sys.exit(1)
    check_timestomping(sys.argv[1])
