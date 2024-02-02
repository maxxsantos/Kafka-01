import asyncio
from fastapi import FastAPI, HTTPException
import uvicorn
from confluent_kafka import Producer
import json
import os

kafka_bootstrap_servers = '172.31.141.162:9092'
kafka_topic = 'teste'

app = FastAPI()

kafka_config = {
    'bootstrap.servers': kafka_bootstrap_servers,
    'client.id': 'json-producer'
}


producer = Producer(kafka_config)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


def delivery_report(err, msg):
    if err is not None:
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao enviar a mensagem para o Kafka: {str(err)}'
            )


@app.post("/produce")
async def send_to_kafka(message: dict):
    try:
        # Enviar mensagem para o tópico especificado
        json_message = json.dumps(message)

        producer.produce(
            kafka_topic,
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


def start():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    config = uvicorn.Config(
        app=app,
        loop="auto",
        port=os.getenv('API_PORT', 3000),
        host=os.getenv('API_HOST', '0.0.0.0')
    )
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == "__main__":
    start()
