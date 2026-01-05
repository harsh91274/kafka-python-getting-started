# Kafka Python Getting Started

A simple Kafka producer and consumer example using the Confluent Kafka Python client library. This project demonstrates how to send and receive messages from a Kafka topic.

## Description

This project contains two sets of Python scripts:

### Root Directory Scripts
- **producer.py**: Sends random purchase events (user-product combinations) to a Kafka topic named "purchases"
- **consumer.py**: Consumes and displays messages from the "purchases" topic

### kafka-python Directory Scripts
- **kafka-python/producer.py**: Sends greeting messages to a Kafka topic named "hello_topic" using Confluent Cloud configuration
- **kafka-python/consumer.py**: Consumes and displays messages from the "hello_topic" using a consumer group
- **kafka-python/config.py**: Configuration file containing Kafka broker connection settings (contains sensitive credentials - not tracked in git)
- **kafka-python/client.properties**: Properties file with Kafka client configuration (contains sensitive credentials - not tracked in git)

## Prerequisites

- Python 3.12+
- Kafka container from Confluent. Can be downloaded using Homebrew with the command 'brew install confluentinc/tap/cli'. 
- Kafka cluster running on `localhost:54689`
- Virtual environment (already set up in `env/`)

## Setup

1. Activate the virtual environment:
   ```bash
   source env/bin/activate
   ```

2. Install dependencies (if not already installed):
   ```bash
   pip install confluent-kafka
   ```

## Running the Code

### Root Directory Scripts

#### Start the Consumer

In one terminal, activate the virtual environment and run the consumer:

```bash
source env/bin/activate
python consumer.py
```

The consumer will wait for messages and display them as they arrive. Press `Ctrl+C` to stop.

#### Start the Producer

In another terminal, activate the virtual environment and run the producer:

```bash
source env/bin/activate
python producer.py
```

The producer will send 10 random purchase events to the "purchases" topic and then exit.

### kafka-python Directory Scripts

The scripts in the `kafka-python/` directory are configured to work with Confluent Cloud. Before running these scripts, ensure that `kafka-python/config.py` contains your Kafka broker configuration.

#### Start the Consumer

In one terminal, navigate to the kafka-python directory, activate the virtual environment, and run the consumer:

```bash
source ../env/bin/activate
cd kafka-python
python consumer.py
```

Or run directly:
```bash
source env/bin/activate
python kafka-python/consumer.py
```

The consumer will subscribe to the "hello_topic" and wait for messages. Press `Ctrl+C` to stop.

#### Start the Producer

In another terminal, navigate to the kafka-python directory, activate the virtual environment, and run the producer:

```bash
source ../env/bin/activate
cd kafka-python
python producer.py
```

Or run directly:
```bash
source env/bin/activate
python kafka-python/producer.py
```

The producer will send greeting messages for multiple names to the "hello_topic" and then exit.

## Configuration

### Root Directory Scripts

Both scripts are configured to connect to a Kafka broker at `localhost:54689`. To change this, modify the `bootstrap.servers` value in both `producer.py` and `consumer.py`.

### kafka-python Directory Scripts

The scripts in the `kafka-python/` directory use a shared configuration file (`kafka-python/config.py`) that contains Kafka broker connection settings. This file contains sensitive credentials and is excluded from version control. You'll need to create this file with your Kafka broker configuration before running these scripts.

The configuration should include:
- `bootstrap.servers`: Kafka broker address
- `security.protocol`: Security protocol (e.g., SASL_SSL)
- `sasl.mechanisms`: SASL mechanism (e.g., PLAIN)
- `sasl.username`: SASL username
- `sasl.password`: SASL password

## Notes

- Make sure your Kafka cluster is running before starting the consumer or producer
- The consumer uses consumer group `kafka-python-getting-started` and will read from the earliest offset
- The producer sends messages with product names as keys and user IDs as values

