.PHONY: up down reset demo shell plan apply destroy

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec lab sh

demo:      ## Run tofu init and tofu plan against data/main.tf
	docker compose run --rm lab sh -c '\
		cd /lab/data && \
		echo "=== tofu init ===" && \
		tofu init && \
		echo && \
		echo "=== tofu plan ===" && \
		tofu plan'

plan:
	docker compose run --rm lab sh -c 'cd /lab/data && tofu plan -out=tfplan'

apply:
	docker compose run --rm lab sh -c 'cd /lab/data && tofu apply tfplan'

destroy:
	docker compose run --rm lab sh -c 'cd /lab/data && tofu destroy -auto-approve'
