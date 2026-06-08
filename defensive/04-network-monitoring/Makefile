# Module 04 — Network Monitoring lab.
.PHONY: up down reset shell demo zeek
up:
	docker compose up -d --build
down:
	docker compose down
reset:
	docker compose down --rmi local --volumes --remove-orphans
shell:
	docker compose exec lab bash
demo:
	docker compose run --rm lab python3 analyze.py
# Run Zeek against a local PCAP: PCAP=my.pcap make zeek
zeek:
	docker compose --profile zeek run --rm zeek zeek -C -r /lab/$(PCAP)
