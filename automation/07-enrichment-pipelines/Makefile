.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec processor sh

demo:      ## Run pipeline for 30 seconds and show processed output
	docker compose up -d --build
	@echo "Pipeline running — waiting 30 seconds..."
	@sleep 30
	@echo
	@echo "=== Processed alerts ==="
	@docker compose exec processor sh -c 'ls /data/shared/processed/ | head -10 && echo "Total:" $$(ls /data/shared/processed/ | wc -l)'
	@echo
	@docker compose logs processor --tail=20
