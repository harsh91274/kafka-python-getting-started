1. Install java SDK and add variables to PATH

brew install openjdk@11

- Add path variables to .zshrc
export PATH=”/usr/local/opt/openjdk@11/bin:$PATH”
export CPPFLAGS=”-I/usr/local/opt/openjdk@11/include”

2. Download and install kafka with zookeeper
curl https://archive.apache.org/dist/kafka/3.3.1/kafka_2.12-3.9.1.tgz --output kafka_2.12-3.9.1.tgz
tar -xzf kafka_2.12-3.9.1.tgz

3. Download Snowflake Kafka Connector from Maven - https://mvnrepository.com/artifact/com.snowflake/snowflake-kafka-connector

4. Setup Snowflake roles and tables for ingestion from Kafka. Steps are explained in snowflake_setup.sql file.

5. Add SF_connect.properties file in the kafka_*/config folder and modify properties 

# generate private key first
openssl genrsa -out privatekey.pem 2048

# generate publickey
openssl rsa -in privatekey.pem -pubout -out publickey.crt

6. Run kafka on desktop - needs 4 terminals 

A. Run Zookeeper
cd ~/kafka_2.12-3.9.1
bin/zookeeper-server-start.sh config/zookeeper.properties

B. Start Kafka Server
cd ~/kafka_2.12-3.9.1
bin/kafka-server-start.sh config/server.properties

C. Start Kafka Connector for Snowflake
cd ~/kafka_2.12-3.9.1
bin/connect-standalone.sh ./config/connect-standalone.properties ./config/SF_connect.properties

D. Run console producer and add sample data
cd ~/kafka_2.12-3.9.1
bin/kafka-console-producer.sh --topic my_kafka_topic --bootstrap-server localhost:9092

7. Check table on Snowflake