# Module 07 — Compliance Scoring & Auditing
# Standard targets: up / down / reset / demo / shell

.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	@echo "=== Module 07 — Compliance Scoring & Auditing Demo ==="
	@echo ""
	@echo "--- BEFORE: Lynis audit (un-hardened container) ---"
	docker compose exec lab bash -c '\
		lynis audit system --no-colors --quiet 2>/dev/null | \
		grep -E "Hardening index|WARNING" | head -10; \
		echo ""'
	@echo ""
	@echo "--- BEFORE: OpenSCAP CIS Level 1 scan ---"
	docker compose exec lab bash -c '\
		oscap xccdf eval \
		  --profile xccdf_org.ssgproject.content_profile_cis_level1_server \
		  --results /tmp/results-before.xml \
		  /usr/share/xml/scap/ssg/content/ssg-ubuntu2204-ds.xml 2>/dev/null; \
		fail_before=$$(grep -c '"'"'result>fail'"'"' /tmp/results-before.xml 2>/dev/null || echo 0); \
		pass_before=$$(grep -c '"'"'result>pass'"'"' /tmp/results-before.xml 2>/dev/null || echo 0); \
		echo "Before — Failing controls: $${fail_before} | Passing controls: $${pass_before}"'
	@echo ""
	@echo "--- Applying one remediation: Enable ASLR ---"
	docker compose exec lab bash -c '\
		echo "kernel.randomize_va_space=2" >> /etc/sysctl.conf && \
		sysctl -p /etc/sysctl.conf 2>/dev/null && \
		echo "ASLR enabled: $(sysctl -n kernel.randomize_va_space)"'
	@echo ""
	@echo "--- AFTER: OpenSCAP re-scan ---"
	docker compose exec lab bash -c '\
		oscap xccdf eval \
		  --profile xccdf_org.ssgproject.content_profile_cis_level1_server \
		  --results /tmp/results-after.xml \
		  /usr/share/xml/scap/ssg/content/ssg-ubuntu2204-ds.xml 2>/dev/null; \
		fail_after=$$(grep -c '"'"'result>fail'"'"' /tmp/results-after.xml 2>/dev/null || echo 0); \
		pass_after=$$(grep -c '"'"'result>pass'"'"' /tmp/results-after.xml 2>/dev/null || echo 0); \
		echo "After  — Failing controls: $${fail_after} | Passing controls: $${pass_after}"; \
		echo ""; \
		fail_before=$$(grep -c '"'"'result>fail'"'"' /tmp/results-before.xml 2>/dev/null || echo 0); \
		echo "Delta: $$((fail_before - fail_after)) controls fixed"'
	@echo ""
	@echo "=== Run 'make shell' for interactive audit exploration ==="

shell:
	docker compose exec lab bash
