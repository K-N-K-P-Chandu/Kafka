# Kafka Python Demo: Orders Producer & Tracker

A beginner-friendly, end-to-end example of Apache Kafka using Python. It spins up Kafka locally with Docker, sends a JSON order event with a producer (`producer.py`), and tracks incoming orders with a consumer (`tracker.py`). This repo is designed to be a gentle on-ramp: short code, clear steps, and practical explanations.

## 1. Project Overview

- Purpose: demonstrate event streaming with Kafka using a simple “orders” workflow.
- Core functionality:
  - `producer.py` publishes a JSON order to the `orders` topic.
  - `tracker.py` subscribes to `orders` and prints each new order.
- Benefits and use cases:
  - Decoupled microservices: producers and consumers don’t call each other directly.
  - Real-time processing: events are delivered quickly and can be replayed.
  - Scalable pipelines: add partitions and consumer groups to process more data.
  - Typical scenarios: order processing, notifications, inventory updates, analytics dashboards.

## 2. Getting Started

- Prerequisites:
  - Windows 10/11, WSL optional.
  - Docker Desktop installed and running.
  - Python `>= 3.10` with `pip`.
  - Optional: Git + GitHub CLI (`gh`).
- Environment setup:
  - Create and activate a virtual environment:
    - PowerShell: `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1`
  - Install Python dependency:
    - `pip install confluent-kafka`
- Start Kafka (Docker Compose):
  - `docker-compose up -d`
  - Verify: `docker ps` shows a `kafka` container exposing `9092`.
- Screenshots (placeholders; add your images under `docs/screenshots/`):
  - ![Docker Desktop running](docs/screenshots/docker_desktop_running.png)
  - ![Kafka container healthy](docs/screenshots/kafka_container_healthy.png)

## 3. Configuration

- Docker Compose (`docker-compose.yaml`):
  - Uses `confluentinc/cp-kafka:7.8.4` with KRaft mode (no ZooKeeper).
  - Key environment variables explained:
    - `KAFKA_KRAFT_MODE`: enables KRaft (built-in metadata management).
    - `CLUSTER_ID`: unique identifier for the KRaft cluster.
    - `KAFKA_NODE_ID`: broker/controller node ID.
    - `KAFKA_PROCESS_ROLES`: `broker,controller` to run both roles in one container.
    - `KAFKA_CONTROLLER_QUORUM_VOTERS`: controller quorum binding (`1@kafka:9093`).
    - `KAFKA_LISTENERS`: internal listener map; `PLAINTEXT://0.0.0.0:9092` for clients.
    - `KAFKA_ADVERTISED_LISTENERS`: `PLAINTEXT://localhost:9092` so clients connect via localhost.
    - `KAFKA_CONTROLLER_LISTENER_NAMES`: names the controller listener.
    - `KAFKA_LOG_DIRS`: storage path inside the container.
  - Volume `kafka_kraft` persists Kafka logs.
- Application configs:
  - Producer (`producer.py`): `bootstrap.servers='localhost:9092'`.
  - Consumer (`tracker.py`): same `bootstrap.servers`, `group.id='order-tracker'`, `auto.offset.reset='earliest'`.
- Topic setup (`orders`):
  - Most Confluent images auto-create a topic when a producer writes; if disabled, create explicitly:
    - `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --create --topic orders --partitions 1 --replication-factor 1`

## 4. Usage

- Step-by-step:
  1) Start Kafka: `docker-compose up -d`
  2) Start the consumer (tracker) first: `python tracker.py`
  3) In a second terminal, run the producer: `python producer.py`
  4) Observe delivery logs in the producer and order prints in the consumer.
 - Command-line arguments:
   - None. The scripts use static configuration and a single sample order for simplicity.
- Customizing:
  - Edit the `order` dict in `producer.py` to simulate different payloads.
  - Adjust `group.id` in `tracker.py` to join/scale consumer groups.

## 5. Technical Details

