from confluent_kafka import Consumer
import json
import uuid

consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'order-tracker',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)

consumer.subscribe(["orders"])

print(" \n🟩 Consumer is running and subscribed to topic 'orders' \n")

try:
    while True:
        msg = consumer.poll(1.0)
        # .Poll() -> Asks the broker for any new messages on the subscribed topics and returns them to the consumer for processing.
        # 1.0 -> Timeout in seconds. 
        # If no message is available within this time, poll() returns None.
        if msg is None:
            continue
        if msg.error():
            print(f"❓ Consumer error: {msg.error()}")
            continue
        value = msg.value().decode("utf-8")
        order = json.loads(value)
        print(f"✅Received Order: {order['quantity']} * {order['items']} from {order['user']}\n ")

except KeyboardInterrupt:
    print(" 🟥 Consumer is stopped due to interrupted by user \n")

finally:
    consumer.close()

