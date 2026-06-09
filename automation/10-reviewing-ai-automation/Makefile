.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec lab bash

demo:      ## Run checkov on ai_generated_terraform.tf (before) and fixed.tf (after, if it exists)
	docker compose run --rm lab sh -c '\
		echo "=== checkov data/ai_generated_terraform.tf (BEFORE) ==="; \
		checkov -f data/ai_generated_terraform.tf --quiet || true; \
		echo; \
		if [ -f data/fixed.tf ]; then \
			echo "=== checkov data/fixed.tf (AFTER) ==="; \
			checkov -f data/fixed.tf --quiet || true; \
		else \
			echo "(data/fixed.tf not yet created — complete the lab steps first)"; \
		fi'
