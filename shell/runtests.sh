poetry run coverage run --source=./simple_async_calculator -m pytest --junitxml=pytest.xml
poetry run coverage report -m --fail-under=100 --skip-covered | tee pytest-coverage.txt