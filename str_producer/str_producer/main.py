import asyncio
from fastapi import FastAPI, HTTPException
import uvicorn
from confluent_kafka import Producer
import json
from confluent_kafka.admin import AdminClient, NewTopic


kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'teste'
num_partitions = 3
num_replicas = 2

app = FastAPI()

kafka_config = {
    'bootstrap.servers': kafka_bootstrap_servers,
    'client.id': 'json-producer'
}


producer = Producer(kafka_config)


@app.get("/")
def read_root():
    return {"Hello": "World"}


def delivery_report(err, msg):
    if err is not None:
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao enviar a mensagem para o Kafka: {str(err)}'
            )


@app.post("/send/{key}")
async def send_to_kafka(key: str, message: dict):
    try:
        # Enviar mensagem para o tópico especificado
        json_message = json.dumps(message)

        topic_config = {
            'num_partitions': num_partitions,
            'replication_factor': num_replicas
        }

        create_topic(kafka_bootstrap_servers, kafka_topic, topic_config)

        producer.produce(
            kafka_topic,
            key=key,
            value=json_message,
            callback=delivery_report
            )
        producer.flush()

        return {
            "status": "Mensagem enviada com sucesso para o tópico {}"
            .format(kafka_topic)
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_topic(bootstrap_servers, topic, config):

    admin_config = {
        'bootstrap.servers': bootstrap_servers,
    }

    admin = AdminClient(admin_config)

    # Verifica se o tópico já existe
    topics = admin.list_topics().topics
    if topic not in topics:
        # Criação do tópico com as configurações desejadas
        new_topic = NewTopic(topic, **config)
        admin.create_topics([new_topic])


def start():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    config = uvicorn.Config(
        app=app,
        loop="auto",
        port=3000,
        host="localhost"
    )
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == "__main__":
    start()
