#!/bin/sh
# demo.sh — demonstrates anti-forensics detection on the Meridian disk image.
set -e

IMG=/data/disk.img

echo "============================================================"
echo "  Meridian Financial — Anti-Forensics Detection Demo"
echo "  Image: $IMG"
echo "============================================================"
echo ""

if [ ! -f "$IMG" ]; then
    echo "ERROR: disk.img not found at $IMG"
    echo "Run 'make create-image' first (requires Linux host with root)."
    exit 1
fi

echo "--- File System Info (fsstat) ---"
fsstat "$IMG" 2>&1 | head -20
echo ""

echo "--- File Listing (fls -r) ---"
fls -r "$IMG" 2>&1
echo ""

echo "--- Deleted files (fls -d flag) ---"
fls -r -d "$IMG" 2>&1 || echo "(no deleted file entries found via fls -d)"
echo ""

echo "--- All entries including deleted (fls -ra) ---"
fls -r -a "$IMG" 2>&1
echo ""

echo "--- Inode detail for svchost32.exe ---"
# Find the inode for svchost32.exe
INODE=$(fls -r "$IMG" 2>/dev/null | grep -i "svchost32" | grep -oE '[0-9]+:' | head -1 | tr -d ':')
if [ -n "$INODE" ]; then
    echo "Inode: $INODE"
    istat "$IMG" "$INODE" 2>&1
else
    echo "(svchost32.exe not found in listing — check fls output above)"
fi
echo ""

echo "--- Running Python timestamp detection script ---"
python3 /scripts/detect_timestomping.py "$IMG"
echo ""

echo "============================================================"
echo "  KEY FINDINGS:"
echo "  - svchost32.exe: mtime set to 2019 via touch"
echo "  - All other files have 2024 timestamps consistent with"
echo "    workstation deployment date"
echo "  - notes.txt deleted from directory — may be recoverable"
echo "    via icat on unallocated inode"
echo "  Action: Document timestamp discrepancy; attempt icat recovery."
echo "============================================================"
