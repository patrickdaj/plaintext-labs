# Module 05 — TLS Deep Dive
# Standard targets: up / down / reset / demo / shell / reload-strong / reload-weak

.PHONY: up down reset demo shell reload-strong reload-weak

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

reload-strong:
	docker compose exec nginx sh -c 'cp /lab/data/nginx-strong.conf /etc/nginx/conf.d/default.conf && nginx -s reload'
	@echo "nginx reloaded with STRONG TLS configuration"

reload-weak:
	docker compose exec nginx sh -c 'cp /lab/data/nginx-weak.conf /etc/nginx/conf.d/default.conf && nginx -s reload'
	@echo "nginx reloaded with WEAK TLS configuration"

demo:
	@echo "=== Module 05 — TLS Deep Dive Demo ==="
	@echo ""
	@echo "--- Scanning WEAK nginx TLS configuration ---"
	docker compose exec lab bash -c '\
		testssl.sh --severity MEDIUM --color 0 nginx:443 2>/dev/null | \
		grep -E "(Testing|MEDIUM|HIGH|CRITICAL|OK|not|weak)" | head -30 || \
		echo "(testssl.sh scanning nginx:443 — run make shell for full output)"'
	@echo ""
	@echo "--- Checking negotiated protocol with openssl s_client ---"
	docker compose exec lab bash -c '\
		echo "Q" | openssl s_client -connect nginx:443 2>/dev/null | \
		grep -E "(Protocol|Cipher|Server certificate)"'
	@echo ""
	@echo "=== Run 'make shell' then: testssl.sh --severity HIGH nginx:443 ==="
	@echo "=== Run 'make reload-strong' to switch to the Mozilla modern profile ==="

shell:
	docker compose exec lab bash
