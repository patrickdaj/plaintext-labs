# Defensive Module 13 — PowerShell Logging & Hunting lab.
# Standard targets every reference lab provides: up / down / reset / demo [/ shell].
.PHONY: up down reset shell demo hunt

up:        ## Build and start the lab container
	docker compose up -d --build

down:      ## Stop and remove the container
	docker compose down

reset:     ## Tear down completely (container + local image)
	docker compose down --rmi local --volumes --remove-orphans

shell:     ## Open a PowerShell prompt in the lab container
	docker compose exec lab pwsh

demo:      ## Worked hunt: flag the malicious script blocks in the bundled 4104 log
	docker compose run --rm lab pwsh -NoProfile -File /lab/hunt.ps1

hunt:      ## make hunt FILE=mylog.json — run the hunt against your own 4104 export
	docker compose run --rm lab pwsh -NoProfile -File /lab/hunt.ps1 -Path $(FILE)
