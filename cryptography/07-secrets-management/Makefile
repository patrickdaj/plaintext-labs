# Module 07 — Secrets Management
# Standard targets: up / down / reset / demo / shell

.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	@echo "=== Module 07 — Secrets Management Demo ==="
	@echo ""
	@echo "--- Part 1: Vault — store, read, rotate a secret ---"
	docker compose exec lab sh -c '\
		echo "== Vault status =="; \
		vault status 2>/dev/null | grep -E "(Sealed|Version|HA Enabled)"; \
		echo ""; \
		echo "== Storing database credential =="; \
		vault kv put secret/meridian/payroll/db \
		  username=payroll_svc password=initial-db-password 2>/dev/null; \
		echo ""; \
		echo "== Reading credential =="; \
		vault kv get secret/meridian/payroll/db; \
		echo ""; \
		echo "== Rotating credential =="; \
		vault kv put secret/meridian/payroll/db \
		  username=payroll_svc password=rotated-db-password-v2 2>/dev/null; \
		vault kv get -field=password secret/meridian/payroll/db; \
		echo ""; \
		echo "== Version history =="; \
		vault kv metadata get secret/meridian/payroll/db | grep current_version'
	@echo ""
	@echo "--- Part 2: SOPS — encrypt a YAML config file ---"
	docker compose exec lab bash -c '\
		age-keygen -o /tmp/age-key.txt 2>/dev/null; \
		pub=$$(age-keygen -y /tmp/age-key.txt 2>/dev/null); \
		cat > /tmp/config.yml <<EOF
database:
  host: db.meridian.internal
  username: payroll_svc
  password: super-secret-password
api_key: sk-meridian-prod-12345
EOF
		export SOPS_AGE_KEY_FILE=/tmp/age-key.txt; \
		sops --encrypt --age "$$pub" /tmp/config.yml > /tmp/config.enc.yml; \
		echo "Encrypted config (values encrypted, keys visible):"; \
		cat /tmp/config.enc.yml | head -15; \
		echo ""; \
		echo "Decrypted (original values):"; \
		sops --decrypt /tmp/config.enc.yml'
	@echo ""
	@echo "=== Run 'make shell' for the full Vault policy and rotation exercises ==="

shell:
	docker compose exec lab bash
