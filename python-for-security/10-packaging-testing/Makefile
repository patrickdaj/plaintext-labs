.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec lab bash

demo:      ## Run ruff+bandit on ai_generated.py (failing), then show fixed.py (passing)
	docker compose run --rm lab sh -c '\
		echo "=== ruff check data/ai_generated.py (BEFORE) ==="; \
		ruff check data/ai_generated.py || true; \
		echo; \
		echo "=== bandit -r data/ai_generated.py (BEFORE) ==="; \
		bandit -r data/ai_generated.py || true; \
		echo; \
		echo "=== (Run make shell then: python -m pytest tests/ after you fix the code) ==="'
