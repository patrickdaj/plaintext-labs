.PHONY: demo shell down reset scan

IMAGE = plaintext/trufflehog:1.0

demo:      ## Build the image and run trufflehog against data/seed-repo/
	docker build -t $(IMAGE) .
	docker run --rm -v "$(PWD)/data/seed-repo:/scan:ro" $(IMAGE) \
		git file:///scan --no-update

shell:     ## Shell inside the built container
	docker run --rm -it --entrypoint bash $(IMAGE)

down:      ## Remove the image
	docker image rm -f $(IMAGE)

reset: down

scan:      ## make scan DIR=/path/to/repo — scan an arbitrary repo
	docker run --rm -v "$(DIR):/scan:ro" $(IMAGE) \
		git file:///scan --no-update
