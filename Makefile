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
ifdef reload
	uvicorn src.simple_async_calculator.cli:app --reload
else
	uvicorn src.simple_async_calculator.cli:app
endif

run-db:
	docker run -e POSTGRES_USER=calc -e POSTGRES_PASSWORD=calc -e POSTGRES_DB=calc_db -p 5432:5432 postgres:15.1
