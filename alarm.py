from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import threading

ENDPOINT = ""
CLIENT_ID = "alarm1"
PATH_TO_CERTIFICATE = ""
PATH_TO_PRIVATE_KEY = ""
PATH_TO_AMAZON_ROOT_CA_1 = ""
topic = "alarm/alarm1"

# Spin up resources
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

def on_message_received(topic, payload, dup, qos, retain):
    print(payload)
    
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=topic,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received
)

subscribe_result = subscribe_future.result()
print(f'Subscribed to {topic}')

threading.Event().wait()