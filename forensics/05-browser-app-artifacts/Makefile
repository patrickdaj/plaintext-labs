# Module 05 — Browser & Application Artifacts lab.
# Standard targets: up / down / reset / demo / shell
.PHONY: up down reset demo shell

up:  ## Build and start the hindsight + sqlite3 container
	docker compose up -d --build

down:  ## Stop and remove the container
	docker compose down

reset:  ## Tear down completely
	docker compose down --rmi local --volumes --remove-orphans

shell:  ## Open a shell in the lab container
	docker compose exec lab bash

demo:  ## Extract Chrome browser artifacts from data/History and display findings
	docker compose run --rm lab sh -c '\
		echo "=== Module 05 — Browser & Application Artifacts: worked demo ==="; \
		echo; \
		echo "-- Visited URLs (incident window 2024-03-15 02:00–02:35 UTC) --"; \
		sqlite3 data/History \
			"SELECT datetime(last_visit_time/1000000 - 11644473600, '"'"'unixepoch'"'"') as visited_at, \
			        url, visit_count \
			 FROM urls \
			 WHERE last_visit_time/1000000 - 11644473600 BETWEEN 1710464400 AND 1710466500 \
			 ORDER BY last_visit_time;"; \
		echo; \
		echo "-- Downloads --"; \
		sqlite3 data/History \
			"SELECT datetime(start_time/1000000 - 11644473600, '"'"'unixepoch'"'"') as dl_at, \
			        target_path, tab_url, total_bytes \
			 FROM downloads ORDER BY start_time;"; \
		echo; \
		echo "-- Search Terms --"; \
		sqlite3 data/History \
			"SELECT k.term, datetime(u.last_visit_time/1000000 - 11644473600, '"'"'unixepoch'"'"') \
			 FROM keyword_search_terms k JOIN urls u ON k.url_id = u.id \
			 ORDER BY u.last_visit_time;"; \
		echo; \
		echo "-- All URLs (full history) --"; \
		sqlite3 data/History \
			"SELECT datetime(last_visit_time/1000000 - 11644473600, '"'"'unixepoch'"'"'), url \
			 FROM urls ORDER BY last_visit_time;"; \
		echo; \
		echo "=== KEY FINDINGS ==="; \
		echo "  - Google searches for exfiltration methods and log clearing"; \
		echo "  - Visit to mega.nz and wetransfer.com (data exfiltration risk domains)"; \
		echo "  - Download of update_patch.exe from pastebin.com"; \
		echo "  - Navigation to \\\\meridian-fs01\\finance\\restricted before transfers"; \
		echo "=== Demo complete. ==="'
