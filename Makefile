run-app:
	@echo "Start Running FastAPI"
	fastapi dev src/fast_zero/app.py

ruff-check-dir:
	@echo "Checking the directory"
	ruff check .

ruff-check-fix:
	@echo "Fixing files in the directory"
	ruff check . --fix

ruff-format:
	@echo "Applying format to files"
	make ruff-check-fix && ruff format .

test:
	pytest --cov=src -vv

test-post:
	@echo "Updating html test file"
	coverage html