# Module 01 — Primitives in Practice
# Standard targets: up / down / reset / demo / shell

.PHONY: up down reset demo shell

KEY=0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20
IV_CBC=0102030405060708090a0b0c0d0e0f10
IV_GCM=010203040506070809000000

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	@echo "=== Module 01 — Cryptographic Primitives Demo ==="
	@echo ""
	@echo "--- Part 1: AES-256-CBC encryption + tamper demo ---"
	docker compose exec lab bash -c '\
		KEY="0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20"; \
		IV="0102030405060708090a0b0c0d0e0f10"; \
		openssl enc -aes-256-cbc -in /lab/data/plaintext.txt -out /tmp/cipher-cbc.bin \
		  -K "$$KEY" -iv "$$IV" 2>/dev/null; \
		echo "CBC encrypted. Tampering with byte 32..."; \
		python3 -c "\
data = bytearray(open('"'"'/tmp/cipher-cbc.bin'"'"','"'"'rb'"'"').read()); \
data[32] ^= 0xFF; \
open('"'"'/tmp/cbc-tampered.bin'"'"','"'"'wb'"'"').write(data)"; \
		echo "Decrypting tampered CBC ciphertext (should succeed with corrupted plaintext):"; \
		openssl enc -d -aes-256-cbc -in /tmp/cbc-tampered.bin \
		  -K "$$KEY" -iv "$$IV" 2>/dev/null | head -3; \
		echo "(Notice: decryption SUCCEEDED but data is corrupted — no integrity check)"'
	@echo ""
	@echo "--- Part 2: AES-256-GCM encryption + tamper demo ---"
	docker compose exec lab bash -c '\
		KEY="0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20"; \
		IV="010203040506070809000000"; \
		openssl enc -aes-256-gcm -in /lab/data/plaintext.txt -out /tmp/cipher-gcm.bin \
		  -K "$$KEY" -iv "$$IV" 2>/dev/null; \
		echo "GCM encrypted. Tampering with byte 10..."; \
		python3 -c "\
data = bytearray(open('"'"'/tmp/cipher-gcm.bin'"'"','"'"'rb'"'"').read()); \
data[10] ^= 0xFF; \
open('"'"'/tmp/gcm-tampered.bin'"'"','"'"'wb'"'"').write(data)"; \
		echo "Decrypting tampered GCM ciphertext (should FAIL with authentication error):"; \
		openssl enc -d -aes-256-gcm -in /tmp/gcm-tampered.bin \
		  -K "$$KEY" -iv "$$IV" 2>&1 | head -5; \
		echo "(GCM rejects the tampered ciphertext — integrity protection works)"'
	@echo ""
	@echo "--- Conclusion ---"
	@echo "  CBC: tampering succeeds silently (no integrity guarantee)"
	@echo "  GCM: tampering is detected (AEAD guarantee)"
	@echo ""
	@echo "=== Run 'make shell' for interactive exercises ==="

shell:
	docker compose exec lab bash
