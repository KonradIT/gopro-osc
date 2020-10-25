.PHONY: run
run:
	@pipenv run main
.PHONY: install-deps
install-deps:
	@pipenv install