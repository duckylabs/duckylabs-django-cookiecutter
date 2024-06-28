.PHONY:
upall: collectstatic
	@docker-compose up || true

.PHONY: up
up:
	@docker-compose run --service-ports --rm backend bash || true

.PHONY: up-prod
up-prod:
	@docker-compose run --service-ports --rm webserver || true

.PHONY: bash
bash:
	@docker exec -it $$(docker ps --no-trunc|grep {{cookiecutter.project_slug}}|grep -E "_run_|bash"|awk '{ print $$1 }') bash || true

.PHONY: test
test:
	@docker-compose run --rm backend dev test || true

.PHONY: testcov
testcov:
	@docker-compose run --rm backend dev pycoverage || true

.PHONY: coverage
coverage:
	@rm -rf .coverage
	@docker-compose run --rm backend dev coverage || true

.PHONY: devserver
devserver:
	@docker-compose run --service-ports --rm backend dev run || true

.PHONY: collectstatic
collectstatic:
	@docker-compose run --rm backend collectstatic || true

.PHONY: makemigrations
makemigrations:
	@docker-compose run --rm backend makemigrations || true

.PHONY: migrate
migrate:
	@docker-compose run --rm backend migrate || true

.PHONY: stop
stop:
	@docker-compose stop

.PHONY: down
down:
	@docker-compose down --remove-orphans

.PHONY: build
build: compile-requirements
	@docker-compose build

.PHONY: init-setup
init-setup: build makemigrations migrate
	@docker-compose run --rm backend python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); users = User.objects.filter(username='admin@admin.com', email='admin@admin.com'); user = users[0] if users else User.objects.create_superuser(username='admin@admin.com', email='admin@admin.com', password='adminpass'); user.set_password('adminpass'); user.is_staff=True; user.is_superuser=True; user.is_active=True; user.save()"
	@echo "superuser created. Username=admin@admin.com, Email=admin@admin.com, Password=adminpass"

.PHONY: compile-requirements
compile-requirements:
	@pip-compile requirements.in --output-file=requirements.txt
	@pip-compile requirements-dev.in --output-file=requirements-dev.txt

.PHONY:
install-local-dependencies:
	@echo "Installing pre-commit..."
	@pip install pre-commit
	@pip install pip-tools
	@pre-commit install
