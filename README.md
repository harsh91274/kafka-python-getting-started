# Kafka Python Getting Started

A comprehensive Kafka project demonstrating producer/consumer patterns with Python and integration with Snowflake using the Kafka Connect framework. This project includes examples of sending and receiving messages from Kafka topics, as well as streaming data from a local Kafka deployment to Snowflake.

## Description

This project contains multiple components:

### Root Directory Scripts
- **producer.py**: Sends random purchase events (user-product combinations) to a Kafka topic named "purchases"
- **consumer.py**: Consumes and displays messages from the "purchases" topic

### kafka-python Directory Scripts
- **kafka-python/producer.py**: Sends greeting messages to a Kafka topic named "hello_topic" using Confluent Cloud configuration
- **kafka-python/consumer.py**: Consumes and displays messages from the "hello_topic" using a consumer group
- **kafka-python/config.py**: Configuration file containing Kafka broker connection settings (contains sensitive credentials - not tracked in git)
- **kafka-python/client.properties**: Properties file with Kafka client configuration (contains sensitive credentials - not tracked in git)

### kafka-snowflake Directory
This directory contains configuration and setup files for integrating a local Kafka deployment with Snowflake using the Snowflake Kafka Connector:
- **SF_connect.properties**: Kafka Connect configuration file for the Snowflake Sink Connector
- **snowflake_setup.sql**: SQL script to set up Snowflake roles, databases, schemas, and users required for the Kafka connector
- **kafka-connect-with-snowflake.md**: Detailed setup and installation instructions for the Kafka-Snowflake integration

## Prerequisites

### For Python Scripts
- Python 3.12+
- Kafka container from Confluent. Can be downloaded using Homebrew with the command `brew install confluentinc/tap/cli`
- Kafka cluster running on `localhost:54689`
- Virtual environment (already set up in `env/`)

### For Kafka-Snowflake Integration
- Java SDK 11+ (OpenJDK)
- Apache Kafka 3.3.1+ with Zookeeper
- Snowflake account with appropriate privileges
- Snowflake Kafka Connector JAR file

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

### Kafka-Snowflake Integration

This integration demonstrates how to stream data from a local Kafka deployment to Snowflake using the Snowflake Kafka Connector. The connector uses Snowpipe Streaming for real-time data ingestion.

#### Setup Instructions

1. **Install Java SDK 11**:
   ```bash
   brew install openjdk@11
   ```
   
   Add to your `~/.zshrc`:
   ```bash
   export PATH="/usr/local/opt/openjdk@11/bin:$PATH"
   export CPPFLAGS="-I/usr/local/opt/openjdk@11/include"
   ```

2. **Download and Install Kafka**:
   ```bash
   curl https://archive.apache.org/dist/kafka/3.3.1/kafka_2.12-3.9.1.tgz --output kafka_2.12-3.9.1.tgz
   tar -xzf kafka_2.12-3.9.1.tgz
   ```

3. **Download Snowflake Kafka Connector**:
   Download from [Maven Repository](https://mvnrepository.com/artifact/com.snowflake/snowflake-kafka-connector) and place the JAR file in the Kafka `libs/` directory.

4. **Set up Snowflake**:
   - Run the SQL script in `kafka-snowflake/snowflake_setup.sql` in your Snowflake account
   - This creates the necessary roles, databases, schemas, users, and grants required permissions
   - Generate RSA key pair for authentication:
     ```bash
     openssl genrsa -out privatekey.pem 2048
     openssl rsa -in privatekey.pem -pubout -out publickey.crt
     ```
   - Update the public key in Snowflake (line 41 of `snowflake_setup.sql`)

5. **Configure Kafka Connect**:
   - Copy `kafka-snowflake/SF_connect.properties` to your Kafka installation's `config/` directory
   - Update the following properties in `SF_connect.properties`:
     - `snowflake.url.name`: Your Snowflake account URL
     - `snowflake.private.key`: Path to your private key file
     - Adjust other settings as needed (database, schema, user, role, warehouse names)

#### Running the Kafka-Snowflake Integration

You'll need **4 terminal windows**:

**Terminal 1 - Start Zookeeper**:
```bash
cd ~/kafka_2.12-3.9.1
bin/zookeeper-server-start.sh config/zookeeper.properties
```

**Terminal 2 - Start Kafka Server**:
```bash
cd ~/kafka_2.12-3.9.1
bin/kafka-server-start.sh config/server.properties
```

**Terminal 3 - Start Kafka Connect for Snowflake**:
```bash
cd ~/kafka_2.12-3.9.1
bin/connect-standalone.sh ./config/connect-standalone.properties ./config/SF_connect.properties
```

**Terminal 4 - Produce Messages**:
```bash
cd ~/kafka_2.12-3.9.1
bin/kafka-console-producer.sh --topic my_kafka_topic --bootstrap-server localhost:9092
```

Type messages in Terminal 4, and they will be automatically ingested into Snowflake. Check your Snowflake table:
```sql
SELECT * FROM MY_KAFKA_DB.MY_KAFKA_SCHEMA.MY_KAFKA_TABLE;
```

For detailed setup instructions, refer to `kafka-snowflake/kafka-connect-with-snowflake.md`.

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
- For the Kafka-Snowflake integration, ensure all four services (Zookeeper, Kafka Server, Kafka Connect, and Producer) are running simultaneously
- The Snowflake connector uses Snowpipe Streaming for real-time ingestion with minimal latency
- Configuration files containing sensitive credentials (`config.py`, `client.properties`, `SF_connect.properties`) are excluded from version control

