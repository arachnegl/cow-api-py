start:
	docker-compose up --build -d

test:
	docker-compose exec app pytest

stop:
	docker-compose down --volumes --remove-orphans
