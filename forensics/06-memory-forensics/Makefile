# Module 06 — Memory Forensics lab.
# Standard targets: up / down / reset / demo / shell / analyze
.PHONY: up down reset demo shell analyze

up:  ## Build and start the Volatility3 container
	docker compose up -d --build

down:  ## Stop and remove the container
	docker compose down

reset:  ## Tear down completely
	docker compose down --rmi local --volumes --remove-orphans

shell:  ## Open a shell in the lab container
	docker compose exec lab bash

demo:  ## Analyze pre-processed Volatility3 output from data/memory-sample.json
	docker compose run --rm lab python3 analyze_memory.py

# To analyze a real memory image, place it at data/memory.img and run:
#   make analyze IMAGE=data/memory.img
analyze:  ## Run Volatility3 plugins against a real memory image (make analyze IMAGE=path/to/image)
	@if [ -z "$(IMAGE)" ]; then \
		echo "Usage: make analyze IMAGE=data/memory.img"; \
		exit 1; \
	fi
	docker compose run --rm lab sh -c '\
		echo "=== pslist ==="; \
		vol -f $(IMAGE) windows.pslist; \
		echo; \
		echo "=== pstree ==="; \
		vol -f $(IMAGE) windows.pstree; \
		echo; \
		echo "=== cmdline ==="; \
		vol -f $(IMAGE) windows.cmdline; \
		echo; \
		echo "=== netscan ==="; \
		vol -f $(IMAGE) windows.netscan; \
		echo; \
		echo "=== malfind ==="; \
		vol -f $(IMAGE) windows.malfind'
