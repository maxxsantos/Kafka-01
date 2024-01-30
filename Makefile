
.PHONY: install

install: python-reqs-producer

python-reqs-producer:
	cd str_producer && poetry config virtualenvs.path --unset
	cd str_producer && poetry config virtualenvs.in-project true
	cd str_producer && poetry install
