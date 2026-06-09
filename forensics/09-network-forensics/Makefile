.PHONY: up down reset demo shell pcap

up:
	docker compose up -d --build
	@echo "Container ready. Run 'make pcap' to generate the capture, then 'make demo'."

pcap:
	@docker compose exec lab python3 /scripts/gen_pcap.py
	@echo "capture.pcap written to data/"

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans
	rm -f data/capture.pcap

demo:
	@if [ ! -f data/capture.pcap ]; then \
		echo "Generating capture.pcap first..."; \
		docker compose exec lab python3 /scripts/gen_pcap.py; \
	fi
	docker compose exec lab sh /scripts/demo.sh

shell:
	docker compose exec lab bash
