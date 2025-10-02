# Kafka Demo: with python ('Orders', 'Producer' & 'Tracker')

This guide helps you run a simple Kafka workflow locally using Docker and Python. It includes a producer (`producer.py`) that sends a sample order and a consumer (`tracker.py`) that reads and prints new orders from the `orders` topic.

## 1. Project Overview

- Purpose: demonstrate a basic Kafka “orders” pipeline with Python.
- What it does:
  - `producer.py` sends a JSON order to topic `orders`.
  - `tracker.py` consumes from `orders` and logs each order.
- Why it’s useful:
  - Easy local testing for event-driven workflows.

## 2. Getting Started

- Prerequisites:
  - Windows 10/11
  - Docker Desktop running
  - Python `>= 3.10` and `pip`
- Environment setup:
  - Create and activate a virtual environment:
    - PowerShell: `python -m venv .venv` then `\.venv\Scripts\Activate.ps1`
  - Install dependency: `pip install confluent-kafka`
- Start Kafka:
  - `docker-compose up -d`
  - Verify with `docker ps` that `kafka` is up and `9092` is exposed.

## 3. Configuration

- Docker Compose (`docker-compose.yaml`):
  - Image: `confluentinc/cp-kafka:7.8.4` in KRaft mode (no ZooKeeper).
  - Key settings:
    - `KAFKA_LISTENERS`: includes `PLAINTEXT://0.0.0.0:9092` for client connections.
    - `KAFKA_ADVERTISED_LISTENERS`: `PLAINTEXT://localhost:9092` so apps connect via `localhost`.
    - `KAFKA_PROCESS_ROLES`: `broker,controller` for a single-node KRaft setup.
- App config:
  - Producer: `bootstrap.servers='localhost:9092'`.
  - Consumer: same server, `group.id='order-tracker'`, `auto.offset.reset='earliest'`.
- Topic:
  - If auto-creation is disabled, create `orders` with the CLI command below.

### Important Notes

- Version Compatibility
  - If you use a newer Kafka release, update the Docker image tag in `docker-compose.yaml` to match: `image: confluentinc/cp-kafka:<your-version>`.
  - Check the running Kafka version inside the container: `docker exec -it kafka kafka-topics --version`.
  - After changing the image version, recreate services: `docker-compose down -v && docker-compose up -d`.

- Volume Path Configuration (Windows)
  - This setup uses a Docker named volume (`kafka_kraft`), so no host path changes are required by default.
  - To use a bind mount to a specific Windows folder for persistence, replace the volume line with: `- C:\\Users\\<your-username>\\kafka-data:/var/lib/kafka/data`.
  - Steps to validate and update:
    - Create the host folder: `C:\Users\<your-username>\kafka-data`.
    - In Docker Desktop, ensure the drive/folder is shared (Settings → Resources → File Sharing).
    - Update `services.kafka.volumes` in `docker-compose.yaml` with your path.
    - Recreate services: `docker-compose down` then `docker-compose up -d`.
  - Verify the mount is active: `docker inspect kafka --format '{{json .Mounts}}'` and confirm `Source` points to your Windows path.

## 4. Usage

- Steps:
  - Start Kafka: `docker-compose up -d`
  - Run consumer: `python tracker.py`
  - Run producer (another terminal): `python producer.py`
  - Observe consumer output for the received order.
- Notes:
  - Scripts use fixed settings for simplicity (no CLI args).
  - Edit the `order` object in `producer.py` to change the payload.

## 5. Technical Details (Quick Definitions)

- Producer: publishes events to Kafka.
- Consumer: reads events from Kafka topics.
- Topic: logical stream (e.g., `orders`).
- Partition: shard of a topic; enables parallel processing.
- Broker: Kafka server storing topic partitions.
- Consumer Group: multiple consumers sharing work across partitions.
- Offset: position of a message within a partition.
- KRaft: Kafka’s built-in metadata quorum (no ZooKeeper).

## 6. Kafka CLI Commands

- `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list`
  - Purpose: lists all topics available on the broker.
  - Why: verify broker connectivity and expected topics.

- `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --create --topic orders --partitions 1 --replication-factor 1`
  - Purpose: creates the `orders` topic.
  - Why: ensure a predictable topic exists for producer/consumer.

- `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic orders`
  - Purpose: shows partition count, replicas, leader, and configuration.
  - Why: validate topic layout before scaling consumers.

- `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --delete --topic orders`
  - Purpose: deletes the topic.
  - Why: clean up local environments or reset data.

- `docker exec -it kafka kafka-console-producer --bootstrap-server localhost:9092 --topic orders`
  - Purpose: send test messages interactively.
  - Why: quick sanity check without application code.

- `docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic orders --from-beginning`
  - Purpose: read messages from `orders` starting at the earliest offset.
  - Why: confirm messages are landing and can be read.

- `docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list`
  - Purpose: list consumer groups.
  - Why: see groups created by your consumers.

- `docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group order-tracker`
  - Purpose: show group state, assigned partitions, lag, and offsets.
  - Why: monitor progress and diagnose delivery/lag issues.

Notes:
- Run commands inside the `kafka` container via `docker exec`.
- Replace `localhost:9092` if you change advertised listeners.

## 7. Support

- Common issues:
  - Broker unreachable: ensure Docker Desktop is running; `docker-compose restart`.
  - Port conflict on `9092`: stop other services or adjust listeners/client configs.
  - `pip install confluent-kafka` fails: update `pip`/Python; install latest Microsoft Visual C++ Redistributable on Windows.
  - Consumer prints nothing: start consumer before producer; check topic exists; use `auto.offset.reset='earliest'` for initial runs.
- Help and references:
  - Kafka docs: https://kafka.apache.org/documentation/
  - Confluent Python client: https://github.com/confluentinc/confluent-kafka-python
  - GitHub diagrams (Mermaid syntax support): https://docs.github.com/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams#creating-mermaid-diagrams