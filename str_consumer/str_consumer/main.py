import asyncio
from fastapi import FastAPI
from .kafka_consumer import KafkaConsumerThread
import uvicorn
import os

app = FastAPI()

bootstrap_servers = '172.31.141.162:9092'
group_id = 'group-1'
topic = 'teste'

consumer_thread = KafkaConsumerThread(bootstrap_servers, group_id, topic)
consumer_thread.start()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get('/consume', response_model=dict)
def consume_messages():
    messages_copy = list(consumer_thread.messages)
    return {'messages': messages_copy}


def start():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    config = uvicorn.Config(
        app=app,
        loop="auto",
        port=os.getenv('API_PORT', 4000),
        host=os.getenv('API_HOST', '0.0.0.0')
    )
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == '__main__':
    start()
