.PHONY: up down reset demo shell trigger-high trigger-critical import-workflow export-workflow

OLLAMA_MODEL ?= tinyllama
N8N_URL ?= http://localhost:5678

up:        ## Start n8n and Ollama, pull model, import workflow
	docker compose up -d
	@echo "Waiting for services to start..."
	@docker compose run --rm lab sh -c '\
		pip install -q requests 2>/dev/null; \
		python3 -c " \
import requests, time; \
for svc, url in [(\"Ollama\",\"http://ollama:11434/api/tags\"),(\"n8n\",\"http://n8n:5678/healthz\")]: \
    for i in range(60): \
        try: requests.get(url, timeout=2); print(svc+\" ready.\"); break \
        except: time.sleep(2) \
    else: print(svc+\" not ready - check docker compose logs\") \
requests.post(\"http://ollama:11434/api/pull\", json={\"name\":\"$(OLLAMA_MODEL)\"}, timeout=600); \
print(\"Setup complete. n8n UI: http://localhost:5678\") \
"'
	@echo "Import the workflow manually via the n8n UI:"
	@echo "  1. Open http://localhost:5678"
	@echo "  2. Create new workflow → Import → paste contents of data/ai-playbook.json"
	@echo "  Or run: make import-workflow"

down:      ## Stop containers
	docker compose down

reset:     ## Tear down completely
	docker compose down --rmi local --volumes --remove-orphans

shell:     ## Open a shell in the lab container
	docker compose exec lab bash

import-workflow:  ## Import the AI playbook workflow into n8n via API
	@docker compose run --rm lab sh -c '\
		pip install -q requests 2>/dev/null; \
		python3 -c " \
import requests, json, time; \
# Wait for n8n \
for i in range(30): \
    try: requests.get(\"http://n8n:5678/healthz\", timeout=2); break \
    except: time.sleep(3) \
with open(\"data/ai-playbook.json\") as f: wf = json.load(f); \
r = requests.post(\"http://n8n:5678/rest/workflows\", json=wf, timeout=30); \
if r.status_code in (200,201): \
    wf_id = r.json().get(chr(100)+chr(97)+chr(116)+chr(97),{}).get(chr(105)+chr(100)); \
    print(f\"Workflow imported. ID: {wf_id}\"); \
    if wf_id: \
        requests.patch(f\"http://n8n:5678/rest/workflows/{wf_id}\", json={\"active\":True}); \
        print(\"Workflow activated.\") \
else: \
    print(f\"Import failed: {r.status_code} {r.text[:200]}\") \
"'

demo:      ## Send a HIGH-severity alert and show the routing decision
	@echo "=== SOAR + AI Demo — HIGH severity alert ==="
	@docker compose run --rm lab sh -c '\
		pip install -q requests 2>/dev/null; \
		python3 scripts/trigger.py --severity HIGH'

trigger-high:     ## Trigger the workflow with a HIGH-severity test alert
	docker compose run --rm lab sh -c 'pip install -q requests 2>/dev/null && python3 scripts/trigger.py --severity HIGH'

trigger-critical: ## Trigger the workflow with a CRITICAL-severity test alert
	docker compose run --rm lab sh -c 'pip install -q requests 2>/dev/null && python3 scripts/trigger.py --severity CRITICAL'

export-workflow:  ## Export the current workflow from n8n (after UI edits)
	@docker compose run --rm lab sh -c '\
		pip install -q requests 2>/dev/null; \
		python3 -c " \
import requests, json; \
r = requests.get(\"http://n8n:5678/rest/workflows\", timeout=10); \
workflows = r.json().get(chr(100)+chr(97)+chr(116)+chr(97), []); \
if not workflows: print(\"No workflows found.\"); exit(1); \
wf = workflows[0]; \
with open(\"data/ai-playbook.json\",\"w\") as f: json.dump(wf, f, indent=2); \
print(f\"Exported workflow: {wf.get(chr(110)+chr(97)+chr(109)+chr(101))}\") \
"'
