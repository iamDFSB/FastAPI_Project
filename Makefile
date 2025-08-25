run-app:
	@echo "Start Running FastAPI"
	fastapi dev src/fast_zero/app.py --host 0.0.0.0 --port 8000

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
	@echo "Testing files"
	pytest --cov=src -vv

test-post:
	@echo "Updating html test file"
	coverage html