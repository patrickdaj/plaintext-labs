.PHONY: up down reset demo shell create-image

up:
	docker compose up -d --build
	@echo "Container ready."
	@if [ ! -f data/disk.img ]; then \
		echo "disk.img not found — generating inside container..."; \
		docker compose exec lab python3 /scripts/create_ext2_img.py /data/disk.img; \
	fi
	@echo "Run 'make demo' to analyse the disk image."

create-image:
	docker compose exec lab python3 /scripts/create_ext2_img.py /data/disk.img

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	docker compose exec lab sh /scripts/demo.sh

shell:
	docker compose exec lab bash
