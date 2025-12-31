POETRY = poetry


#clean files
.PHONY: clean_run
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete


#run the appl
.PHONY: test
test_api:
	poetry run python -m uvicorn backend.main:app --reload --port 8001

.PHONY: test
test_api2:
	python -m uvicorn backend.main:app --reload --port 8001

.PHONY : front
test_front:
	python -m http.server 5500 --directory frontend

.PHONY : front
front:
	cd frontend && npm start

#docker files
.PHONY: build
builddockerbackend :
	docker build -t eco-backend -f backend/Dockerfile .
	docker run -p 8001:8001 eco-backend

.PHONY: buildfront
builddockerfrontend :
	docker build -t eco-frontend -f frontend/Dockerfile .
	docker run -p 3000:3000 eco-frontend

.PHONY: buildfull
build:
	docker compose up --build

.PHONY: compose
compose:
	docker compose up

#tests and requirment
.PHONY : run_test
run_test:
	poetry run pytest -v

.PHONY : coverage
coverage:
	poetry run pytest --cov=backend -v > coverage_report.txt

.PHONY: requirements
to_requi:
	pip freeze > backend/requirements.txt

#formating files
.PHONY: format
format:
	cd backend
	$(info [*] Code formatting...)
	$(POETRY) run isort .
	$(POETRY) run black .
#$(POETRY) run autopep8 --in-place --aggressive --aggressive --max-line-length 79 -r .


.PHONY: formattest
formattest:
	cd backend
	$(info [*] Code formatting...)
	$(POETRY) run isort . --check-only
	$(POETRY) run black . --check