- Key concepts and terminology:
  - Producer: application that publishes events to Kafka.
  - Consumer: application that reads events from Kafka topics.
  - Topic: logical stream (e.g., `orders`) storing events in an append-only log.
  - Partition: a topic shard enabling parallelism; messages in a partition are ordered.
  - Broker: Kafka server that stores and serves topic partitions.
  - Consumer Group: a set of consumer instances that share partitions for scalability.
  - Offset: position of a message within a partition; consumers commit/read by offset.
  - KRaft: Kafka’s built-in metadata quorum (replaces ZooKeeper).
 
 (Code examples are intentionally omitted here to keep the README focused on concepts and operations.)
- Architecture diagrams:
  - Event flow (Mermaid):
    ```mermaid
    flowchart LR
      P[Python Producer] -- JSON order --> T[(Kafka Topic: orders)]
      T --> C[Python Consumer (order-tracker)]
    ```
  - Single-broker local setup (Mermaid):
    ```mermaid
    graph TD
      D[Docker Desktop] --> K[Kafka (cp-kafka:7.8.4)]
      K --> T[(Topics & Partitions)]
      P[Producer.py] --> K
      C[Tracker.py] --> K
    ```

## Kafka CLI Commands

- `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list`
  - Purpose: lists all topics available on the local broker.
  - Why necessary: verifies Kafka is reachable and confirms expected topics exist.

- `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --create --topic orders --partitions 1 --replication-factor 1`
  - Purpose: creates the `orders` topic with one partition.
  - Why necessary: ensures a known topic exists for producer and consumer when auto-creation is disabled.

- `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic orders`
  - Purpose: shows partition count, replicas, leader, and configuration for `orders`.
  - Why necessary: validates topic layout before scaling consumers or tuning performance.

- `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --delete --topic orders`
  - Purpose: deletes the topic.
  - Why necessary: cleans up local environments or resets data between test runs.

- `docker exec -it kafka kafka-console-producer --bootstrap-server localhost:9092 --topic orders`
  - Purpose: sends test messages interactively to the topic.
  - Why necessary: quick sanity check without writing application code.

- `docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic orders --from-beginning`
  - Purpose: reads messages from `orders` starting at the earliest offset.
  - Why necessary: confirms that messages are landing in the topic and tests consumer behavior.

- `docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list`
  - Purpose: lists all known consumer groups.
  - Why necessary: visibility into group names created by your consumers.

- `docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group order-tracker`
  - Purpose: shows group state, assigned partitions, lag, and offsets for `order-tracker`.
  - Why necessary: monitors progress and lag to diagnose performance or delivery issues.

Note: All commands run inside the `kafka` container via `docker exec`. Replace `localhost:9092` if you change advertised listeners.

## 6. Support

- Troubleshooting:
  - Kafka not reachable (`Broker transport failure`): ensure Docker Desktop is running; restart: `docker-compose restart`.
  - Port conflict on `9092`: stop other services or change `KAFKA_ADVERTISED_LISTENERS` and client configs.
  - `pip install confluent-kafka` fails: update `pip` and Python; on Windows ensure latest Visual C++ Redistributable.
  - Consumer prints nothing: start consumer before producer; ensure topic exists; check group offset reset is `earliest`.
- FAQs:
  - Do I need to manually create topics? Often no (auto-creation); if disabled, use `kafka-topics --create` (see above).
  - How is Kafka different from traditional message brokers? Kafka persists events on disk, enabling replay and multiple independent consumers.
  - How do I scale consumers? Increase partitions; run more consumer instances with the same `group.id`.
- Getting help:
  - Issues: open a GitHub issue on your repo.
  - Kafka docs: https://kafka.apache.org/documentation/
  - Confluent Python client: https://github.com/confluentinc/confluent-kafka-python

---

### Repository Notes
- Committed files only: `docker-compose.yaml`, `producer.py`, `tracker.py`.
- This README is provided locally for onboarding; you can commit it later if desired.