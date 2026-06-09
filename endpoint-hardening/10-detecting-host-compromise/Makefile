# Module 10 — Detecting Host Compromise
# Standard targets: up / down / reset / demo / shell

.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	@echo "=== Module 10 — Detecting Host Compromise ==="
	@echo ""
	@echo "--- Alert data: Meridian payroll server (last 24h) ---"
	docker compose exec lab bash -c '\
		python3 -c "
import json
with open('"'"'data/alerts.json'"'"') as f:
    alerts = json.load(f)
print(f'"'"'Total alerts: {len(alerts)}'"'"')
print()
for a in alerts:
    level = a['"'"'rule'"'"']['"'"'level'"'"']
    desc = a['"'"'rule'"'"']['"'"'description'"'"']
    ts = a['"'"'timestamp'"'"']
    mitre = a.get('"'"'mitre'"'"', {}).get('"'"'id'"'"', '"'"'N/A'"'"')
    print(f'"'"'  [{level:2}] {ts} | ATT&CK: {mitre:15} | {desc}'"'"')
"'
	@echo ""
	@echo "--- Running example detection rule (cron persistence) ---"
	docker compose exec lab bash -c '\
		python3 detect.py --rule data/example-rule.yml --alerts data/alerts.json'
	@echo ""
	@echo "--- Convert example rule to Splunk SPL ---"
	docker compose exec lab bash -c '\
		sigma convert -t splunk data/example-rule.yml 2>/dev/null || \
		echo "(sigma-cli: use '\''sigma convert -t splunk <rule.yml>'\'' to convert rules)"'
	@echo ""
	@echo "=== Run 'make shell' to write your own detection rules ==="
	@echo "    Hint: write rules/persistence-cron.yml, rules/credential-shadow.yml, rules/lateral-ssh.yml"

shell:
	docker compose exec lab bash
