COMPOSE_DEV  = docker compose -f docker/compose.yml -f docker/compose.override.yml
COMPOSE_PROD = docker compose -f docker/compose.yml -f docker/compose.prod.yml

# --- Development ---
dev:
	$(COMPOSE_DEV) up

dev-seed:
	$(COMPOSE_DEV) exec backend python manage.py seed_data

dev-build:
	$(COMPOSE_DEV) up --build

dev-migrate:
	$(COMPOSE_DEV) exec backend python manage.py migrate
dev-down:
	$(COMPOSE_DEV) down


# --- Production ---
prod:
	$(COMPOSE_PROD) up -d
	
prod-build:
	$(COMPOSE_PROD) up -d --build

prod-logs:
	$(COMPOSE_PROD) logs -f

prod-migrate:
	$(COMPOSE_PROD) exec backend python manage.py migrate

prod-static:
	$(COMPOSE_PROD) exec backend python manage.py collectstatic --noinput

prod-down:
	$(COMPOSE_PROD) down


prod-seed:
	$(COMPOSE_PROD) exec backend python manage.py seed_data 

# --- Clean Down ---
down:
	docker compose -f docker/compose.yml down
