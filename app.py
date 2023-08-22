from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import threading

ENDPOINT = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CLIENT_ID = "xxxxx"
PATH_TO_CERTIFICATE = "xxxxx.pem.crt"
PATH_TO_PRIVATE_KEY = "xxxxx.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "xxxxx"
topic_alarm = "xxxxx"
topic_temp="xxxx"

event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection_alarm = mqtt_connection_builder.mtls_from_path(
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

connect_future_alarm = mqtt_connection_alarm.connect()
connect_future_alarm.result()
print("Connected!")

def pub_alarm_stat(stat,time,topic_alarm):
    message = {"status":stat,"time":time}
    mqtt_connection_alarm.publish(topic=topic_alarm, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + topic_alarm)
    
def on_message_received_temp(topic, payload, dup, qos, retain):
    data_dict = json.loads(payload.decode('utf-8'))
    t=data_dict['time']
    if data_dict['temp']>30:
        pub_alarm_stat("on",t,"xxxx")
    else:
        pub_alarm_stat("off",t,"xxxx")
        
subscribe_future, packet_id = mqtt_connection_alarm.subscribe(
    topic="xxxx",
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received_temp
)

subscribe_result = subscribe_future.result()
print(f'Subscribed to {topic_temp}')

threading.Event().wait()