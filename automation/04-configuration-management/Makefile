.PHONY: up down reset demo shell idempotency-check

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec controller bash

demo:      ## Run the hardening playbook twice to prove idempotency
	docker compose exec controller bash -c '\
		echo "=== Run 1 ==="; \
		ansible-playbook -i data/inventory.ini data/hardening.yml; \
		echo; \
		echo "=== Run 2 (should show 0 changed) ==="; \
		ansible-playbook -i data/inventory.ini data/hardening.yml'

idempotency-check:  ## Fail if second run shows any changed tasks
	docker compose exec controller bash -c '\
		ansible-playbook -i data/inventory.ini data/hardening.yml && \
		result=$$(ansible-playbook -i data/inventory.ini data/hardening.yml 2>&1); \
		echo "$$result"; \
		if echo "$$result" | grep -q "changed=[1-9]"; then \
			echo "FAIL: idempotency check failed — tasks changed on second run"; exit 1; \
		else \
			echo "PASS: idempotency confirmed — 0 changed on second run"; \
		fi'
