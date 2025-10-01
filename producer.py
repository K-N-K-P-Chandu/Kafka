from confluent_kafka import Producer
import json
import uuid

producer_config = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(producer_config)

def delivery_report(err, msg):
    if err is not None:
        print(f" 😒 Delivery failed: {err}")
    else:
        print(f" 😁 Delivered Success  {msg.value().decode('utf-8')}") 
        # dir() :- Returns a list of all attributes and methods available for an object.
        print(f"✅ Message Delivered to Topic: {msg.topic()} : Partition {msg.partition()}: at Offset {msg.offset()}")

order = {
    "order_id": str(uuid.uuid4()),
    "user" : "krishna",
    "items": "Rice bowl",
    "quantity": 5
}

byte_kafka_format = json.dumps(order).encode("utf-8")

producer.produce(
    topic="orders",
    value=byte_kafka_format,
    callback=delivery_report
    )
producer.flush()