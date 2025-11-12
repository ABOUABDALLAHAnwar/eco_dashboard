
POETRY = poetry

.PHONY: clean run
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

.PHONY: test
test_api:
	uvicorn backend.main:app --reload

.PHONY : front
test_front:
	cd frontend

	python -m http.server 5500