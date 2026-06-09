.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec lab bash

demo:      ## Run sigma check then pytest (sigma check fails on broken rule)
	docker compose run --rm lab sh -c '\
		echo "=== sigma check data/rules/ ==="; \
		sigma check data/rules/ || true; \
		echo; \
		echo "=== pytest data/tests/ -v (run after fixing the broken rule) ==="; \
		pytest data/tests/ -v 2>/dev/null || echo "(tests not yet written — see lab steps)"'
