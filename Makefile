all: format check test

format-black:
	@black custom_components/mealie tests/

format-isort:
	@isort custom_components/mealie tests/

format: format-black format-isort

check-black:
	@black --check custom_components/mealie tests/

check-isort:
	@isort --check-only custom_components/mealie tests/

check-flake8:
	@pflake8 custom_components/mealie tests/

check-mypy:
	@mypy custom_components/mealie tests/

check: check-black check-isort check-flake8 check-mypy

test:
	@pytest --cov=recap tests/