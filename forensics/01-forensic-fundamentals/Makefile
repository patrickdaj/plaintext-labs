# Module 01 — Forensic Fundamentals & Evidence Handling lab.
# No container required; dc3dd runs on the host or via Docker fallback.
# Standard targets: demo / clean
.PHONY: demo clean up down reset shell

# --- Worked example -------------------------------------------------------
demo:  ## Hash evidence files, image with dc3dd, and show chain-of-custody output
	@echo "=== Module 01 — Forensic Fundamentals: worked demo ==="; \
	echo; \
	echo "-- Step 1: SHA-256 hashes of both evidence files --"; \
	sha256sum data/evidence-sample.txt data/evidence-sample.bin; \
	echo; \
	echo "-- Step 2: MD5 hashes (still required by some courts) --"; \
	md5sum data/evidence-sample.txt data/evidence-sample.bin; \
	echo; \
	echo "-- Step 3: Image evidence-sample.bin with dc3dd (inline hash) --"; \
	if command -v dc3dd >/dev/null 2>&1; then \
		dc3dd if=data/evidence-sample.bin of=/tmp/evidence-sample.bin.img hash=sha256 log=/tmp/dc3dd.log 2>&1; \
		echo; \
		echo "-- dc3dd log (inline hash proof) --"; \
		cat /tmp/dc3dd.log; \
	else \
		echo "(dc3dd not installed — running via Docker)"; \
		docker run --rm -v "$(PWD)/data:/evidence:ro" \
			-v /tmp:/out \
			finchlabs/dc3dd:latest \
			dc3dd if=/evidence/evidence-sample.bin of=/out/evidence-sample.bin.img hash=sha256 log=/out/dc3dd.log 2>&1 || \
		echo "  [SKIP] dc3dd unavailable — install it or use the container: docker run --rm ..."; \
	fi; \
	echo; \
	echo "-- Step 4: Verify hash matches (sha256sum == dc3dd inline hash) --"; \
	echo "Compare the SHA-256 above with the hash in the dc3dd log."; \
	echo "If they match, the image is forensically verified."; \
	echo; \
	echo "=== Demo complete. ==="

clean:  ## Remove generated images and logs
	rm -f /tmp/evidence-sample.bin.img /tmp/dc3dd.log

# Stubs so standard 'make up/down/reset/shell' don't fail if called
up:
	@echo "No container needed for module 01. Run 'make demo' directly."
down:
	@true
reset:
	$(MAKE) clean
shell:
	@echo "No container for module 01. Run 'make demo' on your host."
