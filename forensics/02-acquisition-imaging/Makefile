# Module 02 — Acquisition & Imaging lab.
# Standard targets: up / down / reset / demo / shell
.PHONY: up down reset demo shell

up:  ## Build and start the dc3dd container
	docker compose up -d --build

down:  ## Stop and remove the container
	docker compose down

reset:  ## Tear down completely (container + local image + volumes)
	docker compose down --rmi local --volumes --remove-orphans

shell:  ## Open a shell in the lab container
	docker compose exec lab bash

demo:  ## Worked example: create 1MB source, image with dc3dd, verify hash
	docker compose run --rm lab sh -c '\
		echo "=== Module 02 — Acquisition & Imaging: worked demo ==="; \
		echo; \
		echo "-- Step 1: Create 1MB synthetic source device (random data) --"; \
		dd if=/dev/urandom of=/tmp/source.img bs=1M count=1 2>&1; \
		echo; \
		echo "-- Step 2: Image with dc3dd (SHA-256 inline) --"; \
		dc3dd if=/tmp/source.img of=/tmp/forensic-image.img hash=sha256 log=/tmp/acquisition.log 2>&1; \
		echo; \
		echo "-- Step 3: Acquisition log (inline hash proof) --"; \
		cat /tmp/acquisition.log; \
		echo; \
		echo "-- Step 4: Verify with sha256sum --"; \
		SRC=$$(sha256sum /tmp/source.img | cut -d" " -f1); \
		IMG=$$(sha256sum /tmp/forensic-image.img | cut -d" " -f1); \
		echo "Source hash : $$SRC"; \
		echo "Image hash  : $$IMG"; \
		if [ "$$SRC" = "$$IMG" ]; then \
			echo "RESULT: VERIFIED — source and image are identical"; \
		else \
			echo "RESULT: FAILED — hash mismatch, image is suspect"; \
		fi; \
		echo; \
		echo "=== Demo complete. ==="'
