up:
	docker-compose -p async up -d

build:
	docker network create infra_default || true
	docker network create async_network || true
	docker-compose -p async build

stop:
	docker-compose -p async stop

down:
	docker-compose -p async down

reload:
	docker exec -ti async_application_1 sh_scripts/reload_gunicorn.sh

restart:
	docker restart async_application_1

logs-app:
	docker logs --tail=200 async_application_1

tests:
	docker exec -ti async_application_1 python -m unittest
