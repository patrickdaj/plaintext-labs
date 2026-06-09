# Module 05 — Endpoint Telemetry & EDR
# Standard targets: up / down / reset / demo / shell

.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	@echo "=== Module 05 — Endpoint Telemetry with osquery ==="
	@echo ""
	@echo "--- Query 1: Processes with network connections (C2 beaconing detection) ---"
	docker compose exec lab bash -c '\
		osqueryi --json \
		  "SELECT p.pid, p.name, s.remote_address, s.remote_port FROM processes p JOIN process_open_sockets s ON p.pid = s.pid WHERE s.remote_address NOT IN ('"'"''"'"', '"'"'0.0.0.0'"'"', '"'"'127.0.0.1'"'"') AND s.remote_port != 0 LIMIT 10" \
		2>/dev/null | python3 -m json.tool 2>/dev/null || echo "(no remote connections found in container)"'
	@echo ""
	@echo "--- Query 2: Users with login shells ---"
	docker compose exec lab bash -c '\
		osqueryi --json \
		  "SELECT username, uid, shell FROM users WHERE shell NOT LIKE '"'"'%nologin'"'"' AND shell NOT LIKE '"'"'%false'"'"'" \
		2>/dev/null | python3 -m json.tool'
	@echo ""
	@echo "--- Query 3: Listening ports ---"
	docker compose exec lab bash -c '\
		osqueryi --json \
		  "SELECT p.name, l.address, l.port FROM listening_ports l JOIN processes p ON l.pid = p.pid LIMIT 10" \
		2>/dev/null | python3 -m json.tool 2>/dev/null || echo "(query result)"'
	@echo ""
	@echo "--- Query 4: SUID binaries ---"
	docker compose exec lab bash -c '\
		osqueryi --json \
		  "SELECT path, permissions FROM file WHERE path LIKE '"'"'/usr/bin/%'"'"' AND permissions LIKE '"'"'%s%'"'"' AND uid = 0 LIMIT 10" \
		2>/dev/null | python3 -m json.tool'
	@echo ""
	@echo "=== Run 'make shell' then 'osqueryi' for interactive queries ==="

shell:
	docker compose exec lab bash
