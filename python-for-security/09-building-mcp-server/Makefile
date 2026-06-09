.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec mcp-server bash

demo:      ## Start server and make three test tool calls
	docker compose run --rm mcp-server sh -c '\
		echo "=== enrich_ip: malicious IP ==="; \
		python test_call.py enrich_ip "{\"ip\": \"185.220.101.1\"}"; \
		echo; \
		echo "=== enrich_ip: clean IP ==="; \
		python test_call.py enrich_ip "{\"ip\": \"8.8.8.8\"}"; \
		echo; \
		echo "=== enrich_ip: unknown IP (404) ==="; \
		python test_call.py enrich_ip "{\"ip\": \"1.2.3.4\"}"; \
		echo; \
		echo "=== enrich_ip: invalid format ==="; \
		python test_call.py enrich_ip "{\"ip\": \"not-an-ip\"}"'
