poetry run coverage run
(echo "coverage: platform" && poetry run coverage report) | tee pytest-coverage.txt