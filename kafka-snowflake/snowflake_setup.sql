-- Create a Snowflake role with the privileges to work with the connector.
CREATE ROLE my_kafka_connector_role;  --**

create database my_kafka_db;  --**

-- create a warehouse
CREATE OR REPLACE WAREHOUSE my_kafka_warehouse WITH WAREHOUSE_SIZE='SMALL';

-- Grant privileges on the database.
GRANT USAGE ON DATABASE my_kafka_db TO ROLE my_kafka_connector_role;
-- or
GRANT ALL ON DATABASE my_kafka_db TO ROLE my_kafka_connector_role;  --**

CREATE SCHEMA MY_KAFKA_DB.MY_KAFKA_SCHEMA;

-- Grant privileges on the schema.
GRANT USAGE ON SCHEMA my_kafka_schema TO ROLE my_kafka_connector_role;
GRANT USAGE ON WAREHOUSE my_kafka_warehouse TO ROLE my_kafka_connector_role;
GRANT CREATE TABLE ON SCHEMA my_kafka_schema TO ROLE my_kafka_connector_role;
GRANT CREATE STAGE ON SCHEMA my_kafka_schema TO ROLE my_kafka_connector_role;
GRANT CREATE PIPE ON SCHEMA my_kafka_schema TO ROLE my_kafka_connector_role;

-- or
GRANT ALL ON SCHEMA my_kafka_schema TO ROLE my_kafka_connector_role;  --**

-- Only required if the Kafka connector will load data into an existing table.
GRANT OWNERSHIP ON TABLE existing_table TO ROLE my_kafka_connector_role;

-- Only required if the Kafka connector will stage data files in an existing internal stage: (not recommended).
GRANT READ, WRITE ON STAGE existing_stage TO ROLE my_kafka_connector_role;

create user my_kafka_connector_user;  --**

-- Grant the custom role to an existing user.
GRANT ROLE my_kafka_connector_role TO USER my_kafka_connector_user;  --**

-- Set the custom role as the default role for the user.
-- If you encounter an 'Insufficient privileges' error, verify the role that has the OWNERSHIP privilege on the user.
ALTER USER my_kafka_connector_user SET DEFAULT_ROLE = my_kafka_connector_role;  --**

alter user my_kafka_connector_user set RSA_PUBLIC_KEY='put your public key here';  --**

-- view inserted data
select * from MY_KAFKA_DB.MY_KAFKA_SCHEMA.MY_KAFKA_TABLE;

alter warehouse my_kafka_warehouse suspend;