# Offensive Module 15 — PowerShell Offensive Tradecraft lab.
# Standard targets every reference lab provides: up / down / reset / demo [/ shell].
.PHONY: up down reset shell demo

up:        ## Build and start the lab (payload host + attacker box)
	docker compose up -d --build

down:      ## Stop and remove the containers
	docker compose down

reset:     ## Tear down completely (containers + local image)
	docker compose down --rmi local --volumes --remove-orphans

shell:     ## Open a PowerShell prompt in the attacker container
	docker compose exec attacker pwsh

demo:      ## Worked example: cradle → encoded → obfuscated → the 4104 log it all emits
	docker compose up -d --build
	docker compose exec -T attacker pwsh -NoProfile -File /lab/demo.ps1
