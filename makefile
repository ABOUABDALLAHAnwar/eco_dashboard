
POETRY = poetry

.PHONY: clean_run
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

.PHONY: test
test_api:
	uvicorn backend.main:app --reload --port 8001

.PHONY : front
test_front:
	python -m http.server 5500 --directory frontend

.PHONY: requirements
to_requi:
	pip freeze > backend/requirements.txt
