.PHONY: up down reset demo shell

up:        ## Build and start the lab container
	docker compose up -d --build

down:      ## Stop and remove the container
	docker compose down

reset:     ## Tear down completely (container + local image)
	docker compose down --rmi local --volumes --remove-orphans

shell:     ## Open a shell in the lab container
	docker compose exec lab bash

demo:      ## Run ruff and bandit over data/insecure.py and show findings
	docker compose run --rm lab sh -c '\
		echo "=== ruff check data/insecure.py ==="; \
		ruff check data/insecure.py || true; \
		echo; \
		echo "=== bandit -r data/insecure.py ==="; \
		bandit -r data/insecure.py || true; \
		echo; \
		echo "=== Demo complete. Four findings to fix. ==="'
