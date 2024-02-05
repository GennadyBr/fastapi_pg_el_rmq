upv:
	sudo docker-compose up -d --build

downv:
	sudo docker-compose down --remove-orphans

psv:
	sudo docker-compose ps

up:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

ps:
	docker compose ps

al:
	sudo alembic upgrade heads

main:
	sudo python main.py

venv:
	sudo python3.11 -m venv venv

net:
	sudo docker network create nginx_proxy

5432:
	sudo lsof -i -P -n | grep 5432

8002:
	sudo lsof -i -P -n | grep 8002

log:
	sudo docker logs app_2402
