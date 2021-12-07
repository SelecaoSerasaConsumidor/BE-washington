db-migrate-user:
	flask db migrate -d user_api/adapters/gateway/sql/migrations

db-update-user:
	flask db update -d user_api/adapters/gateway/sql/migrations

db-migrate-order:
	flask db migrate -d order_api/adapters/gateway/sql/migrations

db-update-order:
	flask db update -d order_api/adapters/gateway/sql/migrations

run:
	export ENV=dev
	flask run

all-db:
	docker-compose -f user_api/docker-compose.yml up -d
	docker-compose -f order_api/docker-compose.yml up -d

user-db:
	docker-compose -f user_api/docker-compose.yml up -d

order-db:
	docker-compose -f order_api/docker-compose.yml up -d
