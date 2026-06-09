# Module 09 — Local Privilege-Escalation Defense
# Standard targets: up / down / reset / demo / shell

.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	@echo "=== Module 09 — Privilege Escalation Defense Demo ==="
	@echo ""
	@echo "--- Step 1: Find SUID binaries ---"
	docker compose exec lab bash -c '\
		echo "All SUID binaries on this host:"; \
		find / -perm -4000 -type f 2>/dev/null; \
		echo ""; \
		echo "Deliberate misconfiguration: /usr/local/bin/find-suid"; \
		ls -la /usr/local/bin/find-suid; \
		echo ""; \
		echo "GTFOBins technique for find (SUID):"; \
		echo "  find . -exec /bin/sh -p \\; -quit"; \
		echo "  (This would give a root shell via the SUID find binary)"'
	@echo ""
	@echo "--- Step 2: Demonstrate the misconfiguration (as appuser) ---"
	docker compose exec lab bash -c '\
		echo "Running as: $(id)"; \
		echo "Attempting SUID exploitation as appuser..."; \
		su appuser -c "/usr/local/bin/find-suid /tmp -maxdepth 0 -exec id \\;" 2>/dev/null || \
		  echo "(Shell execution blocked in container — on a real host this would show uid=0)"'
	@echo ""
	@echo "--- Step 3: Remediation — remove SUID bit ---"
	docker compose exec lab bash -c '\
		echo "Before:"; ls -la /usr/local/bin/find-suid | awk "{print \$1, \$9}"; \
		chmod u-s /usr/local/bin/find-suid; \
		echo "After: "; ls -la /usr/local/bin/find-suid | awk "{print \$1, \$9}"; \
		echo "SUID bit removed. Exploitation path closed."'
	@echo ""
	@echo "--- Step 4: Full SUID audit ---"
	docker compose exec lab bash -c '\
		echo "Remaining SUID binaries (should be standard system binaries only):"; \
		find / -perm -4000 -type f 2>/dev/null | sort'
	@echo ""
	@echo "=== Run 'make shell' to explore privilege escalation techniques ==="

shell:
	docker compose exec lab bash
