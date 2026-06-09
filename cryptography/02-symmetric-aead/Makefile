# Module 02 — Symmetric & AEAD
# Standard targets: up / down / reset / demo / shell

.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	@echo "=== Module 02 — Symmetric Encryption & AEAD Demo ==="
	@echo ""
	@echo "--- Part 1: GCM IV reuse attack ---"
	docker compose exec lab python3 -c "
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

key = os.urandom(32)
BAD_IV = b'\x00' * 12  # hardcoded IV — the bug

msg1 = b'Salary: \$95,000 '
msg2 = b'Budget: \$200,000'

ct1 = AESGCM(key).encrypt(BAD_IV, msg1, None)
ct2 = AESGCM(key).encrypt(BAD_IV, msg2, None)

# XOR the ciphertexts (first 16 bytes = ciphertext, last 16 = tag)
xor_ct = bytes(a ^ b for a, b in zip(ct1[:16], ct2[:16]))
xor_pt = bytes(a ^ b for a, b in zip(msg1, msg2))

print('IV reuse attack:')
print(f'  XOR of ciphertexts: {xor_ct.hex()}')
print(f'  XOR of plaintexts:  {xor_pt.hex()}')
print(f'  Match: {xor_ct == xor_pt}')
print()
print('An attacker who knows msg1 can recover msg2 by XOR-ing with ct1 XOR ct2.')
"
	@echo ""
	@echo "--- Part 2: Correct implementation (random IV per encryption) ---"
	docker compose exec lab python3 -c "
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, base64, json

key = os.urandom(32)
msg = b'Salary: \$95,000 for Q3 payroll'

# Two encryptions of the same message — IVs MUST differ
iv1 = os.urandom(12)
iv2 = os.urandom(12)

ct1 = AESGCM(key).encrypt(iv1, msg, None)
ct2 = AESGCM(key).encrypt(iv2, msg, None)

print('Correct (random IV per encryption):')
print(f'  Encryption 1 IV: {iv1.hex()}')
print(f'  Encryption 2 IV: {iv2.hex()}')
print(f'  IVs differ: {iv1 != iv2}')
print(f'  Ciphertexts differ: {ct1[:16].hex() != ct2[:16].hex()}')
print()
print('No IV reuse — XOR attack fails.')
"
	@echo ""
	@echo "=== Run 'make shell' for the full IV reuse and AAD exercises ==="

shell:
	docker compose exec lab bash
