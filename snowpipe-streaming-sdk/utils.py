import os
import ast
import pandas as pd
import prettytable as pt
from datetime import datetime

os.environ["SS_LOG_LEVEL"] = "warn"


def display_results(info: dict) -> None:

    info = {k: [v] for k, v in info.items()}
    df = pd.DataFrame(info).T
    table = pt.PrettyTable()
    table.field_names = ['KEY', 'VALUE']
    for row in df.itertuples(index=True):
        table.add_row(row)
    table.align['KEY'] = 'r'
    table.align['VALUE'] = 'l'
    print(table)
    return


def util_get_channel_status(channel_name):
    info = client.get_channel_statuses([channel_name])
    info = info[args.channel].__dict__
    info = {k.lstrip('_').upper(): v for k, v in info.items()}

    for key in [
        'CREATED_ON_MS', 
        'LAST_ERROR_TIMESTAMP_MS', 
        'LAST_REFRESHED_ON_MS'
    ]:
        if isinstance(info[key], int):
            ts = datetime.fromtimestamp(info[key] / 1000)
            ts = ts.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            info[key] = ts
    display_results(info)
    return


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--database", default='MY_KAFKA_DB')
    parser.add_argument("-s", "--schema", default='MY_KAFKA_SCHEMA')
    parser.add_argument("-p", "--pipe", default='MY_PIPE')
    parser.add_argument("-c", "--channel", default="TEST_CHANNEL")
    # streaming utilities
    parser.add_argument("-r", "--drop-channel", action='store_true')
    parser.add_argument("-o", "--get-offset", action='store_true')
    parser.add_argument("-S", "--get-status", action='store_true')
    parser.add_argument("-f", "--flush", action='store_true')
    parser.add_argument("-w", "--wait", action='store_true')
    parser.add_argument("-t", "--time", type=int, default=10)
    parser.add_argument("-a", "--append-row", action='store_true')
    parser.add_argument("-D", "--data", default="(,)")
    args = parser.parse_args()

    from snowflake.ingest.streaming import StreamingIngestClient
    client = StreamingIngestClient(
        client_name="SSv2_utils",
        db_name=args.database,
        schema_name=args.schema,
        pipe_name=args.pipe,
        profile_json="profile.json"
    )
    print(f"Connectted to {args.database}.{args.schema}.{args.pipe}")

    if args.get_status:
        util_get_channel_status(args.channel)
        client.close()

    if args.append_row:
        data, idx = ast.literal_eval(args.data)
        channel, status = client.open_channel(args.channel)
        channel.append_row(data, str(idx))
        client.close()

    if args.get_offset:
        info = client.get_latest_committed_offset_tokens([args.channel])
        display_results(info)
        client.close()
    
    if args.flush:
        channel, status = client.open_channel(args.channel)
        channel.initiate_flush()
        util_get_channel_status(args.channel)
        client.close()

    if args.wait:
        channel, status = client.open_channel(args.channel)
        channel.wait_for_flush(args.time)
        util_get_channel_status(args.channel)
        client.close()

    if args.drop_channel:
        channel, status = client.open_channel(args.channel)
        channel.close()
        client.drop_channel(args.channel)
        print(f"Channel dropped: {args.channel}")
        client.close()

print(f"Client disconnected: {client.client_name}")