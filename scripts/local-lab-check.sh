#!/usr/bin/env bash
# local-lab-check.sh — run lab demos on THIS machine to see how they fare on your
# architecture (e.g. Apple Silicon / M-series). It mirrors what Labs CI does
# (`make up && make demo && make down`) but on your real hardware, and flags any
# lab whose image had to run under amd64 emulation — the cross-platform risk pocket.
#
# Usage (from the plaintext-labs root, or anywhere — it cd's to the repo root):
#   scripts/local-lab-check.sh                 # the opt-in (.ci-demo) labs — matches CI
#   scripts/local-lab-check.sh --all           # every lab that has a `make demo`
#   scripts/local-lab-check.sh offensive/05-memory-corruption defensive/17-kev-driven-defense
#                                              # just the labs you name (good for the risk pockets)
#
# Needs Docker running. Nothing is left up — every lab is torn down with `make down`.
set -uo pipefail

# Run from the repo root regardless of where this is invoked from.
cd "$(cd "$(dirname "$0")/.." && pwd)"

arch="$(uname -m)"
docker_arch="$(docker version -f '{{.Server.Arch}}' 2>/dev/null || echo '?')"
echo "Host arch: $arch   |   Docker engine arch: $docker_arch"
echo "(linux/arm64 here = native on Apple Silicon; an 'EMULATED' flag below = amd64-only image)"
echo

# Choose the set of labs to run.
labs=()
if [ "${1:-}" = "--all" ]; then
  while IFS= read -r mk; do labs+=("$(dirname "$mk")"); done \
    < <(grep -rl '^demo:' --include=Makefile . | sed 's|^\./||' | sort)
elif [ "$#" -gt 0 ]; then
  labs=("$@")
else
  while IFS= read -r m; do labs+=("$(dirname "$m")"); done \
    < <(find . -name .ci-demo | sed 's|^\./||' | sort)
fi

[ "${#labs[@]}" -eq 0 ] && { echo "No labs selected."; exit 0; }

printf '%-46s %-7s %-13s %s\n' "LAB" "RESULT" "EMULATED" "SECS"
printf '%-46s %-7s %-13s %s\n' "---" "------" "--------" "----"

fails=0
for lab in "${labs[@]}"; do
  if [ ! -f "$lab/Makefile" ]; then
    printf '%-46s %-7s\n' "$lab" "NO-MK"; continue
  fi
  start=$(date +%s)
  res="PASS"; emu="-"
  out=$( { make -C "$lab" up && make -C "$lab" demo; } 2>&1 ) || res="FAIL"
  # Docker prints this when it runs an amd64-only image on an arm64 host:
  if printf '%s' "$out" | grep -qi "does not match the detected host platform"; then
    emu="amd64 (slow)"
  fi
  make -C "$lab" down >/dev/null 2>&1 || true
  printf '%-46s %-7s %-13s %s\n' "$lab" "$res" "$emu" "$(( $(date +%s) - start ))"
  if [ "$res" = "FAIL" ]; then
    fails=$((fails+1))
    printf '%s\n' "$out" | tail -6 | sed 's/^/    │ /'
  fi
done

echo
echo "Done — ${#labs[@]} lab(s), $fails failure(s)."
echo "FAIL or 'amd64 (slow)' = a cross-platform pocket worth a multi-arch fix or a documented x86/cloud path."
