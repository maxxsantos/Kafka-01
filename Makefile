
.PHONY: install

install: python-reqs-producer python-reqs-consumer

python-reqs-producer:
	cd str_producer && poetry config virtualenvs.path --unset
	cd str_producer && poetry config virtualenvs.in-project true
	cd str_producer && poetry install

python-reqs-consumer:
	cd str_consumer && poetry config virtualenvs.path --unset
	cd str_consumer && poetry config virtualenvs.in-project true
	cd str_consumer && poetry install


up: start-kafka start-producer start-consumer


down: down-kafka down-producer down-consumer


start-producer:
	cd str_producer && docker-compose up -d

down-producer:
	cd str_producer && docker-compose down

start-consumer:
	cd str_consumer && docker-compose up -d

down-consumer:
	cd str_consumer && docker-compose down

start-kafka:
	cd kafka && docker-compose up -d

down-kafka:
	cd kafka && docker-compose down
