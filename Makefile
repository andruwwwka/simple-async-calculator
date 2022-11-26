test:
	docker-compose up tests
	docker-compose down

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
ifdef env
ifeq ($(env), container)
	docker-compose up webapp
else
	poetry run uvicorn --host 0.0.0.0 simple_async_calculator.api.handlers:app --reload
endif
else
	uvicorn simple_async_calculator.api.handler:app
endif
