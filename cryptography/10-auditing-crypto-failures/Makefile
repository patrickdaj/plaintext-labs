# Module 10 — Auditing Applied-Crypto Failures
# Standard targets: up / down / reset / demo / shell

.PHONY: up down reset demo shell scan-legacy scan-modern scan-strong

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

scan-legacy:
	docker compose exec lab testssl.sh --severity MEDIUM --color 0 nginx-legacy:443 2>/dev/null

scan-modern:
	docker compose exec lab testssl.sh --severity MEDIUM --color 0 nginx-modern:443 2>/dev/null

scan-strong:
	docker compose exec lab testssl.sh --severity MEDIUM --color 0 nginx-strong:443 2>/dev/null

demo:
	@echo "=== Module 10 — Auditing Applied-Crypto Failures Demo ==="
	@echo ""
	@echo "--- Scanning all three TLS configurations ---"
	@echo ""
	@echo "[1] LEGACY (payment gateway — TLS 1.0, mixed ciphers):"
	docker compose exec lab bash -c '\
		testssl.sh --severity HIGH --color 0 nginx-legacy:443 2>/dev/null | \
		grep -E "(MEDIUM|HIGH|CRITICAL|OK|not ok)" | head -15 || \
		echo "  (run: make scan-legacy for full output)"'
	@echo ""
	@echo "[2] MODERN (modernised API — TLS 1.2+, mixed ciphers):"
	docker compose exec lab bash -c '\
		testssl.sh --severity HIGH --color 0 nginx-modern:443 2>/dev/null | \
		grep -E "(MEDIUM|HIGH|CRITICAL|OK|not ok)" | head -10 || \
		echo "  (run: make scan-modern for full output)"'
	@echo ""
	@echo "[3] STRONG (new microservice — TLS 1.3, AEAD only):"
	docker compose exec lab bash -c '\
		testssl.sh --severity HIGH --color 0 nginx-strong:443 2>/dev/null | \
		grep -E "(HIGH|CRITICAL|not ok)" | head -5 || \
		echo "  No HIGH/CRITICAL findings — strong configuration confirmed."'
	@echo ""
	@echo "=== Run 'make shell' then testssl.sh for the full audit exercise ==="
	@echo "=== make scan-legacy / scan-modern / scan-strong for per-server output ==="

shell:
	docker compose exec lab bash
