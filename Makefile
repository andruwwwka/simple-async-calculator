test:
	poetry run pytest --junitxml=pytest.xml --cov-report=term-missing:skip-covered --cov=src --cov-fail-under=100

formatter:
	isort .
	black .

mypy:
	poetry run mypy .

pylint:
	poetry run pylint --recursive=y .

all-checks: formatter mypy pylint test

install-deps:
ifdef deps
ifeq ($(deps), production)
	poetry install --without dev
else
	poetry install --with $(deps) --without dev
endif
else
	poetry install --with test,pylint,mypy
endif

runserver:
ifeq ($(env), dev)
	docker-compose up webapp
else
	uvicorn simple_async_calculator.api.handler:app
endif
