all: format check test

format-black:
	@poetry run black custom_components/mealie tests/

format-isort:
	@poetry run isort custom_components/mealie tests/

format: format-black format-isort

check-black:
	@poetry run black --check custom_components/mealie tests/

check-isort:
	@poetry run isort --check-only custom_components/mealie tests/

check-flake8:
	@poetry run pflake8 custom_components/mealie tests/

check-mypy:
	@poetry run mypy custom_components/mealie tests/

check: check-black check-isort check-flake8 check-mypy

test:
	@poetry run pytest -sv --cov=custom_components tests/