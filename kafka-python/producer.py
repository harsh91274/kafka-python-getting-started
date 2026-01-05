#!/usr/bin/env python
from confluent_kafka import Producer
from config import config

def callback(err, event):
    if err:
        print(f'ERROR: Message failed delivery: {err}')
    else:
        val = event.value().decode('utf8')
        print(f'{val} sent to partition {event.partition()}.')
        
        
def say_hello(producer, key):
    value = f'Hello {key}!'
    producer.produce('hello_topic', value, key, callback=callback)
    
    
if __name__ == '__main__':
    producer = Producer(config)
    keys = ['Amy', 'Brenda', 'Cindy', 'Derrick', 'Elaine', 'Fred']
    [say_hello(producer, key) for key in keys]
    producer.flush()