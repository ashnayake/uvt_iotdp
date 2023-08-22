from datetime import datetime
import random

def temp_gen():
    now=datetime.now()
    curr_time=now.strftime("%H:%M:%S")
    return (30+random.randint(-10,10),curr_time)

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json


ENDPOINT = "xxxxxxxxxxxxxxxxxxxx"
CLIENT_ID = "xxxx"
PATH_TO_CERTIFICATE = "xxxxx"
PATH_TO_PRIVATE_KEY = "xxxxx"
PATH_TO_AMAZON_ROOT_CA_1 = "xxxxxx"
TOPIC = "xxxxxx"

event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )

print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))

connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

def pub_temp(t):
    message = {"temp":t[0],"time" : t[1]}
    mqtt_connection.publish(
        topic=TOPIC, 
        payload=json.dumps(message), 
        qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'xxxxx'")
    
def run():
    print('Begin Publish')
    while True:
        pub_temp(temp_gen())
        t.sleep(2)
    print('Publish End')
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    
run()