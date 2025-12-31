POETRY = poetry

# clean files
.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# run the app
.PHONY: test_api
test_api:
	cd backend && $(POETRY) run python -m uvicorn main:app --reload --port 8001

.PHONY: test_api2
test_api2:
	cd backend && python -m uvicorn main:app --reload --port 8001

.PHONY: test_front
test_front:
	python -m http.server 5500 --directory frontend

.PHONY: front
front:
	cd frontend && npm start

# docker files
.PHONY: builddockerbackend
builddockerbackend:
	docker build -t eco-backend -f backend/Dockerfile .
	docker run -p 8001:8001 eco-backend

.PHONY: builddockerfrontend
builddockerfrontend:
	docker build -t eco-frontend -f frontend/Dockerfile .
	docker run -p 3000:3000 eco-frontend

.PHONY: build
build:
	docker compose up --build

.PHONY: compose
compose:
	docker compose up

.PHONY: down
down:
	docker compose down

# tests and requirements
.PHONY: run_test_old
run_test_old:
	$(POETRY) run pytest -v


.PHONY: run_test
run_test:
	@VENV_BIN=$$(poetry -C backend env info --path)/bin/python; \
	export PYTHONPATH=$(shell pwd); \
	$$VENV_BIN -m pytest backend/tests -v

.PHONY: coverage
coverage:
	cd backend && $(POETRY) run pytest --cov=. -v > ../coverage_report.txt

.PHONY: to_requi
to_requi:
	cd backend && pip freeze > requirements.txt

# formatting files
.PHONY: format
format:
	@$(info [*] Code formatting...)
	cd backend && $(POETRY) run isort . && $(POETRY) run black .

.PHONY: formattest
formattest:
	@$(info [*] Code formatting check...)
	cd backend && $(POETRY) run isort . --check-only && $(POETRY) run black . --check


#$(POETRY) run autopep8 --in-place --aggressive --aggressive --max-line-length 79 -r .

