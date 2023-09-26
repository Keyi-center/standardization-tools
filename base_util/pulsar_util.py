import pulsar
import requests
import json

class Producer(object):
    def __init__(self, topic,pulsar_url):
        self.topic = topic
        self.client = pulsar.Client(pulsar_url)
        self.producer = self.client.create_producer(topic)

    def send(self, message):
        self.producer.send(message.encode('utf-8'))


class Consumer(object):
    def __init__(self, pulsar_url, topic, subscription_name, process_message):
        self.topic = topic
        self.subscription_name = subscription_name
        self.process_message = process_message

        self.client = pulsar.Client(pulsar_url)
        self.consumer = self.client.subscribe(topic=topic,
                                              subscription_name=subscription_name,
                                              consumer_type=pulsar.ConsumerType.Shared,
                                              message_listener=self.message_listener)

    def message_listener(self, consumer, message):
        try:
            self.process_message(message)
            # Acknowledge successful processing of the message
            consumer.acknowledge(message)
        except Exception:
            # Message failed to be processed
            consumer.negative_acknowledge(message)

    def start(self):
        self.consumer.resume_message_listener()

    ## 获取消息队列里消息数
    def get_message_count(self,pulsar_admin_url):
        url = f'{pulsar_admin_url}/admin/v2/persistent/public/default/{self.topic}/stats'
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            data = json.loads(response.text)
            subscriptions = data['subscriptions']
            if self.subscription_name in subscriptions.keys():
                return subscriptions[self.subscription_name]['msgBacklog']
        return -1

