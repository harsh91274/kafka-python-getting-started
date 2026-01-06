import os
os.environ["SS_LOG_LEVEL"] = "warn"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--database", default='<database_name>')
parser.add_argument("-s", "--schema", default='<schema_name>')
parser.add_argument("-p", "--pipe", default='MY_PIPE')
args = parser.parse_args()
print(f"Testing connection to {args.database}.{args.schema}.{args.pipe}")

from snowflake.ingest.streaming import StreamingIngestClient
client = StreamingIngestClient(
    client_name="TEST_CONNECTION",
    db_name=args.database,
    schema_name=args.schema,
    pipe_name=args.pipe,
    profile_json="profile.json"
)
print(f"Client connected successfully: {client.client_name}")

channel, status = client.open_channel("TEST_CHANNEL")
print(f"Channel opened: {channel.channel_name}")

channel.close()
print(f"Channel closed: {channel.channel_name}")

client.close()
print(f"Client disconnected: {client.client_name}")