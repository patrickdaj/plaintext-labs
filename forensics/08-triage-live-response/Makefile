.PHONY: up down reset demo shell

up:
	docker compose up -d --build
	@echo ""
	@echo "Velociraptor server: http://localhost:8889"
	@echo "Waiting for server to be ready..."
	@sleep 8
	@echo "Environment ready. Run 'make demo' to see artifact collection output."

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	@echo "Running simulated VQL artifact collection against Meridian endpoint..."
	@docker run --rm \
		-v "$(CURDIR)/data:/data" \
		-v "$(CURDIR)/scripts:/scripts" \
		python:3.11-slim \
		sh /scripts/demo.sh

shell:
	docker compose exec lab bash
