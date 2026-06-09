.PHONY: up down reset demo shell

up:
	docker compose up -d --build
	@echo "n8n available at http://localhost:5678"
	@echo "Import data/meridian-workflow.json via n8n Settings > Import"

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec n8n sh

demo:      ## Trigger the Meridian webhook and show ticket output
	@echo "Triggering webhook with a HIGH alert..."
	curl -s -X POST http://localhost:5678/webhook/meridian-alert \
		-H "Content-Type: application/json" \
		-d '{"source_ip":"185.220.101.1","alert":"brute force detected","severity":"HIGH"}' \
		| python3 -m json.tool || true
	@echo
	@sleep 3
	@echo "=== Tickets created ==="
	@ls data/tickets/ 2>/dev/null || echo "(no tickets yet — import the workflow first)"
