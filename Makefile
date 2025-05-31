# Docker Compose Commands

# Start all services
up:
	docker compose -f docker-compose.yml up

# Start all services with Ollama
up-ollama:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up

# Build and start all services
build-up:
	docker compose -f docker-compose.yml up --build

# Build and start all services with Ollama
build-up-ollama:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up --build

# Stop all services
down:
	docker compose down

# Stop all services including Ollama
down-ollama:
	docker compose -f docker-compose.yml -f docker-compose.override.yml down

# View logs
logs:
	docker compose logs -f

# View logs for specific service
logs-inference:
	docker compose logs -f inference-app

logs-crud:
	docker compose logs -f crud-app

logs-frontend:
	docker compose logs -f frontend

logs-qdrant:
	docker compose logs -f qdrant

logs-ollama:
	docker-compose logs -f ollama

# Rebuild specific services
build-inference:
	docker compose build inference-app

build-crud:
	docker compose build crud-app

build-frontend:
	docker compose build frontend

# Clean up
clean:
	docker compose down -v --remove-orphans
	docker system prune -f

# Development helpers
dev-inference:
	docker compose up -d qdrant
	docker compose up inference-app

dev-crud:
	docker compose up -d qdrant
	docker compose up crud-app

dev-frontend:
	docker compose up -d inference-app crud-app
	docker compose up frontend

# Health checks
status:
	docker compose ps

# Enter container shell
shell-inference:
	docker compose exec inference-app /bin/bash

shell-crud:
	docker compose exec crud-app /bin/bash

shell-frontend:
	docker compose exec frontend /bin/sh

shell-qdrant:
	docker compose exec qdrant /bin/bash

shell-ollama:
	docker compose exec ollama /bin/bash