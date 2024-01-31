
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

start-producer:
	cd str_producer && poetry run start

start-consumer:
	cd str_consumer && poetry run start

start-kafka:
	cd kafka && docker-compose up -d

down-kafka:
	cd kafka && docker-compose down
