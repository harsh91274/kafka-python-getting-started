-- step 05: create authenication policy for service account user
CREATE OR REPLACE AUTHENTICATION POLICY auth_streaming_keypair2
  AUTHENTICATION_METHODS = ('KEYPAIR')
  CLIENT_TYPES = ('SNOWFLAKE_CLI', 'SNOWSQL', 'DRIVERS');


ALTER USER my_kafka_connector_user 
  SET AUTHENTICATION POLICY auth_streaming_keypair2;

alter user my_kafka_connector_user unset authentication policy;

use role my_kafka_connector_user;

CREATE OR REPLACE TABLE MY_TABLE (
    data VARIANT,
    c1 NUMBER,
    c2 STRING
);

CREATE OR REPLACE PIPE MY_PIPE
AS 
COPY INTO MY_TABLE 
FROM (
  SELECT $1, $1:c1, $1:ts 
  FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING'))
);

GRANT SELECT, INSERT, EVOLVE SCHEMA
ON TABLE MY_KAFKA_DB.MY_KAFKA_SCHEMA.MY_TABLE
TO ROLE my_kafka_connector_role;

GRANT OPERATE
ON PIPE MY_KAFKA_DB.MY_KAFKA_SCHEMA.MY_PIPE
TO ROLE my_kafka_connector_role;


SHOW CHANNELS;

SELECT * FROM MY_KAFKA_DB.MY_KAFKA_SCHEMA.MY_TABLE;