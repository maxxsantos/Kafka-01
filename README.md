# Kafka

This course is about Kafka

Link of course in Udemy platform: <https://www.udemy.com/course/apache-kafka-valdir/>

## Install Dependencies

```bash
make

#or

make install
```

## Up Applications with docker

```bash
make up
```

## Important

Change the IP address of the Kafka host in line 29 of the [kafka docker-compose](./kafka/docker-compose.yml).

After making this change, ensure to update the same IP address in [str_producer:main.py](./str_producer/str_producer/main.py) at line 8 and [str_consume:main.py](./str_consumer/str_consumer/main.py) at line 9 to maintain consistency.
