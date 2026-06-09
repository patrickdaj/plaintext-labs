.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec lab bash

demo:      ## Run checkov and tfsec over data/misconfig.tf
	docker compose run --rm lab sh -c '\
		echo "=== checkov -f data/misconfig.tf ==="; \
		checkov -f data/misconfig.tf --quiet || true; \
		echo; \
		echo "=== tfsec data/ ==="; \
		tfsec data/ 2>/dev/null || true'
