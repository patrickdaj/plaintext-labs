# Module 06 — Configuration Management
# Standard targets: up / down / reset / demo / shell

.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	@echo "=== Module 06 — Ansible Hardening Playbook Demo ==="
	@echo ""
	@echo "--- Run 1: Apply the hardening playbook (should show 'changed' tasks) ---"
	docker compose exec lab bash -c '\
		ansible-playbook -i /lab/inventory /lab/data/playbook.yml 2>&1 | \
		grep -E "(PLAY|TASK|ok:|changed:|failed:|PLAY RECAP)"'
	@echo ""
	@echo "--- Run 2: Re-run for idempotency check (all tasks should be 'ok') ---"
	docker compose exec lab bash -c '\
		ansible-playbook -i /lab/inventory /lab/data/playbook.yml 2>&1 | \
		grep -E "(PLAY RECAP|ok=|changed=|failed=)"'
	@echo ""
	@echo "--- Drift simulation: modify a setting, then check mode shows drift ---"
	docker compose exec lab bash -c '\
		sed -i "s/PermitRootLogin no/PermitRootLogin yes/" /etc/ssh/sshd_config && \
		echo "Drift introduced: PermitRootLogin set to yes" && \
		ansible-playbook -i /lab/inventory /lab/data/playbook.yml --check 2>&1 | \
		grep -E "(changed:|PLAY RECAP)" && \
		echo "(Drift detected above. Re-running to fix...)" && \
		ansible-playbook -i /lab/inventory /lab/data/playbook.yml 2>&1 | \
		grep -E "(PLAY RECAP)"'
	@echo ""
	@echo "=== Run 'make shell' to explore the playbook and inventory ==="

shell:
	docker compose exec lab bash
