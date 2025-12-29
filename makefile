
POETRY = poetry

.PHONY: clean_run
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

.PHONY: test
test_api:
	poetry run python -m uvicorn backend.main:app --reload --port 8001

.PHONY: builddocker
builddocker :
	docker build -t eco-backend -f backend/Dockerfile .
	docker run -p 8001:8001 eco-backend


.PHONY : front
test_front:
	python -m http.server 5500 --directory frontend

.PHONY: requirements
to_requi:
	pip freeze > backend/requirements.txt

.PHONY : frontgpt
front:
	cd frontendgpt && npm start

.PHONY: format
format:
	cd backend
	$(info [*] Code formatting...)
	$(POETRY) run isort .
	$(POETRY) run black .
	$(POETRY) run autopep8 --in-place --aggressive --aggressive --max-line-length 79 -r .



.PHONY : run_test
run_test:
	poetry run pytest -v

.PHONY : coverage
coverage:
	poetry run pytest --cov=backend -v > coverage_report.txt