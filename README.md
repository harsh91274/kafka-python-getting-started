# Kafka Python Getting Started

A simple Kafka producer and consumer example using the Confluent Kafka Python client library. This project demonstrates how to send and receive messages from a Kafka topic.

## Description

This project contains two Python scripts:
- **producer.py**: Sends random purchase events (user-product combinations) to a Kafka topic named "purchases"
- **consumer.py**: Consumes and displays messages from the "purchases" topic

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

### Start the Consumer

In one terminal, activate the virtual environment and run the consumer:

```bash
source env/bin/activate
python consumer.py
```

The consumer will wait for messages and display them as they arrive. Press `Ctrl+C` to stop.

### Start the Producer

In another terminal, activate the virtual environment and run the producer:

```bash
source env/bin/activate
python producer.py
```

The producer will send 10 random purchase events to the "purchases" topic and then exit.

## Configuration

Both scripts are configured to connect to a Kafka broker at `localhost:54689`. To change this, modify the `bootstrap.servers` value in both `producer.py` and `consumer.py`.

## Notes

- Make sure your Kafka cluster is running before starting the consumer or producer
- The consumer uses consumer group `kafka-python-getting-started` and will read from the earliest offset
- The producer sends messages with product names as keys and user IDs as values

