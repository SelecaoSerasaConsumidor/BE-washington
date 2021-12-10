all-app-run-build:
	docker-compose -f user_api/docker-compose.yml up --build -d
	docker-compose -f order_api/docker-compose.yml up --build -d

all-app-run:
	docker-compose -f user_api/docker-compose.yml up -d
	docker-compose -f order_api/docker-compose.yml up -d

all-db:
	flask db upgrade -d user_api/adapters/gateway/sql/migrations
	flask db upgrade -d order_api/adapters/gateway/sql/migrations

user-db-migrate:
	flask db migrate -d user_api/adapters/gateway/sql/migrations

user-db-upgrade:
	flask db upgrade -d user_api/adapters/gateway/sql/migrations

order-db-migrate:
	flask db migrate -d order_api/adapters/gateway/sql/migrations

order-db-update:
	flask db upgrade -d order_api/adapters/gateway/sql/migrations