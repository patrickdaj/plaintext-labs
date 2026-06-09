# Module 09 — Detecting AD Attacks lab.
.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec lab bash

demo:       ## Run chainsaw over EVTX samples with bundled Sigma rules
	@echo "=== AD Attack Detection Demo ==="
	@echo ""
	@echo "--- 1. Kerberoasting detection (Event 4769, RC4 etype) ---"
	docker compose run --rm lab sh -c '\
	    chainsaw hunt data/evtx/kerberoast-4769.evtx \
	        -s data/rules/kerberoast.yml \
	        --mapping data/sigma-mappings.yml \
	        --csv 2>/dev/null || \
	    python3 data/evtx_demo.py data/evtx/kerberoast-4769.json kerberoast'
	@echo ""
	@echo "--- 2. DCSync detection (Event 4662, DS-Replication rights) ---"
	docker compose run --rm lab sh -c '\
	    chainsaw hunt data/evtx/dcsync-4662.evtx \
	        -s data/rules/dcsync.yml \
	        --mapping data/sigma-mappings.yml \
	        --csv 2>/dev/null || \
	    python3 data/evtx_demo.py data/evtx/dcsync-4662.json dcsync'
	@echo ""
	@echo "--- 3. AS-REP roasting detection (Event 4768, no preauth) ---"
	docker compose run --rm lab sh -c '\
	    chainsaw hunt data/evtx/asrep-4768.evtx \
	        -s data/rules/asrep.yml \
	        --mapping data/sigma-mappings.yml \
	        --csv 2>/dev/null || \
	    python3 data/evtx_demo.py data/evtx/asrep-4768.json asrep'
	@echo ""
	@echo "--- 4. Pass-the-Hash detection (Event 4624 Type 3 NTLM) ---"
	docker compose run --rm lab sh -c '\
	    chainsaw hunt data/evtx/pth-4624.evtx \
	        -s data/rules/pth.yml \
	        --mapping data/sigma-mappings.yml \
	        --csv 2>/dev/null || \
	    python3 data/evtx_demo.py data/evtx/pth-4624.json pth'
	@echo ""
	@echo "=== Rules summary ==="
	docker compose run --rm lab sh -c \
	    'for r in data/rules/*.yml; do echo "Rule: $$r"; grep "title:" $$r; grep "tags:" $$r -A3 | grep attack; echo; done'
	@echo "=== Demo complete. Run 'make shell' to write and test your own rules. ==="
