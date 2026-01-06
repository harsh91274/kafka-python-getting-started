1. pip install snowpipe-streaming snowflake pandas
2. Create profile.json
{
    "user": "",
    "account": "",
    "url": "",
    "private_key_file": "rsa_key.p8"
}
3. Run the scripts 
python test_connection.py -d <database_name> -s <schema_name> -p MY_PIPE

4. create utils.py using Snowpipe streaming SDK

5. Ingest one row of data

DATA='({"c1": 111, "c2": 222, "ts": "2025-10-16 :23:59:59"},  101)'
python utils.py --channel TEST_CHANNEL --append-row --data $DATA

6. Get latest committed token 

python utils.py --channel TEST_CHANNEL --get-offset

7. Drop channel
python utils.py --channel TEST_CHANNEL --drop-channel
