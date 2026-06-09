# Module 07 — Timeline Analysis lab.
# Standard targets: up / down / reset / demo / shell
.PHONY: up down reset demo shell l2t

up:  ## Build and start the plaso container
	docker compose up -d --build

down:  ## Stop and remove the container
	docker compose down

reset:  ## Tear down completely
	docker compose down --rmi local --volumes --remove-orphans

shell:  ## Open a shell in the lab container
	docker compose exec lab bash

demo:  ## Analyze pre-computed timeline (data/timeline.csv) and display incident narrative
	docker compose run --rm lab python3 analyze_timeline.py

# Run log2timeline against the bundled artifact directory
# Produces a plaso storage file, then exports a filtered incident-window CSV
l2t:  ## Run log2timeline + psort on data/artifacts/ (builds from raw artifacts)
	docker compose run --rm lab sh -c '\
		echo "=== Step 1: log2timeline.py — ingest artifacts ==="; \
		log2timeline.py /tmp/timeline.plaso data/artifacts/ 2>&1; \
		echo; \
		echo "=== Step 2: psort.py — export all events ==="; \
		psort.py -o l2tcsv /tmp/timeline.plaso 2>/dev/null | head -30; \
		echo; \
		echo "=== Step 3: psort.py — filter to incident window ==="; \
		psort.py -o l2tcsv \
			--slice "2024-03-15T02:00:00" \
			--slice_size 35 \
			/tmp/timeline.plaso 2>/dev/null | head -50; \
		echo; \
		echo "=== Demo complete. For richer analysis, use: make demo ==="'
