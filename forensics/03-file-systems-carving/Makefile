# Module 03 — File Systems & Carving lab.
# Standard targets: up / down / reset / demo / shell
.PHONY: up down reset demo shell

up:  ## Build and start the SleuthKit + foremost container
	docker compose up -d --build

down:  ## Stop and remove the container
	docker compose down

reset:  ## Tear down completely
	docker compose down --rmi local --volumes --remove-orphans

shell:  ## Open a shell in the lab container
	docker compose exec lab bash

demo:  ## Worked example: parse disk.img, list deleted files, recover content, carve
	docker compose run --rm lab sh -c '\
		echo "=== Module 03 — File Systems & Carving: worked demo ==="; \
		echo; \
		echo "-- Step 1: Filesystem summary (fsstat) --"; \
		fsstat data/disk.img 2>&1 | head -30; \
		echo; \
		echo "-- Step 2: All files including deleted (fls -r -d) --"; \
		fls -r -d data/disk.img 2>&1; \
		echo; \
		echo "-- Step 3: Recover the deleted file via icat --"; \
		echo "(Deleted file is at inode 4 in this FAT32 image)"; \
		icat data/disk.img 4 2>/dev/null | cat; \
		echo; \
		echo "-- Step 4: Carve unallocated space with foremost --"; \
		mkdir -p /tmp/foremost-out; \
		foremost -t all -i data/disk.img -o /tmp/foremost-out/ 2>&1; \
		echo; \
		echo "-- foremost audit summary --"; \
		cat /tmp/foremost-out/audit.txt 2>/dev/null || echo "(no audit.txt — check foremost output)"; \
		echo; \
		echo "=== Demo complete. The deleted EXFIL.TXT content should appear above. ==="'
