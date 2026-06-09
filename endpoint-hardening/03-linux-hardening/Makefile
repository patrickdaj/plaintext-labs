# Module 03 — Linux Hardening to CIS
# Standard targets: up / down / reset / demo / shell

.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	@echo "=== Module 03 — Linux Hardening to CIS ==="
	@echo ""
	@echo "--- Part 1: Lynis audit ---"
	docker compose exec lab bash -c '\
		lynis audit system --no-colors --quiet 2>/dev/null | \
		grep -E "(Hardening index|WARNING|Suggestion)" | head -20; \
		echo ""; \
		score=$$(lynis audit system --no-colors --quiet 2>/dev/null | grep "Hardening index" | grep -oP "[0-9]+(?= \[)"); \
		echo "Lynis hardening index: $${score}/100"'
	@echo ""
	@echo "--- Part 2: OpenSCAP CIS Level 1 profile scan ---"
	docker compose exec lab bash -c '\
		oscap xccdf eval \
		  --profile xccdf_org.ssgproject.content_profile_cis_level1_server \
		  --results /tmp/results.xml \
		  /usr/share/xml/scap/ssg/content/ssg-ubuntu2204-ds.xml 2>/dev/null; \
		fail=$$(grep -c '"'"'result>fail'"'"' /tmp/results.xml 2>/dev/null || echo 0); \
		pass=$$(grep -c '"'"'result>pass'"'"' /tmp/results.xml 2>/dev/null || echo 0); \
		total=$$((fail + pass)); \
		echo "OpenSCAP CIS Level 1: $${pass}/$${total} controls pass"'
	@echo ""
	@echo "=== Run 'make shell' to explore further ==="

shell:
	docker compose exec lab bash
