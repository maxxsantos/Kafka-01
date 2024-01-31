from confluent_kafka import Consumer, KafkaError
import threading
import json


class KafkaConsumerThread(threading.Thread):
    def __init__(self, bootstrap_servers, group_id, topic):
        super().__init__()
        self.stop_event = threading.Event()
        self.messages = []

        conf = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        }

        self.consumer = Consumer(conf)
        self.topic = topic
        self.consumer.subscribe([self.topic])

    def run(self):
        try:
            while not self.stop_event.is_set():
                msg = self.consumer.poll(timeout=1000)

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue

                    print(f'Erro no consumo: {msg.error()}')
                    continue

                message_value = json.loads(msg.value().decode('utf-8'))
                self.messages.append(message_value)
                print(f'Mensagem recebida: {message_value}')

        except Exception as e:
            print(f'Erro na thread de consumo: {str(e)}')

    def stop(self):
        self.stop_event.set()
        self.consumer.close()
